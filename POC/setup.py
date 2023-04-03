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
privacyrating_file = solcx.compile_files('privacyRatingSc.sol')
Buyer_file = solcx.compile_files('BuyerSc.sol')
Rule_file = solcx.compile_files('RuleSc.sol')

# Export contract data
abiRegister = register_file['RegisterSc.sol:RegisterSc']['abi']
bytecodeRegister = register_file['RegisterSc.sol:RegisterSc']['bin']

abiSubscription = subscription_file['SubscriptionSc.sol:SubscriptionSc']['abi']
bytecodeSubscription = subscription_file['SubscriptionSc.sol:SubscriptionSc']['bin']

abiPrivacyrating = privacyrating_file['privacyRatingSc.sol:privacyRatingSc']['abi']
bytecodePrivacyrating = privacyrating_file['privacyRatingSc.sol:privacyRatingSc']['bin']

abiBuyer = Buyer_file['BuyerSc.sol:BuyerSc']['abi']
bytecodeBuyer = Buyer_file['BuyerSc.sol:BuyerSc']['bin']

abiRule = Rule_file['RuleSc.sol:RuleSc']['abi']
bytecodeRule = Rule_file['RuleSc.sol:RuleSc']['bin']

def deployRegistercontracts(URL, PR_address):
    #
    #  -- Deploy RegisterSc Contract --
    #
    web3 = Web3(Web3.HTTPProvider(URL))

    register = web3.eth.contract(abi=abiRegister, bytecode=bytecodeRegister)
    construct_txn = register.constructor(PR_address).buildTransaction(
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

def deployRulecontracts(URL):

    #
    #  -- Deploy RuleSc Contract --
    #

    web3 = Web3(Web3.HTTPProvider(URL))

    rule = web3.eth.contract(abi=abiRule, bytecode=bytecodeRule)
    construct_txn = rule.constructor().buildTransaction(
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


    print(f'RuleSc Contract deployed at address: { tx_receipt.contractAddress }')
    Rule_address = tx_receipt.contractAddress
    RuleSc = web3.eth.contract(address=Rule_address, abi=abiRule)
    print(f'RuleSc: {tx_receipt.gasUsed}')
    return Rule_address, abiRule, tx_receipt.gasUsed



def deployPrivacyRatingcontracts(URL, RuleAddress):

    #
    #  -- Deploy PaymentSc Contract --
    #

    web3 = Web3(Web3.HTTPProvider(URL))

    privacyrating = web3.eth.contract(abi=abiPrivacyrating, bytecode=bytecodePrivacyrating)
    construct_txn = privacyrating.constructor(RuleAddress).buildTransaction(
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


    print(f'PrivacyRatingSc Contract deployed at address: { tx_receipt.contractAddress }')
    PrivacyRating_address = tx_receipt.contractAddress
    PrivacyRatingSc = web3.eth.contract(address=PrivacyRating_address, abi=abiPrivacyrating)
    print(f'PrivacyRatingSc: {tx_receipt.gasUsed}')
    return PrivacyRating_address, abiPrivacyrating, tx_receipt.gasUsed

