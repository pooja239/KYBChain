//"SPDX-License-Identifier: UNSW"
pragma experimental ABIEncoderV2;
pragma solidity ^0.5.13;
/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
 
 import "./subscriptionSc.sol";
 import "./privacyRatingSc.sol";
 
 contract registerSc {


    struct User {
        uint role;  //0: provider, 1: buyer
        uint balances;
    }

    mapping(bytes32 => User) userManagement;
    
    //agreementManagement = (AID: contractAddress)
    mapping(bytes32 => address) agreementManagement;

    address privacyratingAddr;
    
    event logID(bytes32);

    function initialize(address _privacyratingAddr) public {
        privacyratingAddr = _privacyratingAddr;
        //PR.initRule(_ruleAddr);
    }
    
    function registerUser(string memory username, uint _role, uint _balance) public{
        bytes32 _userPUK = keccak256(abi.encode(username));
        userManagement[_userPUK].role = _role;
        userManagement[_userPUK].balances = _balance;
        if(_role == 1) {
            //userManagement[_userPUK].buyerInfo.buyerContract = privacyRatingSc(privacyratingAddr).createProfile(_userPUK, buyerC);
            //userManagement[_userPUK].buyerContract = buyerC;
            privacyRatingSc PR = privacyRatingSc(privacyratingAddr);
            PR.createProfile(_userPUK);
        }    
    }

    function registerAgreement(string memory _seller, string memory _buyer) public returns(bool){
        bytes32 Seller = keccak256(abi.encode(_seller));
        bytes32 Buyer = keccak256(abi.encode(_buyer));
        subscriptionSc subscriptionContract =  new subscriptionSc();
        subscriptionContract.initialize(Seller, Buyer);
        bytes32 _agreementID = keccak256(abi.encode(_buyer, _seller));
        agreementManagement[_agreementID] = address(subscriptionContract);
        emit logID(_agreementID);
        return true;
    }


    function addSubscription(bytes32 _AID, uint time, uint dataType, uint interval, uint period, uint age, uint samples, uint dim, uint price, bool resell) public {
        subscriptionSc subsriptionContract =  subscriptionSc(agreementManagement[_AID]);
        subsriptionContract.addSubscription(time, dataType, interval, period, age, samples, dim, price, resell);    
    }

    function confirmDelivery(string memory _buyer, bytes32 _AID, bytes32 _SID) public {
        bytes32 _buyerPUK = keccak256(abi.encode(_buyer));
        subscriptionSc subscriptionContract =  subscriptionSc(agreementManagement[_AID]);
        if(_buyerPUK != subscriptionContract.Buyer()){
            revert('accessible by buyer');
        }
        require(subscriptionContract.PaymentCurrState(_SID) == 1, "Cannot confirm delivery");
        uint[8] memory subscription; // 0: time, 1: dataType, 2: interval, 3:period, 4:age, 5: samples, 6: dim, 7: price
        bool resell;
        string memory status;
        (subscription,resell,status) = subscriptionContract.getSubscriptionbyID(_SID);
        subscriptionContract.confirmDelivery(_SID); //mark the payment status to AWAITING_SETTLEMENT"
        if(paymentSettlement(_buyerPUK, subscriptionContract.Seller(), subscription[7])){ //send payment using paymentSc
            subscriptionContract.payment(_SID); //mark the subscription status to SETTLEMENT
            subscriptionContract.updateS(_SID, "statusF");  //updateS
         //   // buyerAddr, time, samples, provider, interval, period, age, datatype, dimensions, resell
            privacyRatingSc(privacyratingAddr).updatePurchase(_buyerPUK, subscription[0], subscription[5], subscriptionContract.Seller(), subscription[2], subscription[3], subscription[4], subscription[1], subscription[6], resell);
        }
    }
    
    function confirmDelivery_wo(string memory _buyer, bytes32 _AID, bytes32 _SID) public {
        bytes32 _buyerPUK = keccak256(abi.encode(_buyer));
        subscriptionSc subscriptionContract =  subscriptionSc(agreementManagement[_AID]);
        if(_buyerPUK != subscriptionContract.Buyer()){
            revert('accessible by buyer');
        }
        require(subscriptionContract.PaymentCurrState(_SID) == 1, "Cannot confirm delivery");
        uint[8] memory subscription; // 0: time, 1: dataType, 2: interval, 3:period, 4:age, 5: samples, 6: dim, 7: price
        bool resell;
        string memory status;
        (subscription,resell,status) = subscriptionContract.getSubscriptionbyID(_SID);
        subscriptionContract.confirmDelivery(_SID); //mark the payment status to AWAITING_SETTLEMENT"
        if(paymentSettlement(_buyerPUK, subscriptionContract.Seller(), subscription[7])){ //send payment using paymentSc
            subscriptionContract.payment(_SID); //mark the subscription status to SETTLEMENT
            subscriptionContract.updateS(_SID, "statusF");  //updateS
        }
    }


    function paymentSettlement(bytes32 sender, bytes32 recipient, uint amount) internal returns (bool){
        uint senderBalance = userManagement[sender].balances;
        require(senderBalance >= amount, "transfer amount exceeds balance");
        userManagement[sender].balances = senderBalance - amount;
        userManagement[recipient].balances += amount;
        return true;
    }

    function getSubscriptionbyID(bytes32 _AID, bytes32 _SID) view public returns (string memory status) {
        subscriptionSc subscriptionContract =  subscriptionSc(agreementManagement[_AID]);
        (, ,status) = (subscriptionContract.getSubscriptionbyID(_SID));
        return status;
    }

    function retrieveProfiles(string memory  _buyer, string memory  _seller) view public returns(uint[3] memory currentNon, uint[4][] memory currentTem, uint[4][] memory futureNon, uint[5][] memory futureTem){
        bytes32 Seller = keccak256(abi.encode(_seller));
        bytes32 Buyer = keccak256(abi.encode(_buyer));
        (currentNon, currentTem) = privacyRatingSc(privacyratingAddr).retrieveCurrentPurchase(Buyer, Seller);
        (futureNon, futureTem) = privacyRatingSc(privacyratingAddr).retrieveFuturePurchase(Buyer, Seller);
        return(currentNon, currentTem, futureNon, futureTem);
    }
 }
 
