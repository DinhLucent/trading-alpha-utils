import logging
import argparse
import pandas as pd
import numpy as np
from src.indicators import Indicators
from src.backtester import SimpleBacktester

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
    parser = argparse.ArgumentParser(description="Trading Alpha Utils CLI")
    parser.add_argument("--demo", action="store_true", help="Run a demo strategy")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    if args.demo:
        logger.info("🎬 Running Alpha Demo Strategy...")
        data = generate_mock_data()
        
        # Calculate indicators
        data['sma_50'] = Indicators.sma(data['close'], 50)
        data['sma_200'] = Indicators.sma(data['close'], 200)
        
        # Simple Golden Cross Strategy
        def golden_cross_signal(df):
            signals = pd.Series(0, index=df.index)
            signals[df['sma_50'] > df['sma_200']] = 1
            signals[df['sma_50'] < df['sma_200']] = -1
            return signals

        backtester = SimpleBacktester(data)
        results = backtester.run_strategy(golden_cross_signal)
        
        logger.info(f"📈 Strategy Results: {results}")
    else:
        logger.info("🚀 Trading Alpha Utils ready. Use --demo to see it in action.")

if __name__ == "__main__":
    main()
