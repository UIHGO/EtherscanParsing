import requests
from requests import get
import json
import pandas as pd
import time
headers = {"charset": "utf-8", "Content-Type": "application/x-www-form-urlencoded"}


API_KEY = ""
BASE_URL = "https://api.etherscan.io/api"
contract_address = "0x"
ETHER_VALUE = 10 ** 18


def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url


def get_account_balance(address):
    balance_url = make_api_url("account", "balance", address, tag="latest")
    response = get(balance_url)
    data = response.json()

    value = int(data["result"]) / ETHER_VALUE
    return value


#def get_holders(contract_address):
#    holders_url = make_api_url("token", "tokenholderlist", contract_address)
#    response = get(holders_url)
#    data = response.json()
#    value = data["result"]
#   return value

def get_token_account_balance(holder, contract_address):
    #token_balance_url = make_api_url("account", "balance", holder, contract_address, tag="latest")
    token_balance_url = BASE_URL + f"?module = account&action=tokenbalance&contractaddress={contract_address}&address={holder}&tag=latest&apikey ={API_KEY}"
    headers = {"charset": "utf-8", "Content-Type": "application/x-www-form-urlencoded"}
    response = get(token_balance_url, headers=headers)
    data = response.json()

    value = data["result"]
    print(value)
    return value


holders = pd.read_csv("rufs.csv")


#print(holders['Balance'])
#print(type(holders['HolderAddress']))
#print(type(holders))

token_balance = []
#находим сколько на данном адресе монет данного котракта
#for holder in holders['HolderAddress']:
#        token_balance.append(get_token_account_balance(holder, contract_address))
#        print(token_balance)
#        time.sleep(2)
#holders['Balance'] = token_balance

ethbalance = []
#находим полный баланс аккаунта холдера 'HolderAddress'
for holder in holders['HolderAddress']:
        ethbalance.append(get_account_balance(holder))
        print(ethbalance)
        time.sleep(0.5)
#holders.Balance = ethbalance
holders.Quantity = ethbalance
#print(holders['Balance'])
print(type(holders))

grouped = holders.groupby("HolderAddress")["Quantity"].sum()
sorted_data = grouped.sort_values(ascending=False).reset_index()
print(sorted_data.head(30))

# Convert the list of data into a Pandas DataFrame for easier manipulation and sorting
