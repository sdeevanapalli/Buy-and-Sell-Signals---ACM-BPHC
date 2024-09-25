import matplotlib.pyplot as plt  # For plotting graph
from matplotlib.widgets import Button
import numpy as np  # Numerical Operations
import yfinance as yf  # For Downloading Stock Market Data


# Function to download historical data of last 10 years.
# Error handling included


def download_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error during data download: {e}\nCheck download_data function")
        return None


def preprocess_data(data):
    # Excluding missing values
    data = data.dropna()

    # Adding technical indicators
    # 'Close' for closing price. Calculating mean
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    # Additional Features as mentioned
    data['Daily_Return'] = data['Close'].pct_change()  # Daily Percentage Change
    data['Log_Return'] = np.log(data['Close'] / data['Close'].shift(1))  # Current Day and Previous Day Ratio Log
    data['Lagged_Close'] = data['Close'].shift(1)  # Lagged (previous day's) closing price
    data['Lagged_Log_Return'] = data['Log_Return'].shift(1)  # Lagged log returns

    # Technical indicators as mentioned
    data['Volume_Moving_Average'] = data['Volume'].rolling(window=30).mean()  # 30-day moving average of trading volume
    data['Volatility'] = data['Log_Return'].rolling(window=30).std() * np.sqrt(252)  # 30 day average
    # 252 trading days in a year

    return data


def strategy_dev(data):
    data['Signal'] = 0  # Base Case | Initializing

    # Buy signal
    # When SMA 50 crosses above SMA 200
    data.loc[data['SMA_50'] > data['SMA_200'], 'Signal'] = 1  # Set data['Signal'] to 1

    # Sell signal
    # When SMA 50 crosses below SMA 200
    data.loc[data['SMA_50'] < data['SMA_200'], 'Signal'] = -1  # Set data['Signal'] to -1

    return data


# Function to backtest the strategy
def backtest_strategy(data):
    initial_capital = 100000  # Assuming
    capital = initial_capital  # Initial case
    position = 0  # No of shares

    data['Position'] = 0  # In this function, its signal

    for index, row in data.iterrows():  # iterates through each row in dataFrame
        if row['Signal'] == 1:
            # Buy signal
            position = capital / row['Close']  # Buying as many shares as possible
            capital = 0  # Remaining capital is set to zero
        elif row['Signal'] == -1:
            # Sell signal
            capital = position * row['Close']  # Liquidating as many shares as possible
            position = 0  # No shares left

        data.at[index, 'Position'] = position
        # Updates position with calculated position

    data['Portfolio_Value'] = data['Position'] * data['Close'] + capital
    # Total Portfolio Value

    return data


# Performance Evaluation
def evaluate_performance(data):
    # Calculate metrics
    data['Daily_Return_Portfolio'] = data['Portfolio_Value'].pct_change()  # Daily Change in Percentage
    annual_return = (data['Portfolio_Value'].iloc[-1] / data['Portfolio_Value'].iloc[0]) ** (252 / len(data)) - 1
    sharpe_ratio = data['Daily_Return_Portfolio'].mean() / data['Daily_Return_Portfolio'].std() * (252 ** 0.5)
    max_drawdown = (data['Portfolio_Value'] / data['Portfolio_Value'].cummax() - 1).min()

    print(f"Annual Return: {annual_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")


# Function to visualize the results
def visualize_results(data):
    # Plotting
    global var
    fig, ex = plt.subplots(figsize=[11, 7])  # Size of the plot
    # Alpha is transparency for stock market graph
    plt.plot(data['Close'], label='Close Price', alpha=1, color='darkgrey')
    sma_50, = plt.plot(data['SMA_50'], label='50-Day SMA', linestyle='--', alpha=0.8)
    sma_200, = plt.plot(data['SMA_200'], label='200-Day SMA', linestyle='--', alpha=0.8)

    # Plot buy signals
    buy_signals = plt.plot(data[data['Signal'] == 1].index, data['SMA_50'][data['Signal'] == 1], '^', markersize=8,
                            color='g',
                            label='Buy Signal')

    # Plot sell signals
    sell_signals = plt.plot(data[data['Signal'] == -1].index, data['SMA_50'][data['Signal'] == -1], 'v', markersize=8,
                             color='r',
                             label='Sell Signal')

    plt.title('---SMA Strategy - ACM---')  # Header
    plt.xlabel('Date')  # X axis Label
    plt.ylabel('Price')  # Y axis Label
    plt.legend()

    def on_button_click(label):
        # Toggle the visibility of lines
        if label == 'Toggle 50 SMA':
            sma_50.set_visible(not sma_50.get_visible())
        elif label == 'Toggle 200 SMA':
            sma_200.set_visible(not sma_200.get_visible())
        elif label == 'Toggle Signals':
            buy_signals[0].set_visible(not buy_signals[0].get_visible())
            sell_signals[0].set_visible(not sell_signals[0].get_visible())
        fig.canvas.draw_idle()

    # Create buttons
    button_50_sma_ex = plt.axes([0.91, 0.35, 0.08, 0.05])  # Positioning of button
    button_50_sma = Button(button_50_sma_ex, '50 SMA')
    button_50_sma.on_clicked(lambda event: on_button_click('Toggle 50 SMA'))  # Function if button is clicked

    button_200_sma_ex = plt.axes([0.91, 0.28, 0.08, 0.05])  # Positioning of button
    button_200_sma = Button(button_200_sma_ex, '200 SMA')
    button_200_sma.on_clicked(lambda event: on_button_click('Toggle 200 SMA'))  # Function if button is clicked

    button_toggle_signals_ax = plt.axes([0.91, 0.21, 0.08, 0.05])  # Positioning of button
    button_toggle_signals = Button(button_toggle_signals_ax, 'Signals')
    button_toggle_signals.on_clicked(lambda event: on_button_click("Toggle Signals")) # Function if button is clicked

    plt.show()


var = 1
# Main function
if __name__ == "__main__":
    symbol = '^NSEI'  # NIFTY 50 index
    start_date = '2014-01-01'
    end_date = '2024-01-01'

    # Calling all functions in this main function.

    nifty_data = download_data(symbol, start_date, end_date)
    nifty_data = preprocess_data(nifty_data)
    nifty_data = strategy_dev(nifty_data)
    nifty_data = backtest_strategy(nifty_data)
    evaluate_performance(nifty_data)
    visualize_results(nifty_data)
