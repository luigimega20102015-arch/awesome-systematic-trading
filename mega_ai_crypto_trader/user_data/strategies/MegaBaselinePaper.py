"""Unvalidated baseline for Binance spot dry-run only. Do not use live."""
from datetime import datetime
from pandas import DataFrame
from freqtrade.strategy import IStrategy


class MegaBaselinePaper(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "15m"
    can_short = False
    minimal_roi = {"0": 0.04, "120": 0.02, "360": 0.01}
    stoploss = -0.03
    trailing_stop = False
    process_only_new_candles = True
    startup_candle_count = 50
    use_exit_signal = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema12"] = dataframe["close"].ewm(span=12, adjust=False).mean()
        dataframe["ema26"] = dataframe["close"].ewm(span=26, adjust=False).mean()
        dataframe["volume_ma20"] = dataframe["volume"].rolling(20).mean()
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        cross = (
            (dataframe["ema12"] > dataframe["ema26"])
            & (dataframe["ema12"].shift(1) <= dataframe["ema26"].shift(1))
        )
        dataframe.loc[
            cross & (dataframe["volume"] > dataframe["volume_ma20"]) & (dataframe["volume"] > 0),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["ema12"] < dataframe["ema26"])
            & (dataframe["ema12"].shift(1) >= dataframe["ema26"].shift(1)),
            "exit_long",
        ] = 1
        return dataframe
