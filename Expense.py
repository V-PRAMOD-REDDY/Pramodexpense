import os
import datetime
import streamlit as st

EXPENSES_FILE = "expenses.txt"

def get_expenses():
    try:
        with open(EXPENSES_FILE, "r", encoding="utf-8") as file:
            expenses = file.readlines()
        return [expense.strip() for expense in expenses]
    except FileNotFoundError:
        return []

def save_expense(expense):
    with open(EXPENSES_FILE, "a", encoding="utf-8") as file:
        file.write(f"{expense}\n")

def update_expenses(expenses):
    with open(EXPENSES_FILE, "w", encoding="utf-8") as file:
        for expense in expenses:
            file.write(f"{expense}\n")

def display_expenses():
    expenses = get_expenses()
    if not expenses:
        st.write("No expenses found.")
    else:
        for index, expense in enumerate(expenses, start=1):
            st.write(f"{index}. {expense}")

def main():
    st.title("Pramod Expense Tracker")

    menu = ["Add Expense", "View Expenses", "Delete Expense", "Update Expense"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Expense":
        st.subheader("Add Expense")
        expense_description = st.text_input("Enter expense description")
        amount = st.number_input("Enter amount spent (₹)", min_value=0.0, format="%.2f", value=0.0)
        if st.button("Add Expense"):
            if expense_description and amount > 0:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                expense = f"{timestamp} - {expense_description} - ₹{amount:.2f}"
                save_expense(expense)
                st.success("Expense added successfully!")
            else:
                st.error("Please enter both description and a valid amount.")

    elif choice == "View Expenses":
        st.subheader("Expenses")
        display_expenses()

    elif choice == "Delete Expense":
        st.subheader("Delete Expense")
        expenses = get_expenses()
        if not expenses:
            st.write("No expenses found.")
        else:
            expense_to_delete = st.selectbox("Select expense to delete", expenses)
            if st.button("Delete Expense"):
                expenses.remove(expense_to_delete)
                update_expenses(expenses)
                st.success("Expense deleted successfully!")

    elif choice == "Update Expense":
        st.subheader("Update Expense")
        expenses = get_expenses()
        if not expenses:
            st.write("No expenses found.")
        else:
            expense_to_update = st.selectbox("Select expense to update", expenses)
            if expense_to_update:
                new_description = st.text_input("Enter new description", value=expense_to_update.split(" - ")[1])
                new_amount = st.number_input("Enter new amount spent (₹)", min_value=0.0, format="%.2f", value=float(expense_to_update.split(" - ")[2][1:]))
                if st.button("Update Expense"):
                    timestamp = expense_to_update.split(" - ")[0]
                    updated_expense = f"{timestamp} - {new_description} - ₹{new_amount:.2f}"
                    index = expenses.index(expense_to_update)
                    expenses[index] = updated_expense
                    update_expenses(expenses)
                    st.success("Expense updated successfully!")

if __name__ == "__main__":
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "w", encoding="utf-8"):
            pass
    main()
