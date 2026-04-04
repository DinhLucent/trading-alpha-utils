import logging
import argparse
import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
from rich import box
from src.indicators import Indicators
from src.backtester import SimpleBacktester

console = Console()

logger = logging.getLogger(__name__)

def generate_mock_data(periods: int = 500) -> pd.DataFrame:
    """Generates synthetic price data for demonstration."""
    date_rng = pd.date_range(start='2023-01-01', periods=periods, freq='D')
    df = pd.DataFrame(date_rng, columns=['date'])
    
    # Random walk
    returns = np.random.normal(0.001, 0.02, periods)
    price = 100 * (1 + returns).cumprod()
    
    df['close'] = price
    df['volume'] = np.random.randint(1000, 10000, periods)
    return df.set_index('date')

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Trading Alpha Utils Demo")
    parser.add_argument("--demo", action="store_true", help="Run strategy demo")
    args = parser.parse_args()

    if args.demo:
        console.print("[bold cyan]🚀 Running Trading Alpha Strategy Demo...[/bold cyan]")
        
        # 1. Generate Synthetic Data
        dates = pd.date_range(start='2023-01-01', periods=500, freq='D')
        data = pd.DataFrame({
            'close': [100 + np.sin(i/10)*10 + np.random.normal(0, 2) for i in range(500)],
            'volume': np.random.randint(1000, 5000, 500)
        }, index=dates)

        # 2. Define Strategies
        def rsi_strategy(df):
            rsi = Indicators.rsi(df['close'], period=14)
            signals = pd.Series(0, index=df.index)
            signals[rsi < 30] = 1   # Oversold -> Buy
            signals[rsi > 70] = -1  # Overbought -> Sell
            return signals

        def sma_cross(df):
            sma_fast = Indicators.sma(df['close'], 20)
            sma_slow = Indicators.sma(df['close'], 50)
            signals = pd.Series(0, index=df.index)
            signals[sma_fast > sma_slow] = 1
            signals[sma_fast < sma_slow] = -1
            return signals

        # 3. Run Backtests
        backtester = SimpleBacktester(data)
        
        results = []
        for name, strategy in [("RSI Mean Reversion", rsi_strategy), ("SMA Trend Following", sma_cross)]:
            res = backtester.run_strategy(strategy)
            res['name'] = name
            results.append(res)

        # 4. Display Results
        table = Table(title="Strategy Performance Comparison", box=box.ROUNDED)
        table.add_column("Strategy", style="cyan")
        table.add_column("Total Return", justify="right")
        table.add_column("Sharpe Ratio", justify="right")
        table.add_column("Max Drawdown", justify="right")
        table.add_column("Final Value", justify="right")

        for r in results:
            table.add_row(
                r['name'],
                f"{r['total_return']:.2%}",
                f"{r['sharpe_ratio']:.2f}",
                f"{r['max_drawdown']:.2%}",
                f"${r['final_value']:,.2f}"
            )

        console.print(table)

if __name__ == "__main__":
    main()
