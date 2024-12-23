from strategies.base_strategy import TradingStrategy

class EngulfingStrategy(TradingStrategy):
    """
    Implementering af en engulfing-mønster-strategi.
    """
    def generate_signal(self, candle):
        bull_cond1 = candle['close'] > candle['open']
        bull_cond2 = candle['close'] > candle['previous_high']
        bull_cond3 = candle['previous_open'] > candle['previous_close']

        bear_cond1 = candle['close'] < candle['open']
        bear_cond2 = candle['close'] < candle['previous_low']
        bear_cond3 = candle['previous_open'] < candle['previous_close']

        if candle['previous_high'] - candle['previous_low'] == 0:
            return None

        special_cond = abs(candle['open'] - candle['close']) / (candle['previous_high'] - candle['previous_low']) >= 1.5

        if bull_cond1 and bull_cond2 and bull_cond3 and special_cond:
            return 'buy'
        elif bear_cond1 and bear_cond2 and bear_cond3 and special_cond:
            return 'sell'
        else:
            return None