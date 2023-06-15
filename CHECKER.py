import asyncio
from web3 import Web3

# Local file path containing addresses (one address per line)
file_path = r"C:\Users\oluwa\OneDrive\Documents\my files\public keys.txt"

# Dictionary of network RPC URLs
network_rpc_urls = {
    "Ethereum": "https://eth.llamarpc.com",
    "Matic": "https://polygon.llamarpc.com",
    "BNB": "https://rpc.ankr.com/bsc",
    "Fantom": "https://rpcapi.fantom.network",
    "Kava": "https://evm.kava.io",
}

# Output file path for saving addresses with non-zero balances
output_file = r"C:\Users\oluwa\OneDrive\Documents\my files\nonzero.txt"

# Function to read addresses from a local file
def read_addresses(file_path):
    addresses = []
    with open(file_path, "r") as file:
        for line in file:
            address = line.strip()
            if address:
                addresses.append(address)
    return addresses

# Function to write addresses with non-zero balances to a file
def write_balances_to_file(output_file, addresses):
    with open(output_file, "a") as file:
        for address in addresses:
            file.write(f"Address: {address}\n")

# Function to check balance on a specific network
async def check_balance(network_rpc_url, network_name, addresses_batch):
    w3 = Web3(Web3.HTTPProvider(network_rpc_url))
    balances = []
    for address in addresses_batch:
        balance_wei = w3.eth.get_balance(address)
        balance = w3.from_wei(balance_wei, 'ether')
        balances.append(balance)

    # Get addresses with non-zero balance
    addresses_with_balance = [address for i, balance in enumerate(balances) if balance > 0]

    # Save addresses with non-zero balance to the output file
    write_balances_to_file(output_file, addresses_with_balance)

# Read addresses from the local file
addresses = read_addresses(file_path)

# Batch addresses into groups of 10 for batch processing
batch_size = 10
address_batches = [addresses[i:i + batch_size] for i in range(0, len(addresses), batch_size)]

# Check balances on different networks asynchronously
async def check_balances_async():
    tasks = []
    for network_name, rpc_url in network_rpc_urls.items():
        for address_batch in address_batches:
            tasks.append(check_balance(rpc_url, network_name, address_batch))
    await asyncio.gather(*tasks)

# Run the asynchronous balance checking
asyncio.run(check_balances_async())
