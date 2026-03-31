# 📈 Trading Alpha Utils

High-performance technical analysis indicators and backtesting utilities for Python.

![Python](https://img.shields.io/badge/python-3.9+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **High-Performance Indicators**: Implementation of SMA, EMA, RSI, MACD, Bollinger Bands, and VWAP using NumPy/Pandas.
- **Lightweight Backtester**: Vectorized strategy validation engine with performance metrics (Sharpe Ratio, Max Drawdown).
- **Extensible Architecture**: Easy to add custom indicators and strategies.

## 🚀 Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the demo:
   ```bash
   python -m src.main --demo
   ```

## 📊 Strategy Example

```python
def golden_cross_signal(df):
    signals = pd.Series(0, index=df.index)
    signals[df['sma_50'] > df['sma_200']] = 1
    signals[df['sma_50'] < df['sma_200']] = -1
    return signals
```

## 📜 License

MIT License — see [LICENSE](LICENSE)

---
Built with 🧠 by [DinhLucent](https://github.com/DinhLucent)
