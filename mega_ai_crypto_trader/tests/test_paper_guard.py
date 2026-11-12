import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("paper_guard", ROOT / "ops" / "paper_guard.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
CONFIG = {
    "dry_run": True, "trading_mode": "spot", "dry_run_wallet": 80,
    "stake_amount": 25, "max_open_trades": 2, "stake_currency": "USDT",
    "exchange": {"name": "binance", "key": "", "secret": "", "pair_whitelist": ["BTC/USDT", "ETH/USDT"]},
    "api_server": {"enabled": False},
}
class GuardTests(unittest.TestCase):
    def test_valid_config(self): self.assertEqual(guard.check(CONFIG, guard.ALLOWED_ARGS), [])
    def test_live_refused(self): self.assertTrue(guard.check({**CONFIG, "dry_run": False}, guard.ALLOWED_ARGS))
    def test_futures_refused(self): self.assertTrue(guard.check({**CONFIG, "trading_mode": "futures"}, guard.ALLOWED_ARGS))
    def test_credentials_refused(self):
        c = json.loads(json.dumps(CONFIG)); c["exchange"]["key"] = "secret"
        self.assertTrue(guard.check(c, guard.ALLOWED_ARGS))
    def test_wrong_command_refused(self): self.assertTrue(guard.check(CONFIG, ["trade", "--config", "live.json"]))
    def test_excess_position_refused(self): self.assertTrue(guard.check({**CONFIG, "max_open_trades": 5}, guard.ALLOWED_ARGS))
    def test_api_enable_refused(self): self.assertTrue(guard.check({**CONFIG, "api_server": {"enabled": True}}, guard.ALLOWED_ARGS))
    def test_wrong_pairs_refused(self):
        c = json.loads(json.dumps(CONFIG)); c["exchange"]["pair_whitelist"].append("SOL/USDT")
        self.assertTrue(guard.check(c, guard.ALLOWED_ARGS))
if __name__ == "__main__": unittest.main()
