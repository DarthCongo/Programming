import datetime

def calculate_daily_earnings(date):
    total_deposits = 0
    total_withdrawals = 0

    # Read transactions from the text file
    with open("transactions.txt", "r") as file:
        for line in file:
            transaction_date, deposit, winning, withdrawal = line.strip().split(",")
            if transaction_date == date:
                total_deposits += float(deposit)
                total_withdrawals += float(withdrawal)

    # Calculate earnings
    earnings = total_withdrawals - total_deposits
    return earnings

def main():
    # Get today's date
    today = datetime.date.today()
    date = today.strftime("%Y-%m-%d")

    # Calculate daily earnings
    earnings = calculate_daily_earnings(date)
    print(f"Earnings for {date}: ${earnings:.2f}")

if __name__ == "__main__":
    main()