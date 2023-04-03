/*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

'use strict';

const Dictionary = 'abcdefghijklmnopqrstuvwxyz';
const Web3 = require("web3");

/**
 * Class for managing simple account states.
 */
class SimpleState {

    /**
     * Initializes the instance.
     */
    constructor(workerIndex, privacyRatingSc, numberOfBuyers) {
        this.privacyRatingSc = privacyRatingSc;
        this.buyersGenerated = numberOfBuyers;
        this.subscriptionsGenerated = 0;
        this.indexGenerated = 0;
    }

    getinitaddress() {
        return {
            paymentRatingScAddress: this.privacyRatingSc,
        };
    }

    getregisterBuyer() {
        this.indexGenerated++;
        let user = "Buyer" + this.indexGenerated;
        return {
            username: user,
            role: 1,
            balance: 100000000
        };
    }

    getregisterSeller() {
        this.indexGenerated++;
        let user = "Seller" + this.indexGenerated;
        //let user = "Seller"
        return {
            username: user,
            _role: 0,
            _balance: 100000000
        };
    }

    getregisterAgreement() {
        this.indexGenerated++;
        let seller = "Seller" + this.indexGenerated;
        let buyer = "Buyer" + this.indexGenerated;
        const web3 = new Web3;
        let AID = web3.utils.soliditySha3(web3.eth.abi.encodeParameters(['string','string'],[buyer, seller]));

        return {
            _seller: seller,
            _buyer: buyer
        };
    }

    getaddSubscription(index) {
        let seller = "Seller" + index;
        let buyer = "Buyer" + index;
        this.subscriptionsGenerated++;
        const web3 = new Web3;
        let AID = web3.utils.soliditySha3(web3.eth.abi.encodeParameters(['string','string'],[buyer, seller]));
        //console.log(">>>>>>>>>>>>>>>>" + buyer + "   " + seller)
        //console.log(">>>>>>>>>>>>>>>>" + this.subscriptionsGenerated)
        return {
            _AID: AID,
            time: 1,
            dataType: 1,
            interval: 1,
            period: 1,
            age: 1,
            samples: 1,
            dim: 1,
            price: 1,
            resell: true
        };
    }


    getconfirmDelivery(index) {
        let seller = "Seller" + index;
        let buyer = "Buyer" + index;
        const web3 = new Web3;
        let SID = web3.utils.soliditySha3(this.subscriptionsGenerated);
        let AID = web3.utils.soliditySha3(web3.eth.abi.encodeParameters(['string','string'],[buyer, seller]));
        //console.log(">>>>>>>>>>>>>>>>" + buyer + "   " + seller)
        //console.log(">>>>>>>>>>>>>>>>" + this.subscriptionsGenerated)
        this.subscriptionsGenerated++;
        return {
            _buyer: buyer,
            _AID: AID,
            _SID: SID
        };
    }

    getretrieveProfiles() {
	let min = 1;
	let max = this.buyersGenerated;
        let indexGenerated =  Math.floor(Math.random() * (max - min + 1) + min);
	//let rand = Math.random() * this.buyersGenerated;
        //let indexGenerated = Math.floor(rand);
        let buyer = "Buyer"+indexGenerated.toString();
        //console.log(">>> " + buyer);
        //let buyer = "Buyer1"; 
	let seller = "Seller";
        return {
            _buyer: buyer,
            _seller: seller
        };
    } 
}

module.exports = SimpleState;
