# What if balance is 0?
# What if balance is in cents?

import random

# Global Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 3,
    "B": 6,
    "C": 9,
    "D": 12
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():                                            # if they type negative number, it will be false
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount


def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{str(MAX_LINES)})? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines


def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${str(MIN_BET)} and ${str(MAX_BET)}.")
        else:
            print("Please enter a number.")
    return amount


def spin(balance):
    lines = get_number_of_lines()

    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won {winnings}.")
    print(f"You won on lines:", *winning_lines)              # "*" splat/unpack operator, will pass every line from winning_lines to print function
    return winnings - total_bet


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


# Generate Slot Machine
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns):                        # Transposing Our Rows From "get_slot_machine_spin" Into Columns
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):            # Enumerate function gives the index and item
            if i != len(columns) - 1:                   # If statement prints visual of columns with space separation except last column
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()


def main():
    balance = deposit()

    while True:
        print(f"Current balance is: ${balance}")
        answer = input("press enter to play (q to quit).")
        if answer == "q":
            break

        if balance == 0:
            print(f"You're current balance is {balance}. Please deposit to play.")
            balance = deposit()

        balance += spin(balance)

    print(f"You left with ${balance}")


main()