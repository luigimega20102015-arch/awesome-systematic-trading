"""Offline-only crypto paper risk engine; no exchange connectivity."""
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_DOWN
from typing import Dict

D = Decimal

@dataclass(frozen=True)
class Config:
    initial_equity: Decimal = D("500")
    risk_per_trade: Decimal = D("0.01")
    max_positions: int = 5
    max_total_risk: Decimal = D("0.05")
    fee_rate: Decimal = D("0.001")
    daily_loss_limit: Decimal = D("0.02")
    min_notional: Decimal = D("10")
    paper_only: bool = True

@dataclass(frozen=True)
class Position:
    symbol: str
    entry: Decimal
    stop: Decimal
    quantity: Decimal
    reserved_risk: Decimal

@dataclass
class PaperEngine:
    config: Config = field(default_factory=Config)
    cash: Decimal = field(init=False)
    day_start_equity: Decimal = field(init=False)
    realized_pnl: Decimal = D("0")
    positions: Dict[str, Position] = field(default_factory=dict)

    def __post_init__(self):
        if not self.config.paper_only:
            raise ValueError("Live trading deliberately disabled")
        self.cash = self.config.initial_equity
        self.day_start_equity = self.config.initial_equity

    def equity(self, prices=None):
        prices = prices or {}
        return self.cash + sum((p.quantity * D(str(prices.get(s, p.entry))) for s,p in self.positions.items()), D("0"))

    def open_long(self, symbol, entry, stop):
        entry, stop = D(str(entry)), D(str(stop))
        if entry <= 0 or stop <= 0 or stop >= entry:
            raise ValueError("Long stop must be positive and below entry")
        if symbol in self.positions or len(self.positions) >= self.config.max_positions:
            return None
        if self.realized_pnl <= -self.day_start_equity * self.config.daily_loss_limit:
            return None
        equity = self.equity()
        reserved = sum((p.reserved_risk for p in self.positions.values()), D("0"))
        # Conservative headroom for fees reducing equity during entry.
        total_budget = equity * (D("1") - self.config.fee_rate) * self.config.max_total_risk
        budget = min(equity * self.config.risk_per_trade, max(D("0"), total_budget - reserved))
        unit_loss = entry - stop + (entry + stop) * self.config.fee_rate
        affordable = self.cash / (entry * (D("1") + self.config.fee_rate))
        qty = min(budget / unit_loss, affordable).quantize(D("0.00000001"), rounding=ROUND_DOWN)
        if qty <= 0 or qty * entry < self.config.min_notional:
            return None
        cost = qty * entry * (D("1") + self.config.fee_rate)
        p = Position(symbol, entry, stop, qty, qty * unit_loss)
        self.cash -= cost
        self.positions[symbol] = p
        return p

    def close_long(self, symbol, exit_price):
        p = self.positions.pop(symbol)
        exit_price = D(str(exit_price))
        if exit_price <= 0:
            self.positions[symbol] = p
            raise ValueError("Exit price must be positive")
        proceeds = p.quantity * exit_price * (D("1") - self.config.fee_rate)
        self.cash += proceeds
        pnl = proceeds - p.quantity * p.entry * (D("1") + self.config.fee_rate)
        self.realized_pnl += pnl
        return pnl

    def mark_new_day(self, prices=None):
        self.day_start_equity = self.equity(prices)
        self.realized_pnl = D("0")
