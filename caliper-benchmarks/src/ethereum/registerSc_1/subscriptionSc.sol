//"SPDX-License-Identifier: UNSW"
pragma experimental ABIEncoderV2;
pragma solidity ^0.5.13;
/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
 
 contract interfaceSubscription{
    function initialize(bytes32 _seller, bytes32 _buyer) public;
    function updateS(bytes32 _SID, string memory field, bytes32 _value) public;
    function confirmDelivery(bytes32 _SID) public;
    function payment(bytes32 _SID) public;
    function addSubscription(uint time, uint dataType, uint interval, uint period, uint age, uint samples, uint dim, uint price, bool resell) public;
    function getSubscriptionbyID(bytes32 SID) public view returns (uint[8] memory specifications, bool resell, string memory status);
 } 
 
 contract subscriptionSc {
     
    struct Subscription{
         uint time;         //0
         uint dataType;     //1
         uint interval;     //2
         uint period;       //3
         uint age;          //4
         uint samples;      //5
         uint dim;          //6
         uint price;        //7
         string status;
         bool resell;
    }

    bytes32[] subcriptionIDs;
    bytes32 public Seller;
    bytes32 public Buyer;
    mapping(bytes32 => Subscription) subscriptions;
    
    //{ 0: AWAITING_PAYMENT, 1: AWAITING_DELIVERY, 2: AWAITING_SETTLEMENT, 3: COMPLETE }
    mapping(bytes32 => uint8) public PaymentCurrState;
    
    
    event subscriptionID(bytes32);
    event subscriptionStatus(string);
    
    //constructor(string memory _seller, string memory _buyer) {
    function initialize(bytes32 _seller, bytes32 _buyer) public{
        Seller = _seller;
        Buyer = _buyer;
    }
    
    
    function addSubscription(uint time, uint dataType, uint interval, uint period, uint age, uint samples, uint dim, uint price, bool resell) public{
        //require (tx.origin == Seller);
        bytes32 SID = keccak256(abi.encode(subcriptionIDs.length));
        subcriptionIDs.push(SID);
        subscriptions[SID].time = time;
        subscriptions[SID].dataType = dataType;
        subscriptions[SID].interval = interval;
        subscriptions[SID].period = period;
        subscriptions[SID].age = age;
        subscriptions[SID].samples = samples;
        subscriptions[SID].dim = dim;
        subscriptions[SID].price = price;
        subscriptions[SID].status = "ACTIVE";
        subscriptions[SID].resell = resell;
        deposit(SID);
        emit subscriptionID(SID);
        //emit subscriptionStatus("Subcription initiated");
    }
    
    //PaymentStatus: 0: AWAITING_PAYMENT, 1: AWAITING_DELIVERY , 2: AWAITING_SETTLEMENT, 3: COMPLETE
    function deposit(bytes32 _SID) internal {
        require(PaymentCurrState[_SID] == 0, "Already paid");
        PaymentCurrState[_SID] = 1;
    }
    
    //PaymentStatus: 0: AWAITING_PAYMENT, 1: AWAITING_DELIVERY , 2: AWAITING_SETTLEMENT, 3: COMPLETE
    function confirmDelivery(bytes32 _SID) public {
        require(PaymentCurrState[_SID] == 1, "Cannot confirm delivery");
        PaymentCurrState[_SID]  = 2;
    }
    
    //PaymentStatus: 0: AWAITING_PAYMENT, 1: AWAITING_DELIVERY , 2: AWAITING_SETTLEMENT, 3: COMPLETE
    //subscription status: INITIATE, Active, finish, SETTLEMENT
    function updateS(bytes32 _SID, string memory field) public{
        if(compareStrings(field, "statusF")){
            subscriptions[_SID].status = "FINISH";
            PaymentCurrState[_SID]  = 3;
        }
        emit subscriptionStatus("Subcription Updated");
    }
    
    //subscription status: INITIATE, Active, finish, SETTLEMENT
    //require the signature from buyer
    function payment(bytes32 _SID) public{
        subscriptions[_SID].status = "SETTLEMENT";
        emit subscriptionStatus("Subcription Settlement");
    }
    
    
    function compareStrings(string memory a, string memory b) internal pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }
    
    function getSubscriptionbyID(bytes32 SID) public view returns (uint[8] memory specifications, bool resell, string memory status) {
        specifications[0] = subscriptions[SID].time;
        specifications[1] = subscriptions[SID].dataType;
        specifications[2] = subscriptions[SID].interval;
        specifications[3] = subscriptions[SID].period;
        specifications[4] = subscriptions[SID].age;
        specifications[5] = subscriptions[SID].samples;
        specifications[6] = subscriptions[SID].dim;
        specifications[7] = subscriptions[SID].price;
        return (specifications, subscriptions[SID].resell, subscriptions[SID].status);
    }

    
    function paymentStatus(bytes32 _SID) public view returns (string memory result) {
        //require (tx.origin == Seller || tx.origin == Buyer, "not an authorized entity");
        if(PaymentCurrState[_SID] == 0) {
            result = "AWAITING_PAYMENT";
        } else if(PaymentCurrState[_SID] == 1) {
            result = "AWAITING_DELIVERY";
        } else if(PaymentCurrState[_SID] == 2) {
            result = "AWAITING_SETTLEMENT";
        } else {
            result = "COMPLETE";
        }
        return result;
    }
 
 }


