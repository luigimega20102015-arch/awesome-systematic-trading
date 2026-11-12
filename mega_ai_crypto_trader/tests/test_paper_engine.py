import unittest
from decimal import Decimal as D
from paper_engine import Config, PaperEngine

class PaperEngineTests(unittest.TestCase):
    def test_defaults(self):
        e=PaperEngine()
        self.assertEqual(e.cash,D("500"))
        self.assertEqual(e.config.max_positions,5)
        self.assertEqual(e.config.risk_per_trade,D("0.01"))
    def test_no_live(self):
        with self.assertRaises(ValueError): PaperEngine(Config(paper_only=False))
    def test_invalid_stop(self):
        with self.assertRaises(ValueError): PaperEngine().open_long("BTC",100,100)
    def test_fee_aware_risk(self):
        e=PaperEngine()
        p=e.open_long("BTC",100,95)
        self.assertIsNotNone(p)
        self.assertLessEqual(p.reserved_risk,D("5"))
        self.assertGreaterEqual(e.cash,D("0"))
    def test_max_five(self):
        e=PaperEngine()
        for i in range(5): self.assertIsNotNone(e.open_long(f"C{i}",10,9))
        self.assertIsNone(e.open_long("C5",10,9))
    def test_aggregate_risk(self):
        e=PaperEngine()
        for i in range(5): e.open_long(f"C{i}",10,9)
        self.assertLessEqual(sum(p.reserved_risk for p in e.positions.values()),e.equity()*e.config.max_total_risk)
    def test_duplicate_symbol(self):
        e=PaperEngine()
        self.assertIsNotNone(e.open_long("BTC",100,95))
        self.assertIsNone(e.open_long("BTC",100,95))
    def test_close_fee_pnl(self):
        e=PaperEngine()
        p=e.open_long("BTC",100,95)
        pnl=e.close_long("BTC",110)
        self.assertEqual(pnl,p.quantity*(D("110")*D("0.999")-D("100")*D("1.001")))
    def test_daily_breaker(self):
        e=PaperEngine()
        e.realized_pnl=D("-10")
        self.assertIsNone(e.open_long("BTC",100,95))
    def test_small_account(self):
        e=PaperEngine(Config(initial_equity=D("5")))
        self.assertIsNone(e.open_long("BTC",100,95))
if __name__=="__main__": unittest.main()
