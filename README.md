# Investment-Tracker

## Overview

The Investment Tracker is a Python-based application that helps you track, manage, and compare stock investments. It uses the Alpha Vantage API to fetch real-time stock data and provides detailed summaries of original investments, current values, percentage changes, and overall monetary changes.

## Features

- Add multiple investment accounts.
- Track daily stock prices using Alpha Vantage API.
- Calculate the current value of your stock investments.
- Generate a summary of total invested and current values.
- Compare performance across different investment accounts.
- Save account summaries and comparison reports to text files.

## Installation

1. Clone the repository or download the script.

git clone <repo-url>

2. Navigate to the project directory.

cd <directory-name>

3. Install the required dependencies.

pip install requests

## Usage

1. Obtain an API key from Alpha Vantage.

2. Run the script:

python investment_tracker.py

### Input Steps:

- Enter your Alpha Vantage API key.
- Provide a name for your investment account.
- Enter the stock symbol (e.g., AAPL for Apple Inc.).
- Specify the date of investment in YYYY-MM-DD format.
- Enter the amount invested on the specified date.

### Example Flow

Please enter API Key: <YOUR_API_KEY>
What would you like to name your investment account? RetirementFund
Please enter stock symbol you would like to invest in (XXX format): TSLA
Please enter the date of this investment in year-month-day format (xxxx-xx-xx): 2023-05-01
How much did you invest in TSLA on 2023-05-01? 1000
Do you have any more investments? (Y/N): N
Do you want to add another investment account? (Y/N): N

### Output Example:

Investment Account Summary: RetirementFund
========================================
Original Investments:
  - TSLA: $1000.00

Current Values:
  - TSLA: $1500.00

Total Invested: $1000.00
Total Current Value: $1500.00
Percentage Change: 50.00%
Monetary Change: $500.00

## Saving Data

- The application saves individual account summaries to text files in the format: <account_name>_summary.txt.

- If multiple accounts exist, a comparison summary is saved as accounts_comparison.txt.

## Functions

### 1. `StockAPI` Class

- Handles API calls to Alpha Vantage.
  - `get_daily_data(symbol)`: Retrieves daily stock data.

### 2. `Investment` Class

- Manages individual investment accounts.
  - `add_investment(symbol, date, amount)`: Adds investment data.
  - `calculate_investment(symbol)`: Calculates the current value of investments.
  - `get_total_invested()`: Returns total invested amount.
  - `get_total_value()`: Returns current total value.
  - `get_percentage_change()`: Calculates percentage change.
  - `get_monetary_change()`: Calculates monetary change.

### 3. `InputOutput` Class

- Handles user input and output.
  - `user_input()`: Collects investment data from the user.
  - `terminal_output()`: Displays investment summaries.
  - `compare_accounts()`: Compares multiple investment accounts.
  - `save_to_file()`: Saves individual account summaries to text files.
  - `compare_accounts_to_file()`: Saves account comparison summary to a file.

## Error Handling

- If an API request fails, an error message is displayed.
- Ensures valid date formats using `datetime.strptime()`.
- Checks if stock data for the specified date exists.

## API Limitations

- Alpha Vantage imposes API limits. Consider upgrading your API key for higher request rates.

## Future Enhancements

- Support for other financial metrics (e.g., dividends, splits).
- Visualization of stock performance using graphs.
- Export data to CSV format.

## Contributing

Pull requests are welcome. For significant changes, open an issue to discuss proposed changes.

## License

MIT License

## Acknowledgments

- Alpha Vantage for their financial data API.

Happy investing!
Alpha Vantage for their financial data API.

Happy investing!
