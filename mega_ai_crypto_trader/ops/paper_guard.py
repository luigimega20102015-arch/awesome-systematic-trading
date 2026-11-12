"""Fail-closed launcher: refuse live trading or config overrides."""
import json
import os
import sys
from pathlib import Path

ALLOWED_ARGS = [
    "trade", "--config", "/freqtrade/config_paper.json", "--strategy",
    "MegaBaselinePaper", "--db-url", "sqlite:////freqtrade/user_data/trades_paper.sqlite",
]

def check(config, argv):
    problems = []
    if config.get("dry_run") is not True:
        problems.append("dry_run must be true")
    if config.get("trading_mode") != "spot":
        problems.append("spot only")
    if config.get("exchange", {}).get("name") != "binance":
        problems.append("Binance only")
    if config.get("exchange", {}).get("key") or config.get("exchange", {}).get("secret"):
        problems.append("no private exchange credentials")
    if config.get("dry_run_wallet") != 80:
        problems.append("virtual wallet must be 80 USDT")
    if config.get("stake_amount") != 25 or config.get("max_open_trades") != 2:
        problems.append("position allocation changed")
    if config.get("stake_currency") != "USDT":
        problems.append("USDT required")
    if set(config.get("exchange", {}).get("pair_whitelist", [])) != {"BTC/USDT", "ETH/USDT"}:
        problems.append("unexpected pair list")
    if config.get("api_server", {}).get("enabled") is not False:
        problems.append("API server must be disabled")
    if argv != ALLOWED_ARGS:
        problems.append("unapproved command arguments")
    return problems

def main():
    config = json.loads(Path("/freqtrade/config_paper.json").read_text())
    overrides = sorted(k for k in os.environ if k.upper().startswith("FREQTRADE__"))
    errors = check(config, sys.argv[1:])
    if overrides:
        errors.append("Freqtrade config environment overrides forbidden: " + ", ".join(overrides))
    if errors:
        print("PAPER SAFETY GUARD REFUSED START: " + "; ".join(errors), file=sys.stderr)
        return 2
    os.execvp("freqtrade", ["freqtrade", *ALLOWED_ARGS])

if __name__ == "__main__":
    raise SystemExit(main())
