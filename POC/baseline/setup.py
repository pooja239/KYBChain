import solcx
from solcx import get_solc_version, set_solc_version
#from compile import abi, bytecode
from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import random


# If you haven't already installed the Solidity compiler, uncomment the following line
#solcx.install_solc('v0.8.16')

set_solc_version('v0.8.9')

account_from = {
    'private_key': 'de96050609de4b4088375193dd0cf02c3f09ecaf136fb326c71c8f39111a7b1f',
    'address': '0x1656F4E2Dfe9E3a50c499050e79765D9Ff30867a',
}



# Compile contract
register_file = solcx.compile_files('RegisterSc.sol')
subscription_file = solcx.compile_files('SubscriptionSc.sol')

# Export contract data
abiRegister = register_file['RegisterSc.sol:RegisterSc']['abi']
bytecodeRegister = register_file['RegisterSc.sol:RegisterSc']['bin']

abiSubscription = subscription_file['SubscriptionSc.sol:SubscriptionSc']['abi']
bytecodeSubscription = subscription_file['SubscriptionSc.sol:SubscriptionSc']['bin']


def deployRegistercontracts(URL):
    #
    #  -- Deploy RegisterSc Contract --
    #
    web3 = Web3(Web3.HTTPProvider(URL))

    register = web3.eth.contract(abi=abiRegister, bytecode=bytecodeRegister)
    construct_txn = register.constructor().buildTransaction(
    {
        "gasPrice": web3.eth.gas_price,   
        'from': account_from['address'],
        'nonce': web3.eth.getTransactionCount(account_from['address']),
        'chainId': web3.eth.chain_id,
    }
    )
    tx_create = web3.eth.account.signTransaction(construct_txn, account_from['private_key'])
    tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(f'RegisterSc Contract deployed at address: { tx_receipt.contractAddress }')
    register_address = tx_receipt.contractAddress
    RegisterSc = web3.eth.contract(address=register_address, abi=abiRegister)
    print(f'RegisterSc: {tx_receipt.gasUsed}')
    return register_address, abiRegister, tx_receipt.gasUsed