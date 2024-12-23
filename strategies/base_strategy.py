from abc import ABC, abstractmethod


class TradingStrategy(ABC):
    """
    Baseklasse for trading-strategier.
    """
    @abstractmethod
    def generate_signal(self, candle):
        """
        Genererer et signal baseret på candlestick-data.
        Skal implementeres i underklasser.
        """
        pass