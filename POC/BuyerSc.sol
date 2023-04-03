//SPDX-License-Identifier: UNSW
pragma solidity ^0.8.9;
pragma abicoder v2;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */


interface InterfaceBuyerSc { 


    function updatePracticeProfile(int P, int V, int G, int Co, int DS, int R, int time) external;
    function updatePurchaseProfile(address _provider, uint _time, uint _samples, uint _interval, uint _period, uint _age, uint _type, uint _dimensions, bool _resell) external;
    function updateLeakImpact(uint _time, uint _vol, uint _pro, uint _sens, uint _agree) external;
    function currentPossession(address provider) view external returns(uint[3] memory nontemp_purchaseProfile, uint[4][] memory);
    function futureAcquisition(address provider) view external returns(uint[3] memory nontemp_purchaseProfile, uint[4][] memory);
    function LeakageProfile() view external returns(uint[5][] memory, uint[4] memory);
    function PracticeProfile() view external returns(int[7] memory);
    function getTradeCounts(address provider) view external returns(uint);
}

contract BuyerSc {

    event updateProfile(string profile);

    struct practiceElements {
        int purpose;
        int visibility;
        int granularity;
        int controlMech;
        int datasecurity;
        int dataretention;
        int timestamp;
    }

    struct nontemporalElements {
        uint samples;
        uint resellSamples;
        uint[] diversity;
        uint[] dimensionality;
        //bool exist;
    }

    struct temporalElements{
        uint timestamp;
        uint intervalScore;
        uint periodScore;
        uint ageScore;
        bool resell; // 0: no resell, 1: resell
    }


    struct purchaseElements{
        nontemporalElements providerSpecific;
        temporalElements[] tradespecific;
        bool exist;
    }

    struct historicalImpact {
        uint time;
        uint volume;
        uint affectedProviders;
        uint agreements;
        uint senstivity;
    }

    struct leakageElements {
        uint totalVolume;
        uint totalProviders;
        uint totalAgreements;
        uint totalSenstivity;
    }

    mapping(address => purchaseElements) purchaseProfile;
    address[]  providersList;
    practiceElements  practiceProfile;
    historicalImpact[]  impactList;
    leakageElements currentImpact;

    function updatePurchaseProfile(address _provider, uint _time, uint _samples, uint _intervalS, uint _periodS, uint _ageS, uint _type, uint _dimensions, bool _resell) external{
        if (!purchaseProfile[_provider].exist) {
            providersList.push(_provider);
            purchaseProfile[_provider].exist=true;
            currentImpact.totalProviders += 1;
        }
        purchaseProfile[_provider].providerSpecific.samples += _samples;
        if(_resell){
            purchaseProfile[_provider].providerSpecific.resellSamples += _samples;
        }
        if(!elementexist(_dimensions, purchaseProfile[_provider].providerSpecific.dimensionality)){
            purchaseProfile[_provider].providerSpecific.dimensionality.push(_dimensions);
        }
        if(!elementexist(_type, purchaseProfile[_provider].providerSpecific.diversity)){
            purchaseProfile[_provider].providerSpecific.diversity.push(_type);
        }
        purchaseProfile[_provider].tradespecific.push(temporalElements(_time, _intervalS, _periodS, _ageS, _resell));
        currentImpact.totalVolume+=_samples;
        currentImpact.totalSenstivity += (_intervalS + _periodS + _ageS);
        currentImpact.totalAgreements += 1;
        emit updateProfile("Update purchase profile successful");
    }

    function updatePracticeProfile(int P, int V, int G, int Co, int DS, int R, int time) public {
        practiceProfile = practiceElements(P, V, G, Co, DS, R, time);
        emit updateProfile("Update practice profile successful");
    }

    function updateLeakImpact(uint _time, uint _volS, uint _proS, uint _agrS, uint _senS) external {
        //InterfaceRuleSc ruleSc = InterfaceRuleSc(ruleScAddr);
        //uint[4] impactScore = ruleScAddr.getImpactScore(_vol, _prov, _agree, _sens);
        historicalImpact memory impact = historicalImpact(_time, _volS, _proS, _agrS, _senS);
        impactList.push(impact);
        emit updateProfile("Update leakage profile successful");
    }

    function elementexist(uint _ele, uint[] memory array) pure internal returns(bool){
        for(uint i=0; i<array.length; i++) {
            if(_ele == array[i]) 
                return true;
        }
        return false;
    }

    function currentPossession(address provider) view external returns(uint[3] memory nontemp_purchaseProfile, uint[4][] memory) {
        uint[4][] memory temp_purchaseProfile = new uint[4][](purchaseProfile[provider].tradespecific.length);
        for (uint j = 0; j < purchaseProfile[provider].tradespecific.length; j++) {
            temp_purchaseProfile[j] = [purchaseProfile[provider].tradespecific[j].timestamp, purchaseProfile[provider].tradespecific[j].intervalScore, purchaseProfile[provider].tradespecific[j].periodScore, purchaseProfile[provider].tradespecific[j].ageScore];
        }             
        nontemp_purchaseProfile = [purchaseProfile[provider].providerSpecific.samples, purchaseProfile[provider].providerSpecific.dimensionality.length, purchaseProfile[provider].providerSpecific.diversity.length];
        return (nontemp_purchaseProfile, temp_purchaseProfile);
    }

    function getTradeCounts(address provider) view external returns(uint) {
        return purchaseProfile[provider].tradespecific.length;
    }

    function futureAcquisition(address provider) view external returns(uint[3] memory nontemp_purchaseProfile, uint[4][] memory) {
        uint[4][] memory temp_purchaseProfile = new uint[4][](purchaseProfile[provider].tradespecific.length);
        for (uint j = 0; j < purchaseProfile[provider].tradespecific.length; j++) {
            if(purchaseProfile[provider].tradespecific[j].resell){
                temp_purchaseProfile[j] = [purchaseProfile[provider].tradespecific[j].timestamp, purchaseProfile[provider].tradespecific[j].intervalScore, purchaseProfile[provider].tradespecific[j].periodScore, purchaseProfile[provider].tradespecific[j].ageScore];
            }
        }             
        nontemp_purchaseProfile = [purchaseProfile[provider].providerSpecific.resellSamples, purchaseProfile[provider].providerSpecific.dimensionality.length, purchaseProfile[provider].providerSpecific.diversity.length];
        return (nontemp_purchaseProfile, temp_purchaseProfile);     
    }

    function PracticeProfile() view external returns(int[7] memory) {
        return ([practiceProfile.purpose, practiceProfile.visibility, practiceProfile.granularity, practiceProfile.controlMech, practiceProfile.datasecurity, practiceProfile.dataretention, practiceProfile.timestamp]);
    }

    function LeakageProfile() view external returns(uint[5][] memory, uint[4] memory) {
        uint[5][] memory historicalimpactList = new uint[5][](impactList.length);
        for (uint i = 0; i < impactList.length; i++) {
            historicalimpactList[i] = [impactList[i].time, impactList[i].volume, impactList[i].affectedProviders, impactList[i].agreements, impactList[i].senstivity];
        }
        uint[4] memory leakageProfile = [currentImpact.totalVolume, currentImpact.totalProviders, currentImpact.totalAgreements, currentImpact.totalSenstivity];
        return (historicalimpactList, leakageProfile);
    }   
}
