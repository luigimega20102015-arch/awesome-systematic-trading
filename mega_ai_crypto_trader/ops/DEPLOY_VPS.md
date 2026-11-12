# Deploy on VPS — Binance PAPER only

This deployment has passed offline unit tests but **has not yet been started on a real VPS or tested inside the Freqtrade Docker container**.

Requirements: Ubuntu LTS VPS, Docker Engine with Compose plugin, suggested 2 vCPU / 2–4 GB RAM / 20–30 GB SSD, SSH key authentication. Ensure Binance market-data endpoints are accessible in your region.

## Setup
Clone the fork and checkout the branch `mega-ai-crypto-trader-paper-v0`.
From the repository root:

```bash
cd mega_ai_crypto_trader/ops
docker compose config
docker compose pull
mkdir -p ../user_data/data ../user_data/logs
# Make sure UID 1000 can write user_data on the VPS.
docker compose run --rm --entrypoint freqtrade freqtrade download-data --exchange binance --pairs BTC/USDT ETH/USDT --timeframes 15m --days 90 --datadir /freqtrade/user_data/data
docker compose run --rm --entrypoint freqtrade freqtrade backtesting --config /freqtrade/config_paper.json --strategy MegaBaselinePaper --datadir /freqtrade/user_data/data
docker compose up -d
docker compose ps
docker compose logs --tail 100 freqtrade
```

Manual download/backtest commands use an explicit `--entrypoint freqtrade` bypass for non-trading tasks. Never replace them with a live trading command or another config. **The default `docker compose up -d` path invokes the PAPER-only guard.**

Stop with `docker compose down`. Data persists in `user_data/`. Run tests from the `mega_ai_crypto_trader` folder with `python -m unittest discover -s tests -v`.

Important: strategy is unvalidated; simulated 3% stops are not orders on exchange, gaps/slippage may increase risk. The guard is not a security boundary against a VPS operator altering Docker configuration. No remote UI/API is exposed. Never add private API credentials or enable live trading.

Official Docker guide: https://www.freqtrade.io/en/2026.8/docker_quickstart/
