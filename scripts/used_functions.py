from brownie import accounts,network,config
from web3 import Web3
LOCAL_BLOCKCHAIN=['mainnet-fork']

initialSupply = Web3.toWei(1000000, "ether")

def get_enviroment():
    w3 = Web3(Web3.HTTPProvider("https://eth-rinkeby.alchemyapi.io/v2/" + config["project_id"]))
    return w3


def get_account(index= None , id = None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN:
        account = accounts[0]
        return account
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        return accounts.add(config["wallets"]["from_key"])
    return None

def deployTokens(token,account):
    tokenReturned = token.deploy(initialSupply,{"from":account})
    return tokenReturned

def main():
    get_account()