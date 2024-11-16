import sys
from aptos_sdk.account import Account
from aptos_sdk.client import FaucetClient, RestClient

# Set up Aptos environment
NODE_URL = "https://fullnode.devnet.aptoslabs.com"
FAUCET_URL = "https://faucet.devnet.aptoslabs.com"

# Initialize clients
rest_client = RestClient(NODE_URL)
faucet_client = FaucetClient(FAUCET_URL, rest_client)

# Replace with the account that deployed the module
MODULE_ADDRESS = "<module_address>"

# Create user accounts
seller = Account.generate()
buyer = Account.generate()

# Fund accounts
faucet_client.fund_account(seller.address(), 100_000_000)
faucet_client.fund_account(buyer.address(), 100_000_000)


def initialize_marketplace():
    """Initialize the marketplace."""
    txn = rest_client.create_transaction(
        sender=seller,
        payload={
            "type": "script_function_payload",
            "function": f"{MODULE_ADDRESS}::Marketplace::initialize",
            "arguments": [],
        },
    )
    rest_client.submit_transaction(txn)
    print("Marketplace initialized!")


def list_item(item_name, price):
    """List an item for sale."""
    txn = rest_client.create_transaction(
        sender=seller,
        payload={
            "type": "script_function_payload",
            "function": f"{MODULE_ADDRESS}::Marketplace::list_item",
            "arguments": [item_name, int(price)],
        },
    )
    rest_client.submit_transaction(txn)
    print(f"Item '{item_name}' listed for {price} coins.")


def buy_item(seller_address, index, price):
    """Buy an item."""
    txn = rest_client.create_transaction(
        sender=buyer,
        payload={
            "type": "script_function_payload",
            "function": f"{MODULE_ADDRESS}::Marketplace::buy_item",
            "arguments": [seller_address, int(index), price],
        },
    )
    rest_client.submit_transaction(txn)
    print("Item purchased!")


def view_listings(seller_address):
    """View all listings."""
    resource = rest_client.get_account_resource(seller_address, f"{MODULE_ADDRESS}::Marketplace::Listings")
    listings = resource["data"]["listings"]
    print("Current Listings:")
    for i, listing in enumerate(listings):
        print(f"{i}. Item: {listing['item']}, Price: {listing['price']}, Seller: {listing['seller']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python marketplace_cli.py <command> [arguments]")
        print("Commands:")
        print("  initialize                Initialize the marketplace")
        print("  list <item_name> <price>  List an item for sale")
        print("  buy <seller_address> <index> <price>  Buy an item")
        print("  view <seller_address>     View all listings")
        return

    command = sys.argv[1].lower()

    if command == "initialize":
        initialize_marketplace()
    elif command == "list" and len(sys.argv) == 4:
        list_item(sys.argv[2], sys.argv[3])
    elif command == "buy" and len(sys.argv) == 5:
        buy_item(sys.argv[2], sys.argv[3], sys.argv[4])
    elif command == "view" and len(sys.argv) == 3:
        view_listings(sys.argv[2])
    else:
        print("Invalid command or arguments. Use `python marketplace_cli.py` for help.")


if __name__ == "__main__":
    main()