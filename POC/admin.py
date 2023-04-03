from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN

ENCODING = 'utf-8'
 
class admin:
    
    def __init__(self, _privateKey, _address, _userName, _registerAddress, _registerABI, _URL):
        
        self.profile = {}
        self.profile['private_key'] = _privateKey
        self.profile['address'] = _address
        self.profile['userName'] = _userName
        self.URL = _URL

        _web3M = Web3(Web3.HTTPProvider(self.URL))
        _RegisterSc = _web3M.eth.contract(address=_registerAddress, abi=_registerABI)
        self.contracts = {}
        self.contracts['marketplace'] = {'Address': _registerAddress, 'ABI': _registerABI, 'web3': _web3M, 'contract': _RegisterSc}
 

    def registerAuditor(self):
        RegisterSc = self.contracts['marketplace']['contract']
        web3M = self.contracts['marketplace']['web3']

        username = self.profile['userName']

        registerAuditor_tx = RegisterSc.functions.registerAuditor().buildTransaction(
        {
            'from': self.profile['address'],
            'nonce': web3M.eth.getTransactionCount(self.profile['address']),
            "gasPrice": web3M.eth.gas_price,
            'chainId': web3M.eth.chain_id,
        }
        )
        tx_create = web3M.eth.account.signTransaction(registerAuditor_tx, self.profile['private_key'])
        tx_hash = web3M.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3M.eth.waitForTransactionReceipt(tx_hash)
        print(f'auditor added: {tx_receipt.gasUsed}')
        print('Auditor is registered')

    def addRegulator(self, regulatorAddress):
        
        RegisterSc = self.contracts['marketplace']['contract']
        web3M = self.contracts['marketplace']['web3']
        username = self.profile['userName']

        
        addRegulator_tx = RegisterSc.functions.addRegulator(regulatorAddress).buildTransaction(
        {
            'from': self.profile['address'],
            'nonce': web3M.eth.getTransactionCount(self.profile['address']),
            "gasPrice": web3M.eth.gas_price,
            'chainId': web3M.eth.chain_id,
        }
        )
        tx_create = web3M.eth.account.signTransaction(addRegulator_tx, self.profile['private_key'])
        tx_hash = web3M.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3M.eth.waitForTransactionReceipt(tx_hash)
        print(f'Add regulator: {tx_receipt.gasUsed}')
        print('Regualor is added')


    def AuditReport(self, buyerAddress, P, V, G, Co, DS, R, time):
        
        RegisterSc = self.contracts['marketplace']['contract']
        web3M = self.contracts['marketplace']['web3']
        username = self.profile['userName']

        AuditReport_tx = RegisterSc.functions.AuditReport(buyerAddress, P, V, G, Co, DS, R, time).buildTransaction(
        {
            'from': self.profile['address'],
            'nonce': web3M.eth.getTransactionCount(self.profile['address']),
            "gasPrice": web3M.eth.gas_price,
            'chainId': web3M.eth.chain_id,
        }
        )
        tx_create = web3M.eth.account.signTransaction(AuditReport_tx, self.profile['private_key'])
        tx_hash = web3M.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3M.eth.waitForTransactionReceipt(tx_hash)
        print(f'Privacy audit submitted: {tx_receipt.gasUsed}')
        print('Privacy audit is submitted')


    def InvestigationReport(self, buyerAddress, time, volume, provider, senstivity, agreements):
        
        RegisterSc = self.contracts['marketplace']['contract']
        web3M = self.contracts['marketplace']['web3']
        username = self.profile['userName']

        InvestigationReport_tx = RegisterSc.functions.InvestigationReport(buyerAddress, time, volume, provider, senstivity, agreements).buildTransaction(
        {
            'from': self.profile['address'],
            'nonce': web3M.eth.getTransactionCount(self.profile['address']),
            "gasPrice": web3M.eth.gas_price,
            'chainId': web3M.eth.chain_id,
        }
        )
        tx_create = web3M.eth.account.signTransaction(InvestigationReport_tx, self.profile['private_key'])
        tx_hash = web3M.eth.sendRawTransaction(tx_create.rawTransaction)
        tx_receipt = web3M.eth.waitForTransactionReceipt(tx_hash)
        print(f'investigation report submitted: {tx_receipt.gasUsed}')
        print('Investigation Report is submitted')