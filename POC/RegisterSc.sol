//SPDX-License-Identifier: UNSW
pragma solidity ^0.8.9;
pragma abicoder v2;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
 
 import "./subscriptionSc.sol"; 
 import "./privacyRatingSc.sol";
 
 contract RegisterSc {

    enum Role{PROVIDER, BUYER, DUAL}
    
    struct buyerProfile{
        uint policylocation;
        bool KYBapproved;
        address buyerContract;
    }

    struct User {
        //bytes32 ID;
        Role role;
        uint balances;
        bool exist;
        buyerProfile buyerInfo;
        uint RS; //reputation score = (0,100)/100 = (0,1.00)
    }

    mapping(address => bool) public auditorList;
    mapping(address => bool) public regulatorList;

    //userManagement = {"actorAddress": {"Role": , "Balances": , "Exist": , "buyerInfo":}}
    mapping(address => User) public userManagement;
    
    //agreementManagement = (AID: contractAddress)
    mapping(bytes32 => address) public agreementManagement;

    address[] auditors;
    address privacyratingAddr;
    privacyRatingSc prSC;
    address admin;
    
    event uploadedPolicy(address);
    event log(string);
    event logID(bytes32);

    modifier onlyAuditor {
        require(auditorList[msg.sender]);
        _;
    }
    
    modifier onlyRegulator {
        require(regulatorList[msg.sender]);
        _;
    }

    modifier onlyAdmin {
        require(admin == msg.sender);
        _;
    }

    constructor(address _privacyratingAddr){
        privacyratingAddr = _privacyratingAddr;
        prSC = privacyRatingSc(_privacyratingAddr);
        admin = msg.sender;
    }

    function addRegulator(address _regulator) external onlyAdmin{
        require(!regulatorList[_regulator], "already exist");
        regulatorList[_regulator] = true;
    }

    function registerAuditor() external {
        require(!auditorList[msg.sender], "already registered");
        auditorList[msg.sender] = true;
        auditors.push(msg.sender);
    }
    
    function registerUser(Role _role, uint _balance) public{
        
        //bytes32 _userPUK = keccak256(abi.encode(user));
        require(!userManagement[msg.sender].exist, "User is already registered");
        //userManagement[msg.sender].ID = _userPUK;
        userManagement[msg.sender].exist = true;
        userManagement[msg.sender].role = _role;
        userManagement[msg.sender].balances = _balance;
        if(uint8(_role) == uint8(Role.BUYER) || uint8(_role) == uint8(Role.DUAL)){
            //privacyRatingSc PRcontract = privacyRatingSc(privacyratingAddr);
            userManagement[msg.sender].buyerInfo.buyerContract = prSC.createProfile(msg.sender);
        }
        emit log("User registered successfully");
        //emit logID(_userPUK);
        //return true;
    }

    function uploadPolicy(uint _fileID) external {
        //bytes32 _userPUK = keccak256(abi.encode(user));
        require(userManagement[msg.sender].exist && uint8(userManagement[msg.sender].role) != 0, "User is not registered as buyer or dual");
        //require(!(userManagement[_userPUK].role == 0), "User is not registered as buyer or dual");
        userManagement[msg.sender].buyerInfo.policylocation = _fileID;
        emit uploadedPolicy(msg.sender);
    }

    function AuditReport(address _buyer, int P, int V, int G, int Co, int DS, int R, int time) external onlyAuditor{
        //privacyRatingSc PRcontract = privacyRatingSc(privacyratingAddr);
        prSC.updatePractice(_buyer, P, V, G, Co, DS, R, time);
        userManagement[_buyer].buyerInfo.KYBapproved = true;
    }

    function InvestigationReport(address _buyer, uint _time, uint _vol, uint _pro, uint _sens, uint _agree) external onlyRegulator{
        //privacyRatingSc PRcontract = privacyRatingSc(privacyratingAddr);
        prSC.updateImpact(_buyer, _time, _vol, _pro, _sens, _agree);
    }

    function retrieveProfiles(address _buyer, address _provider) view external returns(uint[3] memory currentNon, uint[4][] memory currentTem, uint[4][] memory futureNon, uint[5][] memory futureTem, uint[5][] memory pastImpacts, uint[4] memory currentImpact, uint likelihood, int[7] memory practice){
        (currentNon, currentTem) = prSC.retrieveCurrentPurchase(_buyer, _provider);
        (futureNon, futureTem) = prSC.retrieveFuturePurchase(_buyer, _provider);
        (pastImpacts, currentImpact, likelihood) =  prSC.retrieveleakageProfile(_buyer, userManagement[_buyer].RS);
        if(userManagement[_buyer].buyerInfo.KYBapproved) {
            practice = prSC.retrievepracticeProfile(_buyer);
        } else {
            int x = -99;
            practice = [x, x, x, x, x, x, x];
        }
        return(currentNon, currentTem, futureNon, futureTem, pastImpacts, currentImpact, likelihood, practice);
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
            // buyerAddr, time, samples, provider, interval, period, age, datatype, dimensions, resell
            prSC.updatePurchase(buyer, subscription[0], subscription[5], seller, subscription[2], subscription[3], subscription[4], subscription[1], subscription[6], resell);
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