// SPDX-License-Identifier: UNSW
pragma solidity ^0.8.9;
pragma abicoder v2;

import "./RuleSc.sol";
import "./BuyerSc.sol";

interface interfacePR {
    function createProfile(address buyerAddr) external returns(address);
    function updatePurchase(address buyerAddr, uint _time, uint _samples, address _provider, uint _interval, uint _period, uint _age, uint _type, uint _dimensions, bool _resell) external returns(bool);
    function updatePractice(address buyerAddr, int P, int V, int G, int Co, int DS, int R, uint time) external;
    function updateImpact(address buyerAddr, uint _time, uint _vol, uint _pro, uint _sens, uint _agree) external;
    function retrieveCurrentPurchase(address buyerAddr, address providerAddr) view external returns(uint[3] memory, uint[4][] memory);
    function retrieveFuturePurchase(address buyerAddr, address providerAddr) view external returns(uint[4][] memory, uint[5][] memory);
    function retrieveleakageProfile(address buyerAddr, uint RS) view external returns(uint[5][] memory, uint[4] memory, uint Likelihood);
    function retrievepracticeProfile(address buyerAddr) view external returns(int[7] memory);
}

contract privacyRatingSc {

    address ruleAddr;
    RuleSc ruleSc;
    address[] public buyerContractsList;

    //buyer address = BuyerSc address
    mapping(address => address) buyerMap;

    constructor(address _ruleAddr) {
        ruleAddr = _ruleAddr;
        ruleSc = RuleSc(_ruleAddr);
    }

    function createProfile(address buyerAddr) external returns(address){
        BuyerSc buyerContract = new BuyerSc();
        buyerContractsList.push(address(buyerContract));
        buyerMap[buyerAddr] = address(buyerContract);
        return address(buyerContract);
    }

    function updatePurchase(address buyerAddr, uint _time, uint _samples, address _provider, uint _interval, uint _period, uint _age, uint _type, uint _dimensions, bool _resell) external returns(bool){
        BuyerSc buyerContract = BuyerSc(buyerMap[buyerAddr]);
        uint[3] memory temporalScore = ruleSc.getTemporalScore(_type, _interval, _period, _age);
        buyerContract.updatePurchaseProfile(_provider, _time, _samples, temporalScore[0], temporalScore[1], temporalScore[2], _type, _dimensions, _resell);
        return true;
    }

    function updatePractice(address buyerAddr, int P, int V, int G, int Co, int DS, int R, int time) external {
        BuyerSc buyerContract = BuyerSc(buyerMap[buyerAddr]);
        buyerContract.updatePracticeProfile(P, V, G, Co, DS, R, time);
    }

    function updateImpact(address buyerAddr, uint _time, uint _vol, uint _pro, uint _sens, uint _agree) external {
        BuyerSc buyerContract = BuyerSc(buyerMap[buyerAddr]);
        uint[4] memory Score = ruleSc.getImpactScore( _vol, _pro, _agree, _sens);
        buyerContract.updateLeakImpact(_time, Score[0], Score[1], Score[2], Score[3]);
    }

   function retrieveCurrentPurchase(address buyerAddr, address providerAddr) view external returns(uint[3] memory, uint[4][] memory){
        BuyerSc buyerContract = BuyerSc(buyerMap[buyerAddr]);
        uint[3] memory nontemp_current;
        uint[4][] memory temp_current; //= new uint[4][](buyerContract.getTradeCounts(provider)) ;
        (nontemp_current, temp_current) = buyerContract.currentPossession(providerAddr);
        uint[3] memory score = ruleSc.getNonTemporalScore(nontemp_current[0], nontemp_current[1], nontemp_current[2]);
        return(score, temp_current);
   }

    function retrieveFuturePurchase(address buyerAddr, address providerAddr) view external returns(uint[4][] memory, uint[5][] memory) {
        uint futurelength;
        uint i;
        for(i=0; i<buyerContractsList.length; i++){
            if(buyerContractsList[i] != buyerMap[buyerAddr]){
                BuyerSc other_buyerContract = BuyerSc(buyerContractsList[i]);
                futurelength += other_buyerContract.getTradeCounts(providerAddr);
            }
        }
        uint[4][] memory nontemp_future = new uint[4][](buyerContractsList.length);
        uint[5][] memory temp_future = new uint[5][](futurelength);
        uint[3] memory score;
        uint[3] memory nontemp;
        uint[4][] memory temp;
        uint count = 0;
        for(i=0; i<buyerContractsList.length; i++){
            if(buyerContractsList[i] != buyerMap[buyerAddr]){
                BuyerSc other_buyerContract = BuyerSc(buyerContractsList[i]);
                (nontemp, temp) = other_buyerContract.futureAcquisition(providerAddr);
                score = ruleSc.getNonTemporalScore(nontemp[0], nontemp[1], nontemp[2]);
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

    function retrieveleakageProfile(address buyerAddr, uint RS) view external returns(uint[5][] memory, uint[4] memory, uint Likelihood){
        uint[5][] memory pastImpactScores;
        uint[4] memory currentImpact;
        BuyerSc buyerContract = BuyerSc(buyerMap[buyerAddr]);
        (pastImpactScores, currentImpact) = buyerContract.LeakageProfile();
        uint[4] memory currentImpactScore = ruleSc.getImpactScore(currentImpact[0], currentImpact[1], currentImpact[2], currentImpact[3]);
        int dataSecurity = buyerContract.PracticeProfile()[4]; 

        Likelihood = ruleSc.getLikelihood(RS, dataSecurity);
        return(pastImpactScores, currentImpactScore, Likelihood);
    }

    function retrievepracticeProfile(address buyerAddr) view external returns(int[7] memory){
        BuyerSc buyerContract = BuyerSc(buyerMap[buyerAddr]);
        return (buyerContract.PracticeProfile());
    }
}