import datetime

def calculate_weekly_earnings(year, week):
    total_deposits = 0
    total_withdrawals = 0

    # Read transactions from the text file
    with open("transactions.txt", "r") as file:
        for line in file:
            transaction_date, deposit, winning, withdrawal = line.strip().split(",")
            transaction_year, transaction_week, _ = transaction_date.split("-")
            if int(transaction_year) == year and int(transaction_week) == week:
                total_deposits += float(deposit)
                total_withdrawals += float(withdrawal)

    # Calculate earnings
    earnings = total_withdrawals - total_deposits
    return earnings

def main():
    # Get today's date
    today = datetime.date.today()

    # Calculate the year and week number for today's date
    year, week, _ = today.isocalendar()

    # Calculate weekly earnings for the current week
    earnings = calculate_weekly_earnings(year, week)
    print(f"Earnings for week {week} of {year}: ${earnings:.2f}")

if __name__ == "__main__":
    main()