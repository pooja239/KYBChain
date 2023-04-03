//SPDX-License-Identifier: UNSW
pragma solidity ^0.8.9;
pragma abicoder v2;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
 
 import "./subscriptionSc.sol";

 
 contract RegisterSc {

    enum Role{PROVIDER, BUYER, DUAL}

    struct User {
        //bytes32 ID;
        Role role;
        uint balances;
        bool exist;
        uint RS; //reputation score = (0,100)/100 = (0,1.00)
    }


    //userManagement = {"actorAddress": {"Role": , "Balances": , "Exist": , "buyerInfo":}}
    mapping(address => User) public userManagement;
    
    //agreementManagement = (AID: contractAddress)
    mapping(bytes32 => address) public agreementManagement;

    address admin;
    
    event log(string);
    event logID(bytes32);

    modifier onlyAdmin {
        require(admin == msg.sender);
        _;
    }

    function registerUser(Role _role, uint _balance) public{
        
        //bytes32 _userPUK = keccak256(abi.encode(user));
        require(!userManagement[msg.sender].exist, "User is already registered");
        //userManagement[msg.sender].ID = _userPUK;
        userManagement[msg.sender].exist = true;
        userManagement[msg.sender].role = _role;
        userManagement[msg.sender].balances = _balance;
        emit log("User registered successfully");
        //emit logID(_userPUK);
        //return true;
    }
    
    //multi-sig function
    function registerAgreement(address _contractAddress) public returns(bool){
        SubscriptionSc subsriptionContract =  SubscriptionSc(_contractAddress);
        address buyer = subsriptionContract.Buyer();
        address seller = subsriptionContract.Seller();
        bytes32 _agreementID = keccak256(abi.encode(seller,buyer));
        agreementManagement[_agreementID] = _contractAddress;
        emit logID(_agreementID);
        return true;
    }

    function confirmDelivery(bytes32 _AID, bytes32 _SID) public {
        SubscriptionSc subsriptionContract =  SubscriptionSc(agreementManagement[_AID]);
        address buyer = subsriptionContract.Buyer();
        require(msg.sender == buyer, "Accessible by only buyer");
        require(subsriptionContract.PaymentCurrState(_SID) == 1, "Cannot confirm delivery");
        uint[8] memory subscription; // 0: time, 1: dataType, 2: interval, 3:period, 4:age, 5: samples, 6: dim, 7: price
        bool resell;
        string memory status;
        (subscription,resell,status) = subsriptionContract.getSubscriptionbyID(_SID);
        address seller = subsriptionContract.Seller();
        subsriptionContract.confirmDelivery(_SID); //mark the payment status to AWAITING_SETTLEMENT"
        if(paymentSettlement(buyer, seller, subscription[7])){ //send payment using paymentSc
            subsriptionContract.payment(_SID); //mark the subscription status to SETTLEMENT
            subsriptionContract.updateS(_SID, "statusF");  //updateS
        }
    }

    function paymentSettlement(address sender, address recipient, uint amount) internal returns (bool){
        uint senderBalance = userManagement[sender].balances;
        require(senderBalance >= amount, "transfer amount exceeds balance");
        userManagement[sender].balances = senderBalance - amount;
        //address Recipient = AccountID[_recipient];
        userManagement[recipient].balances += amount;
        //emit Transfer(msg.sender, Recipient, amount);
        return true;
    }


    
    function getSellerInfo(bytes32 _AID) public view returns(address seller) {
        //require(msg.sender == digitalNotary, "Accessible by only digital notary");
        SubscriptionSc subsriptionContract =  SubscriptionSc(agreementManagement[_AID]);
        seller = subsriptionContract.Seller();
        return seller;
    }

    function getBuyerInfo(bytes32 _AID) public view returns(address buyer) {
        //require(msg.sender == digitalNotary, "Accessible by only digital notary");
        SubscriptionSc subsriptionContract =  SubscriptionSc(agreementManagement[_AID]);
        buyer = subsriptionContract.Buyer();
        return buyer;
    }


    
    
}