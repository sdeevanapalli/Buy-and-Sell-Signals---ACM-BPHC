Here is the content for your `README.md` file:

```markdown
# Stock Market Strategy Backtesting with SMA Crossover

This project implements a strategy for analyzing and backtesting stock market data using the **Simple Moving Average (SMA)** crossover method. It uses **yfinance** for downloading historical stock data, and **matplotlib** for plotting the results and adding interactivity.

## Features
- Downloads historical stock data from **Yahoo Finance**.
- Preprocesses the data by calculating key technical indicators such as **SMA (50)**, **SMA (200)**, **daily returns**, **log returns**, and more.
- Implements a simple buy/sell strategy based on the SMA crossover.
- Backtests the strategy to evaluate portfolio performance.
- Visualizes the results, including SMA lines and buy/sell signals, with interactive buttons to toggle visibility of plotted elements.

## Getting Started

### Prerequisites
Ensure you have the following libraries installed:
- `matplotlib`
- `numpy`
- `yfinance`
- `python-dotenv` (optional, for loading environment variables)

You can install these using the following command:

```bash
pip install -r requirements.txt
```

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   ```

2. Navigate to the project directory:
   ```bash
   cd yourrepository
   ```

3. Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Define the stock symbol, start date, and end date in the main function (default: NIFTY 50 index):
   ```python
   symbol = '^NSEI'  # NIFTY 50 index
   start_date = '2014-01-01'
   end_date = '2024-01-01'
   ```

2. Run the script:
   ```bash
   python script_name.py
   ```

3. The strategy will:
   - Download the stock data.
   - Preprocess the data to calculate SMA, returns, and other technical indicators.
   - Implement a buy/sell strategy based on the SMA crossover.
   - Backtest the strategy and print out performance metrics like annual return, Sharpe ratio, and max drawdown.
   - Plot the results, including SMA lines, stock prices, and buy/sell signals.

### Interactivity
You can toggle the visibility of the following elements in the plot:
- **50-Day SMA**
- **200-Day SMA**
- **Buy/Sell Signals**

Buttons will appear in the plot window to enable or disable these features.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

You can copy and paste this content into a `README.md` file for your project!
