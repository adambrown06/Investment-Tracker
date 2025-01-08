import requests
from datetime import datetime

class StockAPI:
    def __init__(self, api_key):
        # Store the API key and set the base URL for Alpha Vantage API
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    def get_daily_data(self, symbol):
        # Construct the URL for fetching daily stock data
        url = f"{self.base_url}?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={self.api_key}"
        response = requests.get(url)
        
        # Check if the API call was successful
        if response.status_code == 200:
            data = response.json()
            # Verify if daily time series data is available in the response
            if "Time Series (Daily)" in data:
                return data["Time Series (Daily)"]
            else:
                # Raise an error if the expected data is not found
                raise ValueError(f"Invalid response for symbol {symbol}: {data}")
        else:
            # Raise an error if there was an issue with the API request
            raise ConnectionError(f"API request failed with status code {response.status_code}")

class Investment:
    def __init__(self, api_key, name):
        # Initialize with an API instance, name, and data structures for investments
        self.api = StockAPI(api_key)
        self.name = name
        self.investments = []
        self.stock_data = {}
        self.current_values = {}
        self.original_invested = {}

    def add_investment(self, symbol, date, amount):
        # Add an investment, fetch stock data if not already present, and update total invested
        self.investments.append((symbol, date, amount))
        if symbol not in self.stock_data:
            self.stock_data[symbol] = self.api.get_daily_data(symbol)
        if symbol not in self.original_invested:
            self.original_invested[symbol] = 0.0
        self.original_invested[symbol] += amount

    def calculate_investment(self, symbol):
        # Calculate the current value of investments in a specific stock
        if symbol not in self.stock_data:
            raise ValueError(f"No stock data found for symbol {symbol}.")
        stock_data = self.stock_data[symbol]
        total_shares = 0.0
        latest_date = max(stock_data.keys())
        current_price = float(stock_data[latest_date]["4. close"])
        
        # Calculate total shares based on historical investment data
        for inv_symbol, inv_date, inv_amount in self.investments:
            if inv_symbol == symbol:
                if inv_date not in stock_data:
                    raise ValueError(f"No stock price data for {symbol} on {inv_date}")
                price_at_purchase = float(stock_data[inv_date]["4. close"])
                shares = inv_amount / price_at_purchase
                total_shares += shares
        
        # Store the current value of the investment
        current_value = current_price * total_shares
        self.current_values[symbol] = current_value

    def get_total_invested(self):
        # Sum up all original investments
        return sum(self.original_invested.values())

    def get_total_value(self):
        # Sum up all current values of investments
        return sum(self.current_values.values())

    def get_percentage_change(self):
        # Calculate percentage change in investment value
        return ((self.get_total_value() / self.get_total_invested()) * 100) - 100

    def get_monetary_change(self):
        # Calculate monetary increase or decrease in investment
        return self.get_total_value() - self.get_total_invested()

