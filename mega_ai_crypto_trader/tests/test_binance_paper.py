import io
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from binance_public import get_public_ticker

class FakeResponse:
    def __init__(self, data): self.data = data
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self): return json.dumps(self.data).encode()

class BinancePaperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=json.loads((ROOT/"binance_dryrun.json").read_text())
    def test_dry_run_mandatory(self):
        self.assertIs(self.cfg["dry_run"],True)
    def test_wallet_80(self):
        self.assertEqual(self.cfg["dry_run_wallet"],80)
    def test_spot(self):
        self.assertEqual(self.cfg["trading_mode"],"spot")
    def test_only_two_positions(self):
        self.assertEqual(self.cfg["max_open_trades"],2)
    def test_fixed_stake_25(self):
        self.assertEqual(self.cfg["stake_amount"],25)
    def test_no_exchange_credentials(self):
        self.assertEqual(self.cfg["exchange"]["key"],"")
        self.assertEqual(self.cfg["exchange"]["secret"],"")
    def test_no_automatic_remote_control(self):
        self.assertFalse(self.cfg["api_server"]["enabled"])
    def test_allowed_public_market(self):
        got=get_public_ticker("BTCUSDT",lambda request,timeout: FakeResponse({"symbol":"BTCUSDT","price":"90000.1"}))
        self.assertEqual(got["price"],"90000.1")
    def test_reject_unknown_market(self):
        with self.assertRaises(ValueError): get_public_ticker("DOGEUSDT")
    def test_reject_invalid_ticker(self):
        with self.assertRaises(ValueError): get_public_ticker("BTCUSDT",lambda request,timeout: FakeResponse({"symbol":"BTCUSDT","price":"0"}))
if __name__=="__main__": unittest.main()
