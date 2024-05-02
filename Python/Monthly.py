import datetime

def calculate_monthly_earnings(year, month):
    total_deposits = 0
    total_withdrawals = 0

    # Read transactions from the text file
    with open("transactions.txt", "r") as file:
        for line in file:
            transaction_date, deposit, winning, withdrawal = line.strip().split(",")
            transaction_year, transaction_month, _ = transaction_date.split("-")
            if int(transaction_year) == year and int(transaction_month) == month:
                total_deposits += float(deposit)
                total_withdrawals += float(withdrawal)

    # Calculate earnings
    earnings = total_withdrawals - total_deposits
    return earnings

def main():
    # Get today's date
    today = datetime.date.today()

    # Calculate the year and month for today's date
    year = today.year
    month = today.month

    # Calculate monthly earnings for the current month
    earnings = calculate_monthly_earnings(year, month)
    print(f"Earnings for {today.strftime('%B %Y')}: ${earnings:.2f}")

if __name__ == "__main__":
    main()