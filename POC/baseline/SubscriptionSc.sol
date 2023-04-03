//SPDX-License-Identifier: UNSW
pragma solidity ^0.8.9;
pragma abicoder v2;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
 
 interface interfaceSubscription{
    function updateS(bytes32 _SID, string memory field, bytes32 _value) external;
    function SignOutside(address) external;
    function reset() external;
    function confirmDelivery(bytes32 _SID) external;
    function payment(bytes32 _SID) external;
    function getSubscriptionbyID(bytes32 SID) external view returns (uint[8] memory specifications, bool resell, string memory status);
 } 
 
 contract SubscriptionSc {
     
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
    address public Seller;
    address public Buyer;
    mapping(bytes32 => Subscription) subscriptions;
    mapping(address => bool) signed;
    
    //{ 0: AWAITING_PAYMENT, 1: AWAITING_DELIVERY, 2: AWAITING_SETTLEMENT, 3: COMPLETE }
    mapping(bytes32 => uint8) public PaymentCurrState;
    
    
    event subscriptionID(bytes32);
    event subscriptionStatus(string);
    
    constructor(address _seller, address _buyer) {
        Seller = _seller;
        Buyer = _buyer;
    }
    
    modifier onlyBuyer() {
        require(tx.origin == Buyer, "Only buyer can call this method");
        _;
    }
 
    function addSubscription(uint time, uint dataType, uint interval, uint period, uint age, uint samples, uint dim, uint price, bool resell) public{
        require (tx.origin == Seller);
        bytes32 SID = keccak256(abi.encode(subcriptionIDs.length, Seller, Buyer));
        subcriptionIDs.push(SID);
        subscriptions[SID].time = time;
        subscriptions[SID].dataType = dataType;
        subscriptions[SID].interval = interval;
        subscriptions[SID].period = period;
        subscriptions[SID].age = age;
        subscriptions[SID].samples = samples;
        subscriptions[SID].dim = dim;
        subscriptions[SID].price = price;
        subscriptions[SID].status = "INITIATE";
        subscriptions[SID].resell = resell;
        emit subscriptionID(SID);
        emit subscriptionStatus("Subcription initiated");
    }
    
    //require the signature from both seller and buyer
    function startSubscription(bytes32 _SID) public{
        Sign();
        //require (signed[Buyer] == true && signed[Seller] == true, "Require sign by both the actors");
        if(signed[Buyer] == true && signed[Seller] == true){
            subscriptions[_SID].status = "ACTIVE";
            deposit(_SID);
            reset();
            emit subscriptionStatus("Subcription Started");
        }
        emit subscriptionStatus("Require sign by both the actors");
    }
    
    //PaymentStatus: 0: AWAITING_PAYMENT, 1: AWAITING_DELIVERY , 2: AWAITING_SETTLEMENT, 3: COMPLETE
    function deposit(bytes32 _SID) onlyBuyer internal {
        require(PaymentCurrState[_SID] == 0, "Already paid");
        PaymentCurrState[_SID] = 1;
    }
    
    //PaymentStatus: 0: AWAITING_PAYMENT, 1: AWAITING_DELIVERY , 2: AWAITING_SETTLEMENT, 3: COMPLETE
    function confirmDelivery(bytes32 _SID) external {
        require(PaymentCurrState[_SID] == 1, "Cannot confirm delivery");
        PaymentCurrState[_SID]  = 2;
    }
    
    //PaymentStatus: 0: AWAITING_PAYMENT, 1: AWAITING_DELIVERY , 2: AWAITING_SETTLEMENT, 3: COMPLETE
    //subscription status: INITIATE, Active, finish, SETTLEMENT
    function updateS(bytes32 _SID, string memory field) external{
        if(compareStrings(field, "statusF")){
            subscriptions[_SID].status = "FINISH";
            PaymentCurrState[_SID]  = 3;
        }
        emit subscriptionStatus("Subcription Updated");
    }
    
    //subscription status: INITIATE, Active, finish, SETTLEMENT
    //require the signature from buyer
    function payment(bytes32 _SID) external{
        require (tx.origin == Buyer);
        subscriptions[_SID].status = "SETTLEMENT";
        emit subscriptionStatus("Subcription Settlement");
    }
    
    function reset() internal {
        signed[Buyer] = false;
        signed[Seller] = false;
    }
    

    function Sign() internal {
        require (tx.origin == Seller || tx.origin == Buyer);
        require (signed[tx.origin] == false);
        signed[tx.origin] = true;
    }
    
    
    function compareStrings(string memory a, string memory b) internal pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }
    
    function getSubscriptionList() external view returns (Subscription[] memory) {
        uint count = subcriptionIDs.length;
        Subscription[] memory SL = new Subscription[](count);
        for(uint i=0; i<count; i++){
            bytes32 _SID = subcriptionIDs[i];
            SL[i] = subscriptions[_SID];
        }
        return SL;
    }

    function getSubscriptionbyID(bytes32 SID) external view returns (uint[8] memory specifications, bool resell, string memory status) {
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

    
    function paymentStatus(bytes32 _SID) external view returns (string memory result) {
        require (tx.origin == Seller || tx.origin == Buyer, "not an authorized entity");
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


