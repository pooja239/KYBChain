// SPDX-License-Identifier: UNSW
pragma solidity ^0.8.9;
pragma abicoder v2;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */

interface InterfaceRuleSc { 
	function getTemporalScore(uint _type, uint _interval, uint _period, uint _age) view external returns(uint[3] memory score); //
    function getNonTemporalScore(uint _sam, uint _dim, uint _div) view external returns(uint[3] memory score); //
    function getLikelihood(uint RS, int DS) view external returns(uint LL);
    function getImpactScore(uint _vol, uint _prov, uint _agree, uint _sens) view external returns(uint[4] memory score); //
}

contract RuleSc{


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

    struct likelihoodRule {
        uint RSlowDSlowRISKvhigh;
	    uint RSlowDShighRISKhigh;
	    uint RShighDSlowRISKlow;
        uint RShighDShighRISKvlow;
        bool exist;
    }

    struct impactRule {
        uint[2] volume;
        uint[2] providers;
        uint[2] agreements;
        bool exist;
    }

    mapping(uint => temporalRule) datatypeSpecificScore; /* map temporal elements to data-type */

    likelihoodRule _leakageLikelihood;
    impactRule _impactRule;
    nontemporalRule _nontemporalScore;

    constructor(){
        uint[2] memory range;
        range[0] = 5;
        range[1] = 10;
        _leakageLikelihood = likelihoodRule(80, 60, 40, 20, true);
        _impactRule = impactRule(range, range, range, true);
        _nontemporalScore = nontemporalRule(range, range, range, true);
        datatypeSpecificScore[0] = temporalRule(range, range, range, true);
        datatypeSpecificScore[1] = temporalRule(range, range, range, true);
    }

    function updateTemporalScore(uint _datatype, uint[2] memory _int, uint[2] memory _per, uint[2] memory _age) external {
        
        for (uint i = 0; i < 2; i++) {
            datatypeSpecificScore[_datatype].interval[i] = _int[i];
            datatypeSpecificScore[_datatype].period[i] = _per[i];
            datatypeSpecificScore[_datatype].age[i] = _age[i];
        }
        datatypeSpecificScore[_datatype].exist = true;
    }

    function updateNonTemporalScore(uint[2] memory _sam, uint[2] memory _dim, uint[2] memory _div) external{
        for (uint i = 0; i < 2; i++) {
            _nontemporalScore.samples[i] = _sam[i];
            _nontemporalScore.dimenstionality[i] = _dim[i];
            _nontemporalScore.diversity[i] = _div[i];
        }
        _nontemporalScore.exist = true;
    }

    function updateLikelihood(uint vhigh, uint high, uint low, uint vlow) external{
        _leakageLikelihood = likelihoodRule(vhigh, high, low, vlow, true);
    }

    function updateImpactScore(uint[2] memory _vol, uint[2] memory _prov, uint[2] memory _agree) external{
        for (uint i = 0; i < 2; i++) {
            _impactRule.volume[i] = _vol[i];
            _impactRule.providers[i] = _prov[i];
            _impactRule.agreements[i] = _agree[i];
           
        }
         _impactRule.exist = true;
    }

    function getTemporalScore(uint _type, uint _interval, uint _period, uint _age) view external returns(uint[3] memory score){
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

    function getNonTemporalScore(uint _sam, uint _dim, uint _div) view external returns(uint[3] memory score){
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

    function getLikelihood(uint RS, int DS) view external returns(uint LL){
        require(_leakageLikelihood.exist, "No Likelihood rules are defined");
        if(RS <= 50 && DS <= 0) {
            return _leakageLikelihood.RSlowDSlowRISKvhigh;
        } else if (RS <= 50 && DS > 0) {
            return _leakageLikelihood.RSlowDShighRISKhigh;
        } else if(RS > 50 && DS <= 0) {
            return _leakageLikelihood.RShighDSlowRISKlow;
        } else if (RS > 50 && DS > 0) {
            return _leakageLikelihood.RShighDShighRISKvlow;
        }
    }


    function getImpactScore(uint _vol, uint _prov, uint _agree, uint _sens) view external returns(uint[4] memory score){
        require(_nontemporalScore.exist, "No non-temporal rules are defined");
        if(0 < _vol && _vol <= _impactRule.volume[0]) {
            score[0] = 1;
        } else if (_impactRule.volume[0] < _vol && _vol <= _impactRule.volume[1]) {
            score[0] = 2;
        } else if (_impactRule.volume[1] < _vol ) {
            score[0] = 3;
        }
        if(0 < _prov && _prov <= _impactRule.providers[0]) {
            score[1] = 1;
        } else if (_impactRule.providers[0] < _prov && _prov <= _impactRule.providers[1]) {
            score[1] = 2;
        } else if (_impactRule.providers[1] < _prov) {
            score[1] = 3;
        }
        if(0 < _agree && _agree <= _impactRule.agreements[0]) {
            score[2] = 1;
        } else if (_impactRule.agreements[0] < _agree && _agree <= _impactRule.agreements[1]) {
            score[2] = 2;
        } else if (_impactRule.agreements[1] < _agree) {
            score[2] = 3;
        }
        score[3] = _sens;
        return score;
    }
 }