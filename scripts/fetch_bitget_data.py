#!/usr/bin/env python3
"""
Fetch on-chain data from Bitget Wallet API
Focus: tx stats, security audit, batch prices
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Bitget integration script path (private workspace)
BITGET_INTEGRATION = Path.home() / ".openclaw/workspace/tools/bitget_integration.py"

def fetch_trump_stats():
    """获取 TRUMP token 交易统计"""
    cmd = ["python3", str(BITGET_INTEGRATION), "tx-stats", "sol", "6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}
    return json.loads(result.stdout)

def fetch_trump_security():
    """获取 TRUMP token 安全审计"""
    cmd = ["python3", str(BITGET_INTEGRATION), "security", "sol", "6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}
    return json.loads(result.stdout)

def fetch_portfolio_prices():
    """批量获取投资组合价格（TRUMP + SOL + BTC + ETH）"""
    tokens = "sol:6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN,sol:,btc:,eth:"
    cmd = ["python3", str(BITGET_INTEGRATION), "batch-prices", tokens]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}
    return json.loads(result.stdout)

def main():
    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "bitget_wallet_api",
        "data": {}
    }
    
    # 1. TRUMP 交易统计
    print("Fetching TRUMP tx stats...", file=sys.stderr)
    tx_stats = fetch_trump_stats()
    if "error" not in tx_stats:
        output["data"]["trump_tx_stats"] = {
            "price": tx_stats.get("price"),
            "24h": {
                "volume": tx_stats.get("24h", {}).get("volume"),
                "buyers": tx_stats.get("24h", {}).get("buyers"),
                "sellers": tx_stats.get("24h", {}).get("sellers"),
                "buy_volume": tx_stats.get("24h", {}).get("buy_volume"),
                "sell_volume": tx_stats.get("24h", {}).get("sell_volume"),
            },
            "1h": {
                "volume": tx_stats.get("1h", {}).get("volume"),
                "buyers": tx_stats.get("1h", {}).get("buyers"),
                "sellers": tx_stats.get("1h", {}).get("sellers"),
            }
        }
    
    # 2. TRUMP 安全审计
    print("Fetching TRUMP security audit...", file=sys.stderr)
    security = fetch_trump_security()
    if "error" not in security:
        output["data"]["trump_security"] = {
            "safe": security.get("safe"),
            "risk_count": security.get("risk_count"),
            "warn_count": security.get("warn_count"),
            "high_risk": security.get("high_risk"),
            "buy_tax": security.get("buy_tax"),
            "sell_tax": security.get("sell_tax"),
            "freeze_auth": security.get("freeze_auth"),
            "mint_auth": security.get("mint_auth"),
        }
    
    # 3. 投资组合价格
    print("Fetching portfolio prices...", file=sys.stderr)
    portfolio = fetch_portfolio_prices()
    if "error" not in portfolio:
        output["data"]["portfolio"] = portfolio.get("tokens", [])
    
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
