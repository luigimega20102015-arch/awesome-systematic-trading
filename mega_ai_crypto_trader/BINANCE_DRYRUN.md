# Binance 80 USDT — DRY RUN ONLY

The user has an indicative $80 real trading budget. **This project is NOT authorized or configured to place real orders.** The existing 500 USDT paper research ledger remains unchanged.

## Proposed small-account profile
- Venue: Binance Spot, pairs BTC/USDT and ETH/USDT
- Simulated wallet: 80 USDT; stake: 25 USDT; max 2 positions (50 USDT allocated, approx 30 USDT spare)
- Baseline stoploss: 3%, about 0.75 USDT price-risk per position before fees, slippage and gaps.
- This is a small-account PAPER experiment, not evidence of profitability.
- The original 1% risk rule translates to ~$0.80/trade for 80 USDT. Fees reduce the available risk budget.
- Real $80 balance may not equal 80 USDT due to exchange rates or conversion.
- Spot only; no leverage, futures, withdrawals or API keys. At this stage do not change dry_run to false.

## Run in an isolated Freqtrade installation
1. Install Freqtrade from its official documentation; check supported Python, Docker and platform versions.
2. Copy `binance_dryrun.json` and the `user_data/strategies/MegaBaselinePaper.py` strategy file into your Freqtrade workspace.
3. Verify exchange permissions, local jurisdiction, Binance market minimums and pair filters. No private API keys are needed.
4. Download OHLCV data and backtest first, e.g. `freqtrade download-data --config binance_dryrun.json --timeframes 15m --days 90` and `freqtrade backtesting --config binance_dryrun.json --strategy MegaBaselinePaper`.
5. Launch **dry-run only** using `freqtrade trade --config binance_dryrun.json --strategy MegaBaselinePaper`. Requires an always-on runtime for unattended service.

The baseline is an EMA12/EMA26 crossover with 20-candle volume filter, 15-minute candles, illustrative ROI and 3% stop. **It is unvalidated.**

### Important safety gaps before any live trading
- Verify order sizes, step sizes and min notional for each Binance market using exchangeInfo.
- Confirm stop-loss-on-exchange behavior and failure handling; Freqtrade spot Binance uses stop-limit, which can remain unfilled in gaps.
- Add real-market fee schedule, persistent database isolation, monitoring, error handling, reconciliation and liquidation prevention (no leverage).
- Test genuine market data, realistic backtests and extended dry-run performance.
- Never put API keys in GitHub; never enable withdrawals.

Read-only public-price smoke test: `python binance_public.py`
Offline unit tests: `python -m unittest discover -s tests -v`.
Official docs: https://docs.freqtrade.io/en/latest/configuration/
