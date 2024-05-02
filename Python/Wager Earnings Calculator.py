import datetime

def record_transaction(deposit, winning, withdrawal):
    # Get today's date
    today = datetime.date.today()
    
    # Record the transaction in a text file
    with open("transactions.txt", "a") as file:
        file.write(f"{today},{deposit},{winning},{withdrawal}\n")

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

def calculate_weekly_earnings():
    total_deposits = 0
    total_withdrawals = 0
    today = datetime.date.today()
    year, week, _ = today.isocalendar()

    # Read transactions from the text file
    with open("transactions.txt", "r") as file:
        for line in file:
            transaction_date, deposit, winning, withdrawal = line.strip().split(",")
            transaction_year, transaction_week, _ = datetime.datetime.strptime(transaction_date, "%Y-%m-%d").isocalendar()
            if transaction_year == year and transaction_week == week:
                total_deposits += float(deposit)
                total_withdrawals += float(withdrawal)

    # Calculate earnings
    earnings = total_withdrawals - total_deposits
    return earnings

def calculate_monthly_earnings():
    total_deposits = 0
    total_withdrawals = 0
    today = datetime.date.today()
    year = today.year
    month = today.month

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
    while True:
        deposit = float(input("Enter deposit amount: "))
        winning = float(input("Enter winning amount: "))
        withdrawal = float(input("Enter withdrawal amount: "))
        record_transaction(deposit, winning, withdrawal)
        print("Transactions recorded successfully!")

        # Calculate today's date
        today = datetime.date.today()

        # Calculate daily earnings for today
        date = today.strftime("%Y-%m-%d")
        daily_earnings = calculate_daily_earnings(date)
        print(f"Earnings for {date}: ${daily_earnings:.2f}")

        # Calculate weekly earnings for the current week
        year, week, _ = today.isocalendar()
        weekly_earnings = calculate_weekly_earnings()
        print(f"Earnings for the current week: ${weekly_earnings:.2f}")

        # Calculate monthly earnings for the current month
        monthly_earnings = calculate_monthly_earnings()
        print(f"Earnings for the current month: ${monthly_earnings:.2f}")

        print("\n1. Record Another Transaction")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "2":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()