import requests
from requests import get
import json
import pandas as pd

API_KEY = "E"
BASE_URL = "https://api.etherscan.io/api"
contract_address = "0x"
ETHER_VALUE = 10 ** 18

#address_url = f"https://api.etherscan.io/api?module=account&action=balance&address=0x7eFA3cA268c9f1b7399FbCb5F096aaae980f2dFa&tag=latest&apikey=E1K45DSD27EC2U1AK1YKQZVXE32DCTFF5J"

# Set the starting block number to retrieve data from
block_number = 0

# Create an empty list to store the data
data = []

def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url
# Loop over blocks and retrieve data
while True:
    # Define the API parameters for retrieving the list of token holders
    params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": contract_address,
        "tag": "latest",
        "apikey": api_key,
        "startblock": block_number
    }

    # Make the API request and retrieve the response

    response = requests.get(address_url, params=params)
    print(response.text)
    if response.text.strip():
        response_data = json.loads(response.text)
        # rest of the code
    else:
        print("Empty response received")
    response_data = json.loads(response.text)

    # Check if the response was successful and retrieve the list of token holders
    if response_data["status"] == "1":
        for holder in response_data["result"]:
            # Add the holder's address and balance to the list of data
            data.append({
                "address": holder["account"],
                "balance": int(holder["balance"])
            })

        # If the response contained less than 10,000 results, it means we've retrieved all the data
        if len(response_data["result"]) < 10000:
            break

        # Set the block number to the next one to retrieve more data
        block_number = int(response_data["result"][-1]["blockNumber"]) + 1
    else:
        # If the response was not successful, print the error message and stop the program
        print(f"Error retrieving data: {response_data['message']}")
        break

# Convert the list of data into a Pandas DataFrame for easier manipulation and sorting
df = pd.DataFrame(data)

# Group the data by address and sum the balances to get the total holdings value for each address
grouped = df.groupby("address")["balance"].sum()

# Sort the data by total holdings value in descending order
sorted_data = grouped.sort_values(ascending=False).reset_index()

# Print the top 10 holders by total holdings value
print(sorted_data.head(10))
