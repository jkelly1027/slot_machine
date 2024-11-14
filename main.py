# Modules
import random

# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

# Dimensions of slot machine
ROWS = 3
COLS = 3

# Symbols within each column/reel | How many times each symbol appears/rarity
symbol_count = {
    "A" : 2,
    "B" : 4,
    "C" : 6,
    "D" : 8
}

# Value = Multiplier
symbol_value = {
    "A" : 5,
    "B" : 4,
    "C" : 3,
    "D" : 2
}

# Get user Deposit
def Deposit():
    
    # Continually ask until valid amount entered
    while True:
        amount = input("Deposit Amount: \n")

        # Need to check if user entered a valid whole number amount greater than 0
        if amount.isdigit():
            amount = int(amount)
            
            if amount > 0:
                # Valid!
                break
            else:
                print("Amount must be greater than 0! \n")
        else:
            print("Please enter a valid amount! \n")

    return amount

# Get user bet amount | How many lines they want to bet on | Amount X Lines
def Lines():
    
    # Continually ask until valid amount entered
    while True:
        lines = input("Lines to bet on: (1-" + str(MAX_LINES) + ") \n")

        # Need to check if user entered a valid number of lines
        if lines.isdigit():
            lines = int(lines)
            
            # Check lines is 1 or greater and less than or equal to the max number of lines
            if 1 <= lines <= MAX_LINES:
                # Valid!
                break
            else:
                print("Enter valid number of lines! \n")
        else:
            print("Please enter a valid number! \n")

    return lines

# Get user bet amount
def Get_bet():
    
    # Continually ask until valid amount entered
    while True:
        amount = input("Bet Amount (Per Line): \n")

        # Need to check if user entered a valid bet amount
        if amount.isdigit():
            amount = int(amount)
            
            # Check if amount is between the max/min bet size
            if MIN_BET <= amount <= MAX_BET:
                # Valid!
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}. \n")
        else:
            print("Please enter a valid number! \n")

    return amount

# Multiple bet amount by number of lines to bet on:
def Total_bet(bet_amount, lines):
    total = bet_amount * lines

    return total

# Determine the outcome of the slot machine
def Slot_spin(rows, cols, symbols):
    
    # Generate what symbols will be in each column based on frequency of symbols in dictionary.
    # Need to randomly pick the number of rows in each column
    # Create list of all possible values we could select, then randomly choose three of those values (3 in each row)
    # Choose a value, remove it from the list, do it again...
    # .items() gives you the key and the value associated with a dictionary
    # _ (Anonymous variable): Dont care about the iteration value

    all_symbols = []

    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol) # Example: Will add A 2 times

    # Now need to select what values go in every single column
    columns = []

    # For each column we have we need to generate values to populate them. (Number of values generated = number of rows we have)
    # Will need to create a copy of all_symbols as we will be removing items from this list
    
    for _ in range(cols): # Generate a column for the amount of columns we want (cols = 3)
        column = []
        # Copy a list
        current_symbols = all_symbols[:]
        # This code is then picking random values for each row in our column
        # We have a column, we have the current symbols that we can select from
        for _ in range(rows): # Then we loop through the number of values we need to generate (rows)
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            # Then want to add this value to our column
            column.append(value)

        # Append our current column
        columns.append(column)

    return columns

# Print the Slot Machine
def Print_Machine(columns):
    # Our columns currently look like rows, we need to flip them around
    for row in range(len(columns[0])):
        for i, column in enumerate(columns): # 
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        
        # Will bring us to new line after every row
        print()

# Check whether user won or not | What there bet is | Which lines they bet on:
def Check_Win(columns, lines, bet, values):
    
    # Need to check that every symbol in line/row is the same.

    winnings = 0
    winning_lines = []

    # Need to look through only the rows the user bet on
    # If they bet on one line loop will only look at 0-1 not inclusive of 1, 2 lines 0-2, so lines 0-1...
    for line in range(lines):

        symbol = columns[0][line] # Gives us the first symbol of each line/row we check | Looking at column 0 row x of the machine

        # Knowing what the symbols is in the first column of the row we now loop through the other columns of the row
        for column in columns:
            # Check the symbol in the current column of row x
            symbol_to_check = column[line]
            # If the symbol doesn't match, stop checking, dont update winnings, move to next line if there is one
            if symbol != symbol_to_check:
                break
        else:
            # All symbols match, update winnings | Symbol multiplier x Bet on that specific line (not total bet)
            winnings += values[symbol] * bet
            # What line(s) user won on
            winning_lines.append(line + 1)

    return winnings, winning_lines

# Run an instance of the slot machine
def Spin(balance):

    # Get the number of lines to bet on:
    line = Lines()

    while True:

        # Get the users bet amount:
        bet_amount = Get_bet()

        # Get total bet amount
        total = Total_bet(bet_amount, line)

        if total > balance:
            print(f"Insufficient funds to bet that amount (${total}) | Current Balance: ${balance}")
        else:
            break

    # Inform user of current bet:
    print(f"\nBet Status: ${bet_amount} on {line} line(s)")
    print(f"Total bet amount: ${total}\n")

    slots = Slot_spin(ROWS, COLS, symbol_count)
    Print_Machine(slots)

    # Display User Winning
    winnings, winning_lines = Check_Win(slots, line, bet_amount, symbol_value)
    print(f"\nYOU WON ${winnings}!!!")
    print(f"You won on line(s): ", *winning_lines) # * unpacks the list

    return winnings - total

# Main Function
def main():
    
    # Get user initial deposit:
    balance = Deposit()

    while True:
        print(f"Current Balance: ${balance}\n")
        answer = input("Press Enter to spin! (q to Quit)\n")

        if answer == "q":
            break
        
        # Spin the slot machine!
        balance += Spin(balance)

    print(f"Final Balance: ${balance}\n")
    
# Call main()    
main()