class InputOutput:
    def __init__(self):
        # Initialize with an empty list to hold investment accounts
        self.accounts = []

    def user_input(self):
        # Gather user input for setting up investment accounts
        api_key = input("Please enter API Key: ")
        while True:
            name = input("What would you like to name your investment account? ")
            account = Investment(api_key, name)

            while True:
                symbol = input("Please enter stock symbol you would like to invest in (XXX format): ").upper()
                while True:
                    date = input("Please enter the date of this investment in year-month-day format (xxxx-xx-xx): ")
                    try:
                        datetime.strptime(date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Incorrect format. Please try again.")
                amount = float(input(f"How much did you invest in {symbol} on {date}? "))
                account.add_investment(symbol, date, amount)
                account.calculate_investment(symbol)
                choice = input("Do you have any more investments? (Y/N): ").upper()
                if choice == "N":
                    break

            self.accounts.append(account)
            choice = input("Do you want to add another investment account? (Y/N): ").upper()
            if choice == "N":
                break

    def terminal_output(self):
        # Display the summary of each investment account in the terminal
        for account in self.accounts:
            print(f"\nInvestment Account Summary: {account.name}")
            print("=" * 40)
            print("Original Investments:")
            for symbol, amount in account.original_invested.items():
                print(f"  - {symbol}: ${amount:.2f}")
            print("\nCurrent Values:")
            for symbol, value in account.current_values.items():
                print(f"  - {symbol}: ${value:.2f}")
            print(f"\nTotal Invested: ${account.get_total_invested():.2f}")
            print(f"Total Current Value: ${account.get_total_value():.2f}")
            print(f"Percentage Change: {account.get_percentage_change():.2f}%")
            print(f"Monetary Change: ${account.get_monetary_change():.2f}")
            print("=" * 40)

    def compare_accounts(self):
        # Compare performance across multiple accounts if more than one exists
        max_percentage = None
        max_monetary = None
        best_percentage_account = None
        best_monetary_account = None

        for account in self.accounts:
            percentage_change = account.get_percentage_change()
            monetary_change = account.get_monetary_change()

            if max_percentage is None or percentage_change > max_percentage:
                max_percentage = percentage_change
                best_percentage_account = account.name

            if max_monetary is None or monetary_change > max_monetary:
                max_monetary = monetary_change
                best_monetary_account = account.name

        print("\nComparison of Accounts:")
        print(f"The account with the highest percentage growth is {best_percentage_account} "
              f"with {max_percentage:.2f}%.")
        print(f"The account with the highest monetary growth is {best_monetary_account} "
              f"with ${max_monetary:.2f}.")

    def save_to_file(self):
        # Save singular account summary to a file
        for account in self.accounts:
            filename = f"{account.name}_summary.txt"
            try:
                with open(filename, "w") as file:
                    file.write(f"Investment Account Summary: {account.name}\n")
                    file.write("=" * 40 + "\n")
                    file.write("Original Investments:\n")
                    for symbol, amount in account.original_invested.items():
                        file.write(f"  - {symbol}: ${amount:.2f}\n")
                    file.write("\nCurrent Values:\n")
                    for symbol, value in account.current_values.items():
                        file.write(f"  - {symbol}: ${value:.2f}\n")
                    file.write(f"\nTotal Invested: ${account.get_total_invested():.2f}\n")
                    file.write(f"Total Current Value: ${account.get_total_value():.2f}\n")
                    file.write(f"Percentage Change: {account.get_percentage_change():.2f}%\n")
                    file.write(f"Monetary Change: ${account.get_monetary_change():.2f}\n")
                    file.write("=" * 40 + "\n")
                print(f"Summary for {account.name} saved to {filename}")
            except Exception as e:
                print(f"Error saving to file {filename}: {e}")

    def compare_accounts_to_file(self):
        # Save comparison of accounts to a file if there are more than one account
        filename = "accounts_comparison.txt"

        max_percentage = None
        max_monetary = None
        best_percentage_account = None
        best_monetary_account = None

        try:
            with open(filename, "w") as file:
                for account in self.accounts:
                    percentage_change = account.get_percentage_change()
                    monetary_change = account.get_monetary_change()

                    if max_percentage is None or percentage_change > max_percentage:
                        max_percentage = percentage_change
                        best_percentage_account = account.name

                    if max_monetary is None or monetary_change > max_monetary:
                        max_monetary = monetary_change
                        best_monetary_account = account.name

                    file.write(f"Investment Account Summary: {account.name}\n")
                    file.write("=" * 40 + "\n")
                    file.write("Original Investments:\n")
                    for symbol, amount in account.original_invested.items():
                        file.write(f"  - {symbol}: ${amount:.2f}\n")
                    file.write("\nCurrent Values:\n")
                    for symbol, value in account.current_values.items():
                        file.write(f"  - {symbol}: ${value:.2f}\n")
                    file.write(f"\nTotal Invested: ${account.get_total_invested():.2f}\n")
                    file.write(f"Total Current Value: ${account.get_total_value():.2f}\n")
                    file.write(f"Percentage Change: {account.get_percentage_change():.2f}%\n")
                    file.write(f"Monetary Change: ${account.get_monetary_change():.2f}\n")
                    file.write("=" * 40 + "\n\n")

                file.write("\nComparison of Accounts:\n")
                file.write(f"The account with the highest percentage growth is {best_percentage_account} "
                           f"with {max_percentage:.2f}%.\n")
                file.write(f"The account with the highest monetary growth is {best_monetary_account} "
                           f"with ${max_monetary:.2f}.\n")

            print(f"Comparison saved to {filename}")
        except Exception as e:
            print(f"Error saving to file {filename}: {e}")

# Main execution flow to run the investment tracker
print("\nWelcome to the Investment Tracker!")
user = InputOutput()
print("\nStep 1: Input your investment data.\n")
user.user_input()
print("\nStep 2: Displaying account summaries.")
user.terminal_output()

if len(user.accounts) > 1:
    print("\nStep 3: Comparing accounts.")
    user.compare_accounts()
    print("\nStep 4: Saving account summaries and comparison to a file.")
    user.compare_accounts_to_file()

else:
    print("\nStep 3: Saving account summaries to files.")
    user.save_to_file()

print("\nAll steps completed. Thank you for using the Investment Tracker!")