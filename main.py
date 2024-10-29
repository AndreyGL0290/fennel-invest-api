from os import getenv
from dotenv import load_dotenv
from typing import Literal

from fennel_invest_api import Fennel

# Setup an account. Do test runs

def main():
    fennel = Fennel()

    fennel.login(getenv("FENNEL_ACCOUNT_EMAIL")) # Login to the fennel client. It will ask you for the 2FA code
    account_ids = fennel.get_account_ids()
    
    # Places an order for each account_id 
    for account_id in account_ids:
        print(f"Currently serving account: {account_id}")

        side: Literal["buy"] | Literal["sell"] = input("Buy or sell: ").lower()
        while side not in ["buy", "sell"]:
            side = input("Allowed actions are - \"buy\" and \"sell\": ").lower()
        
        stock_to_trade = input("What stock do you want to perform the action on: ").upper()
        isin = fennel.get_stock_isin(ticker=stock_to_trade) # Stocks ISIN number (12 digit number that every registered stock have)
        while not fennel.is_stock_tradable(isin, account_id, side)[0]: # If current stock is not tradable, ask to enter another stock
            while not isin and stock_to_trade != "0": # If current stock is not registered, ask to enter another stock
                print("Stock you are looking for does not exist or is not currently tradable. Enter 0 if you want to skip to the next account")
                stock_to_trade = input("What stock do you want to perform the action on: ").upper()
                isin = fennel.get_stock_isin(ticker=stock_to_trade)
            if stock_to_trade == "0": break
        if stock_to_trade == "0": continue # Continue to the next account
        quantity = input("Enter on how many stocks you want to perform the action: ")
        while type(quantity) is not int:
            quantity = input("Quantity must be an integer: ")

        order = fennel.place_order(account_id=account_id, ticker=stock_to_trade, quantity=quantity, side=side, price="market", dry_run=False) # Places the order
        print(order) # Prints order details
    
    print("All actions on accounts were done successfully. Terminating with status 0")
        

if __name__ == "__main__":
    load_dotenv() # Downloading environmental variables
    
    main()