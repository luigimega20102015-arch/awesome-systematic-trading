# MEGA AI Crypto Trader — Phase 0 (PAPER ONLY)

New crypto trading research project, isolated in this folder of the Awesome Systematic Trading fork. This prototype is **not connected to exchanges** and **does not have a validated profitable strategy**.

## Configuration
- Starting virtual capital: **500 USDT**
- Planned stop-loss risk: **1% simulated equity per trade**, initially 5 USDT
- Maximum open positions: **5**
- Planned aggregate stop-loss risk: **5% simulated equity**
- Daily realized-loss entry brake: **2% of opening-day equity**, initially 10 USDT
- Long-only spot simulation; assumed 0.1% fee on entry and exit
- Hardcoded PAPER ONLY; no credentials, no exchange API, no real orders

## Tests
From this directory run:
```bash
python -m unittest discover -s tests -v
```
All 10 tests passed in the local offline development environment before publication.

## Current capabilities
`paper_engine.py` provides virtual cash bookkeeping, stop-distance position sizing with fee-aware budgeting, a cap of five positions, a planned aggregate stop-risk cap and simple realized P&L.

## Major limitations
- Stops are reference prices for sizing, **not automatically executed**. Gaps, costs or slippage can produce larger losses.
- No live prices, historical data, indicator signals, backtesting, Freqtrade installation or orders.
- No persistent state, dry-run service, Telegram, dashboard or crash recovery.
- Daily loss brake currently uses realized, not unrealized, P&L.
- Equity values open positions at entry unless explicit marks are supplied.
- Fee estimate and min notional are illustrative; exchange-specific constraints unverified.

## Next build stages
1. Add historical market data, data-quality checks and fee/slippage models.
2. Evaluate momentum, breakout and mean-reversion benchmarks with walk-forward tests.
3. Integrate Freqtrade in dry-run mode, retaining independent risk checks.
4. Add persistence, portfolio-level mark-to-market limits, logging and Telegram.
5. Consider FreqAI only if it improves out-of-sample net results.

Upstream catalog: https://github.com/paperswithbacktest/awesome-systematic-trading
