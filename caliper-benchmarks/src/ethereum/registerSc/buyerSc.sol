//"SPDX-License-Identifier: UNSW"
pragma experimental ABIEncoderV2;
pragma solidity ^0.5.13;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */


contract InterfaceBuyerSc { 


    function updatePurchaseProfile(bytes32 _provider, uint _time, uint _samples, uint _interval, uint _period, uint _age, uint _type, uint _dimensions, bool _resell) public;
    function currentPossession(bytes32 provider) view public returns(uint[3] memory nontemp_purchaseProfile, uint[4][] memory);
    function futureAcquisition(bytes32 provider) view public returns(uint[3] memory nontemp_purchaseProfile, uint[4][] memory);
    function getTradeCounts(bytes32 provider) view public returns(uint);
}

contract buyerSc {

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


    struct leakageElements {
        uint totalVolume;
        uint totalProviders;
        uint totalAgreements;
        uint totalSenstivity;
    }

    mapping(bytes32 => purchaseElements) purchaseProfile;
    bytes32[]  providersList;
    leakageElements currentImpact;

    event updateProfile(string profile);

    function updatePurchaseProfile(bytes32 _provider, uint _time, uint _samples, uint _intervalS, uint _periodS, uint _ageS, uint _type, uint _dimensions, bool _resell) public{
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


    function elementexist(uint _ele, uint[] memory array) pure internal returns(bool){
        for(uint i=0; i<array.length; i++) {
            if(_ele == array[i]) 
                return true;
        }
        return false;
    }

    function currentPossession(bytes32 provider) view public returns(uint[3] memory nontemp_purchaseProfile, uint[4][] memory) {
        uint[4][] memory temp_purchaseProfile = new uint[4][](purchaseProfile[provider].tradespecific.length);
        for (uint j = 0; j < purchaseProfile[provider].tradespecific.length; j++) {
            temp_purchaseProfile[j] = [purchaseProfile[provider].tradespecific[j].timestamp, purchaseProfile[provider].tradespecific[j].intervalScore, purchaseProfile[provider].tradespecific[j].periodScore, purchaseProfile[provider].tradespecific[j].ageScore];
        }             
        nontemp_purchaseProfile = [purchaseProfile[provider].providerSpecific.samples, purchaseProfile[provider].providerSpecific.dimensionality.length, purchaseProfile[provider].providerSpecific.diversity.length];
        return (nontemp_purchaseProfile, temp_purchaseProfile);
    }

    function getTradeCounts(bytes32 provider) view public returns(uint) {
        return purchaseProfile[provider].tradespecific.length;
    }

    function futureAcquisition(bytes32 provider) view public returns(uint[3] memory nontemp_purchaseProfile, uint[4][] memory) {
        uint[4][] memory temp_purchaseProfile = new uint[4][](purchaseProfile[provider].tradespecific.length);
        for (uint j = 0; j < purchaseProfile[provider].tradespecific.length; j++) {
            if(purchaseProfile[provider].tradespecific[j].resell){
                temp_purchaseProfile[j] = [purchaseProfile[provider].tradespecific[j].timestamp, purchaseProfile[provider].tradespecific[j].intervalScore, purchaseProfile[provider].tradespecific[j].periodScore, purchaseProfile[provider].tradespecific[j].ageScore];
            }
        }             
        nontemp_purchaseProfile = [purchaseProfile[provider].providerSpecific.resellSamples, purchaseProfile[provider].providerSpecific.dimensionality.length, purchaseProfile[provider].providerSpecific.diversity.length];
        return (nontemp_purchaseProfile, temp_purchaseProfile);     
    }
}
