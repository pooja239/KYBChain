//"SPDX-License-Identifier: UNSW"
pragma experimental ABIEncoderV2;
pragma solidity ^0.5.13;

import "./ruleSc.sol";
import "./buyerSc.sol";


contract interfacePR {
    function createProfile(bytes32 buyer) public;
    function updatePurchase(bytes32 buyer, uint _time, uint _samples, bytes32 _provider, uint _interval, uint _period, uint _age, uint _type, uint _dimensions, bool _resell) public returns(bool);
    function retrieveCurrentPurchase(bytes32 buyer, bytes32 provider) view public returns(uint[3] memory, uint[4][] memory);
    function retrieveFuturePurchase(bytes32 buyer, bytes32 provider) view public returns(uint[4][] memory, uint[5][] memory) ;
}


contract privacyRatingSc {

    address ruleAddr;
    
    //buyer id = BuyerSc address
    mapping(bytes32 => address) buyerMap;
    address[] public buyerContractsList;

    constructor() public{
        ruleSc _ruleSc = new ruleSc();
        ruleAddr = address(_ruleSc);
        //ruleAddr = _ruleSc;
    }


    function createProfile(bytes32 buyer) public{
        buyerSc buyerContract = new buyerSc();
        buyerContractsList.push(address(buyerContract));
        //buyerContractsList.push(buyerContract);
        buyerMap[buyer] = address(buyerContract);
        //return address(buyerContract);
    }

    function updatePurchase(bytes32 buyer, uint _time, uint _samples, bytes32 _provider, uint _interval, uint _period, uint _age, uint _type, uint _dimensions, bool _resell) public returns(bool){
        buyerSc buyerContract = buyerSc(buyerMap[buyer]);
        uint[3] memory temporalScore = ruleSc(ruleAddr).getTemporalScore(_type, _interval, _period, _age);
        buyerContract.updatePurchaseProfile(_provider, _time, _samples, temporalScore[0], temporalScore[1], temporalScore[2], _type, _dimensions, _resell);
        return true;
    }

    function retrieveCurrentPurchase(bytes32 buyer, bytes32 provider) view public returns(uint[3] memory, uint[4][] memory){
        buyerSc buyerContract = buyerSc(buyerMap[buyer]);
        uint[3] memory nontemp_current;
        uint[4][] memory temp_current; 
        (nontemp_current, temp_current) = buyerContract.currentPossession(provider);
        uint[3] memory score = ruleSc(ruleAddr).getNonTemporalScore(nontemp_current[0], nontemp_current[1], nontemp_current[2]);
        return(score, temp_current);
   }

    function retrieveFuturePurchase(bytes32 buyer, bytes32 provider) view public returns(uint[4][] memory, uint[5][] memory) {
        uint futurelength;
        uint i;
        for(i=0; i<buyerContractsList.length; i++){
            if(buyerContractsList[i] != buyerMap[buyer]){
                buyerSc other_buyerContract = buyerSc(buyerContractsList[i]);
                futurelength += other_buyerContract.getTradeCounts(provider);
            }
        }
        uint[4][] memory nontemp_future = new uint[4][](buyerContractsList.length);
        uint[5][] memory temp_future = new uint[5][](futurelength);
        uint[3] memory score;
        uint[3] memory nontemp;
        uint[4][] memory temp;
        uint count = 0;
        for(i=0; i<buyerContractsList.length; i++){
            if(buyerContractsList[i] != buyerMap[buyer]){
                buyerSc other_buyerContract = buyerSc(buyerContractsList[i]);
                (nontemp, temp) = other_buyerContract.futureAcquisition(provider);
                score = ruleSc(ruleAddr).getNonTemporalScore(nontemp[0], nontemp[1], nontemp[2]);
                nontemp_future[i] = [i, score[0], score[1], score[2]];
                for(uint j=0; j < temp.length; j++){
                    temp_future[count] = [i, temp[j][0], temp[j][1], temp[j][2], temp[j][3]];
                    count++;
                }
            }
            else {
                nontemp_future[i] = [i, 99, 99, 99];
            }
        }
        return(nontemp_future, temp_future);
   }

}