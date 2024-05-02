import datetime

def record_transaction(deposit, winning, withdrawal):
    # Get today's date
    today = datetime.date.today()
    
    # Record the transaction in a text file
    with open("transactions.txt", "a") as file:
        file.write(f"{today},{deposit},{winning},{withdrawal}\n")

def main():
    # Get user input for today's transactions
    deposit = float(input("Enter deposit amount: "))
    winning = float(input("Enter winning amount: "))
    withdrawal = float(input("Enter withdrawal amount: "))

    # Record the transactions
    record_transaction(deposit, winning, withdrawal)
    print("Transactions recorded successfully!")

if __name__ == "__main__":
    main()