daily_expense = float(input("Enter daily expense amount: ₹"))
days = int(input("Enter number of days: "))

total_expense = daily_expense * days

print("\n----- Expense Summary -----")
print(f"Daily Expense : ₹{daily_expense:.2f}")
print(f"Number of Days: {days}")
print(f"Total Expense : ₹{total_expense:.2f}")
print("---------------------------")