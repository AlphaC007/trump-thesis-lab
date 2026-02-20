#!/usr/bin/env python3
import json
import os
import urllib.error
import urllib.request

TOKEN_ADDRESS = "6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN"

MORALIS_ENDPOINTS = [
    f"https://solana-gateway.moralis.io/token/mainnet/{TOKEN_ADDRESS}/holders",
    f"https://solana-gateway.moralis.io/token/mainnet/{TOKEN_ADDRESS}/metadata",
]

SOLSCAN_ENDPOINTS = [
    f"https://pro-api.solscan.io/v2.0/token/holders?address={TOKEN_ADDRESS}&page=1&page_size=10",
    f"https://pro-api.solscan.io/v2.0/token/meta?address={TOKEN_ADDRESS}",
]


def mask(secret: str | None) -> str:
    if not secret:
        return "<missing>"
    if len(secret) <= 8:
        return "****"
    return f"{secret[:4]}***{secret[-4:]}"


def probe(name: str, url: str, headers: dict):
    req = urllib.request.Request(url, headers={"User-Agent": "trump-thesis-lab/debug-onchain"} | headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode("utf-8", errors="ignore")
            print(f"\n[{name}] {url}")
            print(f"status={r.status}")
            print("body[0:500]=")
            print(body[:500])
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"\n[{name}] {url}")
        print(f"status={e.code}")
        print("body[0:500]=")
        print(body[:500])
    except Exception as e:
        print(f"\n[{name}] {url}")
        print(f"error={e}")


def main():
    moralis = os.getenv("MORALIS_API_KEY")
    solscan = os.getenv("SOLSCAN_API_KEY")

    print("== Key presence (masked) ==")
    print("MORALIS_API_KEY:", mask(moralis))
    print("SOLSCAN_API_KEY:", mask(solscan))

    print("\n== Moralis probes ==")
    moralis_headers_list = []
    if moralis:
        moralis_headers_list.append({"X-API-Key": moralis})
        moralis_headers_list.append({"Authorization": f"Bearer {moralis}"})
    else:
        moralis_headers_list.append({})

    for h in moralis_headers_list:
        label = "moralis " + ("X-API-Key" if "X-API-Key" in h else "Authorization" if "Authorization" in h else "no-auth")
        for url in MORALIS_ENDPOINTS:
            probe(label, url, h)

    print("\n== Solscan probes ==")
    sol_headers_list = []
    if solscan:
        sol_headers_list.append({"token": solscan})
        sol_headers_list.append({"Authorization": f"Bearer {solscan}"})
    else:
        sol_headers_list.append({})

    for h in sol_headers_list:
        label = "solscan " + ("token" if "token" in h else "Authorization" if "Authorization" in h else "no-auth")
        for url in SOLSCAN_ENDPOINTS:
            probe(label, url, h)


if __name__ == "__main__":
    main()
