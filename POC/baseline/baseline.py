import setup
import solcx
from solcx import get_solc_version, set_solc_version
from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from admin import admin
from user import user

#evoke satoshi inform quantum put various cool afraid joke reduce crumble venue

entityList = {
    "Admin": {
        "privateKey": "de96050609de4b4088375193dd0cf02c3f09ecaf136fb326c71c8f39111a7b1f", 
        "address": "0x1656F4E2Dfe9E3a50c499050e79765D9Ff30867a", 
        "Name": "Admin"
    }, 
    "Auditor": {
        "privateKey": "d62d521222eb3a0f78d57526feb7c0b6dee81341ed6066ce43d7a226369fe7b2", 
        "address": "0x40545333Bd4482A58c9DC93246666AC6D991D48F", 
        "Name": "Auditor"
    }, 
    "Regulator": {
        "privateKey": "02c045c5f77603c4d3347ce7f1e317287cf35a6a0650fc96b9bcf3e71986c732", 
        "address": "0x6762A3d7f6d29b88df40E0cAFF2c8eacc92aEF20", 
        "Name": "Regulator"
    },
    "Provider1": {
        "privateKey": "772d16f529c7decc55d67b8ba00627851f0cf537885c04df52e3c56c16dde504", 
        "address": "0x2deEf17FC0BE9E508792D78b60b97842fEb84ffa", 
        "Name": "Provider1", 
        "Role": 0
    },
     "Provider2": {
        "privateKey": "2b8429e4528ee2d08ce07b567578049dacf6758f9a7c982a65bed3053cb0d215", 
        "address": "0x9552f500d4815e2A3353def83D8122D94dee9e04", 
        "Name": "Provider2", 
        "Role": 0
    },
    "Provider3": {
        "privateKey": "1c7ab9250428659dfead1bc3665363f7a2647744c00f1b2fbae3f7c3b8e1aa1a", 
        "address": "0x2d3674F8EF64652A8aaa041f637251e1b1F34C52",
        "Name": "Provider3", 
        "Role": 0
    },
    "Buyer1": {
        "privateKey": "13493ece8d77a3b34bb57b7a2f3ef7e558df4e55ed23e8ba086b4213e75907db", 
        "address": "0xa7CA55F25e51dA8024A4D2f6D4D9a28D9c4d9541",
        "Name": "Buyer1", 
        "Role": 1,
        "filelocation": 1234
    },
    "Buyer2": {
        "privateKey": "1f8f68e2cca328d56499bc39e3c39a6831cba23cb3985b7a3683802d6e8cd959", 
        "address": "0x7A4eFdB8482e2262869a07013bF96Ef8A4074f00",
        "Name": "Buyer2", 
        "Role": 1,
        "filelocation": 1234
    },
    "Buyer3": {
        "privateKey": "258063f63f70da3247c20124198abda0c426174d82ebcc9aadb85bcdd83a9282", 
        "address": "0x28FF57b9E3fAC07F4d2D32c90fB9f22ED1502e9d",
        "Name": "Buyer3", 
        "Role": 1,
        "filelocation": 1234
    }
}

URL = 'http://127.0.0.1:8545'

print('\n********************************************************************')
print('Initialization: Deploy marketplace, rule, privacyrating contracts')
print('********************************************************************')

#deploy marketplace contracts
registerAddress, registerABI, register_gasUsed = setup.deployRegistercontracts(URL)

print('\n********************************************************************')
print(f'Create Admin, auditor, provider and buyer instances for Marketplace')
print('********************************************************************')
                  
_Admin = admin(entityList['Admin']['privateKey'], entityList['Admin']['address'], entityList['Admin']['Name'], registerAddress, registerABI, URL)

_Auditor = admin(entityList['Auditor']['privateKey'], entityList['Auditor']['address'], entityList['Auditor']['Name'], registerAddress, registerABI, URL)

_Regulator = admin(entityList['Regulator']['privateKey'], entityList['Regulator']['address'], entityList['Regulator']['Name'], registerAddress, registerABI, URL)

_Provider1 = user(entityList['Provider1']['privateKey'], entityList['Provider1']['address'], entityList['Provider1']['Name'], entityList['Provider1']['Role'], registerAddress, registerABI, URL)

_Provider2 = user(entityList['Provider2']['privateKey'], entityList['Provider2']['address'], entityList['Provider2']['Name'], entityList['Provider2']['Role'], registerAddress, registerABI, URL)

_Provider3 = user(entityList['Provider3']['privateKey'], entityList['Provider3']['address'], entityList['Provider3']['Name'], entityList['Provider3']['Role'], registerAddress, registerABI, URL)

_Buyer1 = user(entityList['Buyer1']['privateKey'], entityList['Buyer1']['address'], entityList['Buyer1']['Name'], entityList['Buyer1']['Role'], registerAddress, registerABI, URL)

_Buyer2 = user(entityList['Buyer2']['privateKey'], entityList['Buyer2']['address'], entityList['Buyer2']['Name'], entityList['Buyer2']['Role'], registerAddress, registerABI, URL)

