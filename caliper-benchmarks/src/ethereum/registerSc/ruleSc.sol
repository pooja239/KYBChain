//"SPDX-License-Identifier: UNSW"
pragma experimental ABIEncoderV2;
pragma solidity ^0.5.13;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */

contract InterfaceRuleSc { 
    function getTemporalScore(uint _type, uint _interval, uint _period, uint _age) view public returns(uint[3] memory score); //
    function getNonTemporalScore(uint _sam, uint _dim, uint _div) view public returns(uint[3] memory score); //
}

contract ruleSc{


    struct temporalRule {   
        uint[2] interval;           /* seconds */
        uint[2] period;             /* seconds */
        uint[2] age;                /* seconds */
        bool exist;
    }

    struct nontemporalRule {   
        uint[2] samples;            /* numbers */
        uint[2] dimenstionality;    /* numbers */
        uint[2] diversity;          /* numbers */
        bool exist;
    }


    mapping(uint => temporalRule) datatypeSpecificScore; /* map temporal elements to data-type */

    nontemporalRule _nontemporalScore;

    constructor() public{
        uint[2] memory range;
        range[0] = 5;
        range[1] = 10;
        _nontemporalScore = nontemporalRule(range, range, range, true);
        datatypeSpecificScore[0] = temporalRule(range, range, range, true);
        datatypeSpecificScore[1] = temporalRule(range, range, range, true);
    }

    function updateTemporalScore(uint _datatype, uint[2] memory _int, uint[2] memory _per, uint[2] memory _age) public {
        
        for (uint i = 0; i < 2; i++) {
            datatypeSpecificScore[_datatype].interval[i] = _int[i];
            datatypeSpecificScore[_datatype].period[i] = _per[i];
            datatypeSpecificScore[_datatype].age[i] = _age[i];
        }
        datatypeSpecificScore[_datatype].exist = true;
    }

    function updateNonTemporalScore(uint[2] memory _sam, uint[2] memory _dim, uint[2] memory _div) public{
        for (uint i = 0; i < 2; i++) {
            _nontemporalScore.samples[i] = _sam[i];
            _nontemporalScore.dimenstionality[i] = _dim[i];
            _nontemporalScore.diversity[i] = _div[i];
        }
        _nontemporalScore.exist = true;
    }


    function getTemporalScore(uint _type, uint _interval, uint _period, uint _age) view public returns(uint[3] memory score){
        require(datatypeSpecificScore[_type].exist, "No temporal rules defined for this type");
        if(0 < _interval && _interval <= datatypeSpecificScore[_type].interval[0]) {
            score[0] = 3;
        } else if (datatypeSpecificScore[_type].interval[0] < _interval && _interval <= datatypeSpecificScore[_type].interval[1]) {
            score[0] = 2;
        } else if (datatypeSpecificScore[_type].interval[1] < _interval) {
            score[0] = 1;
        }
        if(0 < _period && _period <= datatypeSpecificScore[_type].period[0]){
            score[1] = 1;
        } else if (datatypeSpecificScore[_type].period[0] < _period && _period <= datatypeSpecificScore[_type].period[1]) {
            score[1] = 2;
        } else if (datatypeSpecificScore[_type].period[1] < _period) {
            score[1] = 3;
        }
        if(0 < _age && _age <= datatypeSpecificScore[_type].age[0]){
            score[2] = 3;
        } else if (datatypeSpecificScore[_type].age[0] < _age && _age <= datatypeSpecificScore[_type].age[1]) {
            score[2] = 2;
        } else if (datatypeSpecificScore[_type].age[1]  < _age) {
            score[2] = 1;
        }

        return score;
    }

    function getNonTemporalScore(uint _sam, uint _dim, uint _div) view public returns(uint[3] memory score){
        require(_nontemporalScore.exist, "No non-temporal rules are defined");
        if(0 < _sam && _sam <= _nontemporalScore.samples[0]) {
            score[0] = 1;
        } else if (_nontemporalScore.samples[0] < _sam && _sam <= _nontemporalScore.samples[1]) {
            score[0] = 2;
        } else if (_nontemporalScore.samples[1] < _sam) {
            score[0] = 3;
        }
        if(0 < _dim && _dim <= _nontemporalScore.dimenstionality[0]) {
            score[1] = 1;
        } else if (_nontemporalScore.dimenstionality[0] < _dim && _dim <= _nontemporalScore.dimenstionality[1]) {
            score[1] = 2;
        } else if (_nontemporalScore.dimenstionality[1] < _dim) {
            score[1] = 3;
        }        
        if(0 < _div && _div <= _nontemporalScore.diversity[0]) {
            score[2] = 1;
        } else if (_nontemporalScore.diversity[0] < _div && _div <= _nontemporalScore.diversity[1]) {
            score[2] = 2;
        } else if (_nontemporalScore.diversity[1] < _div) {
            score[2] = 3;
        }       
        return score;
    }

 }