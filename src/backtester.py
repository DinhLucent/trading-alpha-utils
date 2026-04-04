import pandas as pd
import numpy as np
from typing import Callable, Dict, Any

class SimpleBacktester:
    """
    A lightweight vectorised backtester for rapid strategy validation.
    """
    
    def __init__(self, data: pd.DataFrame, initial_capital: float = 10000.0):
        self.data = data.copy()
        self.initial_capital = initial_capital
        
    def run_strategy(self, signal_func: Callable[[pd.DataFrame], pd.Series]) -> Dict[str, Any]:
        """
        Executes a strategy described by a signal function.
        signal_func should return a Series of 1 (buy), -1 (sell), or 0 (hold).
        """
        self.data['signal'] = signal_func(self.data)
        # Handle signals: 1 (Buy), -1 (Sell), 0 (Hold)
        # Position is carried forward on 0 signals
        self.data['position'] = self.data['signal'].replace(0, np.nan).ffill().fillna(0)
        
        # Calculate returns
        self.data['market_return'] = self.data['close'].pct_change()
        # Strategy return uses position from previous period (execution at next open/close)
        self.data['strategy_return'] = self.data['position'].shift(1) * self.data['market_return']
        
        # Cumulative returns
        self.data['cum_market_return'] = (1 + self.data['market_return']).cumprod()
        self.data['cum_strategy_return'] = (1 + self.data['strategy_return']).cumprod()
        
        # Performance metrics
        total_return = self.data['cum_strategy_return'].iloc[-1] - 1
        sharpe_ratio = np.sqrt(252) * (self.data['strategy_return'].mean() / self.data['strategy_return'].std())
        max_drawdown = (self.data['cum_strategy_return'].cummax() - self.data['cum_strategy_return']).max()
        
        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'final_value': self.initial_capital * (1 + total_return)
        }