_Buyer3 = user(entityList['Buyer3']['privateKey'], entityList['Buyer3']['address'], entityList['Buyer3']['Name'], entityList['Buyer3']['Role'], registerAddress, registerABI, URL)

print('\n********************************************************************')
print(f'Registration and Setup: Add regulator, register auditor and users')
print('********************************************************************')

#create profile for provider1 in marketplace
_Provider1.createProfileinMarketplace()

#create profile for provider2 in marketplace
_Provider2.createProfileinMarketplace()

#create profile for provider3 in marketplace
_Provider3.createProfileinMarketplace()

#create profile for Buyer1 in marketplace
_Buyer1.createProfileinMarketplace()


#create profile for Buyer1 in marketplace
_Buyer2.createProfileinMarketplace()


#create profile for Buyer1 in marketplace
_Buyer3.createProfileinMarketplace()


print('\n********************************************************************')
print(f'Build profile for data-buyers')
print('********************************************************************')

def addSubscriptionsinMarketplace(_AID, provider, buyer):
    _SID, addSubscriptiongasUsed = provider.addSubscription(_AID, 1, 0, 2, 2, 2, 2, 2, 2, True);
    provider.startSubscription(_AID, _SID)
    buyer.startSubscription(_AID, _SID)
    buyer.confirmDelivery(_AID, _SID)
    return _SID
    
def createAgreements(provider, buyer):
    subscriptionAddress, subscriptionABI, subscriptionGasUsed = provider.deploySubscriptionSc(buyer.profile['address'])
    buyer.subscriptionAddress = subscriptionAddress
    buyer.subscriptionABI = subscriptionABI
    AID1, registerAgreementGasUsed1 = provider.registerAgreement(subscriptionAddress, subscriptionABI)
    AID2, registerAgreementGasUsed2 = buyer.registerAgreement(subscriptionAddress, subscriptionABI)
    if (AID1 == AID2):
        _AID = AID1
        print(f'>> Agreement ID is: {_AID}')
    return _AID

#AID11 = AID(provider)(buyer)
AID11 = createAgreements(_Provider1, _Buyer1)
SID11_1 = addSubscriptionsinMarketplace(AID11, _Provider1, _Buyer1)
SID11_2 = addSubscriptionsinMarketplace(AID11, _Provider1, _Buyer1)
SID11_3 = addSubscriptionsinMarketplace(AID11, _Provider1, _Buyer1)
SID11_4 = addSubscriptionsinMarketplace(AID11, _Provider1, _Buyer1)
SID11_5 = addSubscriptionsinMarketplace(AID11, _Provider1, _Buyer1)


#AID11 = AID(provider)(buyer)
AID12 = createAgreements(_Provider1, _Buyer2)
SID12_1 = addSubscriptionsinMarketplace(AID12, _Provider1, _Buyer2)
SID12_2 = addSubscriptionsinMarketplace(AID12, _Provider1, _Buyer2)
SID12_3 = addSubscriptionsinMarketplace(AID12, _Provider1, _Buyer2)
SID12_4 = addSubscriptionsinMarketplace(AID12, _Provider1, _Buyer2)
SID12_5 = addSubscriptionsinMarketplace(AID12, _Provider1, _Buyer2)

#AID11 = AID(provider)(buyer)
AID21 = createAgreements(_Provider2, _Buyer1)
SID21_1 = addSubscriptionsinMarketplace(AID21, _Provider2, _Buyer1)
SID21_2 = addSubscriptionsinMarketplace(AID21, _Provider2, _Buyer1)
SID21_3 = addSubscriptionsinMarketplace(AID21, _Provider2, _Buyer1)
SID21_4 = addSubscriptionsinMarketplace(AID21, _Provider2, _Buyer1)
SID21_5 = addSubscriptionsinMarketplace(AID21, _Provider2, _Buyer1)



#_SID, addSubscriptiongasUsed = _Provider1.addSubscription(_AID, 1, 0, 2, 2, 2, 2, 2, 2, True);
#_Provider1.startSubscription(_AID, _SID)
#_Buyer1.startSubscription(_AID, _SID)
#_Buyer1.confirmDelivery(_AID, _SID)


#subscriptionAddress, subscriptionABI, subscriptionGasUsed = _Provider1.deploySubscriptionSc(entityList['Buyer2']['address'])
#_Buyer2.subscriptionAddress = subscriptionAddress
#_Buyer2.subscriptionABI = subscriptionABI

#AID1, registerAgreementGasUsed1 = _Provider1.registerAgreement(subscriptionAddress, subscriptionABI)
#AID2, registerAgreementGasUsed2 = _Buyer2.registerAgreement(subscriptionAddress, subscriptionABI)

#if (AID1 == AID2):
#        _AID = AID1
#        print(f'>> Agreement ID is: {_AID}')


#_SID, addSubscriptiongasUsed = _Provider1.addSubscription(_AID, 1, 0, 2, 2, 2, 2, 2, 2, True);
#_Provider1.startSubscription(_AID, _SID)
#_Buyer2.startSubscription(_AID, _SID)
#_Buyer2.confirmDelivery(_AID, _SID)




