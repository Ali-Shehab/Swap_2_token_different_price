from brownie import  accounts, network,Token1,Token2,Swap,config
from scripts.used_functions import get_account,deployTokens


LOCAL_BLOCKCHAIN = ["ganache-local","development"]
def deploy(TokenA,TokenB):
    account = get_account()
    print("Token deployed")
    print(config['project_id'])
    if (network.show_active() not in LOCAL_BLOCKCHAIN ):
        price_feed_address1 = config['networks'][network.show_active()]['usdc_usd_price_feed'] #'0x8fffffd4afb6115b954bd326cbe7b4ba576818f6'
        price_feed_address2 = config['networks'][network.show_active()]['usdt_usd_price_feed'] #'0x3e7d1eab13ad0104d2750b8863b489d65364e32d'
    myContract = Swap.deploy(TokenA,TokenB,price_feed_address1,price_feed_address2,{"from":account},
                            publish_source=config["networks"][network.show_active()].get("verify"))
    
    return myContract
    
def swap():
    account = get_account()
    TokenA = deployTokens(Token1,account)
    TokenB = deployTokens(Token2,account)
    myContract = deploy(TokenA,TokenB)
    TokenA.transfer(myContract.address,100000 * (10 ** 18))
    TokenB.transfer(myContract.address,100000 * (10 ** 18))

    TokenA.approve(myContract.address,10000 * (10 ** 18),{"from":account})
    TokenB.approve(myContract.address,10000 * (10 ** 18),{"from":account})

    print(TokenA.balanceOf(account.address)/ (10 ** 18))
    print(TokenB.balanceOf(account.address)/ (10 ** 18))
    print("****************Contract***********")
    print(TokenA.balanceOf(myContract.address)/ (10 ** 18))
    print(TokenB.balanceOf(myContract.address)/ (10 ** 18))

    myContract.swap(TokenA,1000 * (10 ** 18),{"from":account})
    print(TokenA.balanceOf(account.address)/ (10 ** 18))
    print(TokenB.balanceOf(account.address)/ (10 ** 18))
    print("****************Contract***********")
    print(TokenA.balanceOf(myContract.address)/ (10 ** 18))
    print(TokenB.balanceOf(myContract.address)/ (10 ** 18))

def main():
    swap()
