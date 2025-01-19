import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Connect to MySQL database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='KINGWOOD',
    database='Housemg'
)
mycursor = mydb.cursor()
print("Database connection successful!")

# Welcome message
name = input("Please enter your name: ")
print(f"\nHi {name}, Welcome to the Home Expenditure Calculator & Management System!\n")

# Input Section
income = int(input('Enter your Monthly Salary: '))
bonus = int(input('Enter your Annual Bonus: '))
electricity = int(input('Enter your Monthly Electricity Expense: '))
food = int(input('Enter your Monthly Food Expense: '))
fuel = int(input('Enter your Monthly Fuel Expense: '))
internet = int(input('Enter your Monthly Internet Expense: '))
rent = int(input('Enter your Monthly Rent: '))
others = int(input('Enter your Monthly Other Expenses: '))

# Calculations
total_expenses = electricity + food + fuel + internet + rent + others
monthly_savings = income - total_expenses
yearly_savings = (monthly_savings * 12) + bonus

# Insert data into MySQL table
sql = """
INSERT INTO customers (name, income, electricity, food, fuel, internet, rent, others, total_expenses, monthly_savings)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
values = (name, income, electricity, food, fuel, internet, rent, others, total_expenses, monthly_savings)
mycursor.execute(sql, values)
mydb.commit()
print("Data inserted successfully!")

# Function Definitions
def plot_expenses():
    """Plot monthly expenses as a bar chart."""
    categories = ['Electricity', 'Food', 'Fuel', 'Internet', 'Rent', 'Others']
    values = [electricity, food, fuel, internet, rent, others]
    plt.figure(figsize=(8, 5))
    plt.bar(categories, values, color='skyblue')
    plt.title('Monthly Expenses Breakdown')
    plt.ylabel('Amount (INR)')
    plt.show()

def calculate_emi():
    """Calculate EMI."""
    p = float(input("Enter Loan Principal Amount: "))
    r = float(input("Enter Monthly Interest Rate (in %): ")) / 100
    n = int(input("Enter Number of Monthly Installments: "))
    emi = p * r * (1 + r)**n / ((1 + r)**n - 1)
    print(f"Your monthly EMI is: {emi:.2f} INR")

def calculate_compound_interest():
    """Calculate compound interest on savings."""
    years = int(input("Enter the number of years for savings: "))
    rate = float(input("Enter the annual interest rate (in %): ")) / 100
    future_value = yearly_savings * (1 + rate)**years
    total_interest = future_value - yearly_savings
    print(f"Future Savings: {future_value:.2f} INR")
    print(f"Total Interest Earned: {total_interest:.2f} INR")
    return future_value, total_interest

def view_history():
    """View expense history from the database."""
    mycursor.execute("SELECT * FROM customers")
    results = mycursor.fetchall()
    for row in results:
        print(row)

def calculate_tax():
    """Calculate yearly tax based on income."""
    yearly_income = (income * 12) + bonus
    print(f"Your Yearly Income: {yearly_income} INR")
    if yearly_income <= 250000:
        tax = 0
    elif yearly_income <= 500000:
        tax = (yearly_income - 250000) * 0.05
    elif yearly_income <= 750000:
        tax = (yearly_income - 500000) * 0.10 + 12500
    elif yearly_income <= 1000000:
        tax = (yearly_income - 750000) * 0.15 + 37500
    elif yearly_income <= 1250000:
        tax = (yearly_income - 1000000) * 0.20 + 75000
    elif yearly_income <= 1500000:
        tax = (yearly_income - 1250000) * 0.25 + 125000
    else:
        tax = (yearly_income - 1500000) * 0.30 + 187500
    print(f"Your Tax Liability: {tax:.2f} INR")

def savings_chart():
    """Show savings and expenses comparison chart."""
    labels = ['Expenses', 'Savings']
    values = [total_expenses * 12, yearly_savings]
    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['tomato', 'gold'])
    plt.title('Yearly Savings vs Expenses')
    plt.show()

# Main Menu
while True:
    print("\nChoose an option:")
    print("1. View Expense Breakdown (Chart)")
    print("2. Calculate EMI")
    print("3. Calculate Compound Interest")
    print("4. View Expense History")
    print("5. Calculate Tax")
    print("6. Compare Savings and Expenses (Pie Chart)")
    print("7. Exit")
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        plot_expenses()
    elif choice == 2:
        calculate_emi()
    elif choice == 3:
        calculate_compound_interest()
    elif choice == 4:
        view_history()
    elif choice == 5:
        calculate_tax()
    elif choice == 6:
        savings_chart()
    elif choice == 7:
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")