import solcx
from solcx import get_solc_version, set_solc_version
from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN


ENCODING = 'utf-8'

set_solc_version('v0.8.9')

class user:
    def __init__(self, _privateKey, _address, _UserName, _role, _registerAddress, _registerABI, _URL):
        self.profile = {}
        self.profile['private_key'] = _privateKey
        self.profile['address'] = _address
        self.profile['UserName'] = _UserName
        self.profile['Role'] = _role
        self.marketplaceURL = _URL

        _web3M = Web3(Web3.HTTPProvider(self.marketplaceURL))
        
        _RegisterSc = _web3M.eth.contract(address=_registerAddress, abi=_registerABI)
        
        self.contracts = {}
        self.contracts['marketplace'] = {'Address': _registerAddress, 'ABI': _registerABI, 'web3': _web3M, 'contract': _RegisterSc}
 

    def createProfileinMarketplace(self):
        
        RegisterSc = self.contracts['marketplace']['contract']
        web3 = self.contracts['marketplace']['web3']

        username = self.profile['UserName']
        registerUser_tx = RegisterSc.functions.registerUser(self.profile['Role'], 100000000).buildTransaction(
        {
            'from': self.profile['address'],
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.getTransactionCount(self.profile['address']),
            'chainId': web3.eth.chain_id,
        }
        )
        tx_create = web3.eth.account.signTransaction(registerUser_tx, self.profile['private_key'])
        tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        logs = RegisterSc.events.logID().processReceipt(tx_receipt, errors=DISCARD)
        #self.profile['UserID'] = Web3.toHex(logs[0]['args'][''])
        print(f'{username} registered: {tx_receipt.gasUsed}')
        print(f'{username} is registered in Marketplace')

        #return self.profile['UserName']
  

    def deploySubscriptionSc(self, _buyer):  ##pass buyer's address

        #RegisterSc = self.contracts['application']['contract']
        web3 = self.contracts['marketplace']['web3']
        
        username = self.profile['UserName']
        subscription_file = solcx.compile_files('SubscriptionSc.sol')
        abiSubscription = subscription_file['SubscriptionSc.sol:SubscriptionSc']['abi']
        bytecodeSubscription = subscription_file['SubscriptionSc.sol:SubscriptionSc']['bin']
        subscription = web3.eth.contract(abi=abiSubscription, bytecode=bytecodeSubscription)


        seller = self.profile["address"]
        buyer = _buyer

        # Build Constructor Tx
        construct_txn = subscription.constructor(seller, buyer).buildTransaction(
        {
            'gasPrice': web3.eth.gas_price,  
            'from': self.profile['address'],
            'nonce': web3.eth.getTransactionCount(self.profile['address']),
            'chainId': web3.eth.chain_id,
        }
        )
        tx_create = web3.eth.account.signTransaction(construct_txn, self.profile['private_key'])

        tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        gasUsed = tx_receipt
        print(f'{username} deploy subscriptionSc: {tx_receipt.gasUsed}')
        print(f'-> [{username}]: Data-Seller deploys SubscriptionSc address: { tx_receipt.contractAddress }')
        return tx_receipt.contractAddress, abiSubscription, tx_receipt.gasUsed


    def registerAgreement(self, _subscriptionAddress, _subscriptionABI):
    
        RegisterSc = self.contracts['marketplace']['contract']
        web3 = self.contracts['marketplace']['web3']

        username = self.profile['UserName']
        registerAgreement_tx = RegisterSc.functions.registerAgreement(_subscriptionAddress).buildTransaction(
        {
            'from': self.profile['address'],
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.getTransactionCount(self.profile['address']),
            'chainId': web3.eth.chain_id,
        }
        )
        tx_create = web3.eth.account.signTransaction(registerAgreement_tx, self.profile['private_key'])
        tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = RegisterSc.events.logID().processReceipt(tx_receipt, errors=DISCARD)
        self.AID = Web3.toHex(logs[0]['args'][''])
        print(f'-> [{username}]: registers contract in the marketplace')
        
        subscriptionSc = web3.eth.contract(address=_subscriptionAddress, abi=_subscriptionABI)
        self.AgreementList = {self.AID: {'subscriptionSc': subscriptionSc, 'address': _subscriptionAddress, 'ABI': _subscriptionABI,'subscriptionList': []}}
        print(f'{username}: registers contract: {tx_receipt.gasUsed}')        
        return self.AID, tx_receipt.gasUsed


    def addSubscription(self, _AID, _time, _datatype, _interval, _period, _age, _samples, _dim, _price, _resell):
    
        web3 = self.contracts['marketplace']['web3']

        username = self.profile['UserName']

        SubscriptionSc = self.AgreementList[_AID]['subscriptionSc']
        addS_tx = SubscriptionSc.functions.addSubscription(_time, _datatype, _interval, _period, _age, _samples, _dim, _price, _resell).buildTransaction(
        {
            'from': self.profile['address'],
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.getTransactionCount(self.profile['address']),
            'chainId': web3.eth.chain_id,
        }
        )
        tx_create = web3.eth.account.signTransaction(addS_tx, self.profile['private_key'])
        tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)


        logs = SubscriptionSc.events.subscriptionID().processReceipt(tx_receipt, errors=DISCARD)
        SID = Web3.toHex(logs[0]['args'][''])
        print(f'[{username}]: Data-Seller add subscription with ID: {SID}')

        self.AgreementList[_AID]['subscriptionList'].append(SID)        
        print(f'{username} subscription added: {tx_receipt.gasUsed}')
        self.checkSubscriptionStatus(_AID, SID)
        return SID, tx_receipt.gasUsed

    def startSubscription(self, _AID, _SID):
        
        web3 = self.contracts['marketplace']['web3']  

        username = self.profile['UserName']
        SubscriptionSc = self.AgreementList[_AID]['subscriptionSc']
        #SubscriptionSc = web3.eth.contract(address=Subscription_address, abi=abiSubscription)
        startSubscription_tx = SubscriptionSc.functions.startSubscription(_SID).buildTransaction(
        {
            'from': self.profile['address'],
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.getTransactionCount(self.profile['address']),
            'chainId': web3.eth.chain_id,
        }
        )
        tx_create = web3.eth.account.signTransaction(startSubscription_tx, self.profile['private_key'])
        tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        logs = SubscriptionSc.events.subscriptionStatus().processReceipt(tx_receipt, errors=DISCARD)
        status = logs[0]['args']['']

        print(f'[{username}]: Starts the subscription')
        print(f'{username} subscription started: {tx_receipt.gasUsed}')        
        self.checkSubscriptionStatus(_AID, _SID)
        return tx_receipt.gasUsed
    
    def confirmDelivery(self, _AID, _SID):
        RegisterSc = self.contracts['marketplace']['contract']
        web3 = self.contracts['marketplace']['web3']

        username = self.profile['UserName']
        confirmDelivery_tx = RegisterSc.functions.confirmDelivery(_AID, _SID).buildTransaction(
        {
            'from': self.profile['address'],
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.getTransactionCount(self.profile['address']),
            'chainId': web3.eth.chain_id,
        }
        )
        tx_create = web3.eth.account.signTransaction(confirmDelivery_tx, self.profile['private_key'])
        tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        print(f'subscription confirm delivery: {tx_receipt.gasUsed}')
        print(f'-> [{username}]: confirm delivery in the marketplace that automatically triggers the payment settlement')
		
        return tx_receipt.gasUsed
		

    def checkSubscriptionStatus(self, _AID, _SID):

        SubscriptionSc = self.AgreementList[_AID]['subscriptionSc']
        #SubscriptionSc = web3.eth.contract(address=Subscription_address, abi=abiSubscription)
        subscriptionsStatus = SubscriptionSc.functions.getSubscriptionbyID(_SID).call()
        print(f'-> Subscription status : {subscriptionsStatus[2]}')
        paymentStatus = SubscriptionSc.functions.paymentStatus(_SID).call({'from': self.profile['address']})
        print(f'-> Payment status : {paymentStatus}')