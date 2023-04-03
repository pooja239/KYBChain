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
    constructor(workerIndex, subscriptionsperbuyer, buyers = 0, subscriptions = 0) {
        this.buyersGenerated = buyers;
        this.subscriptionsperBuyer = subscriptionsperbuyer;
        this.subscriptionsGenerated = subscriptions;
    }

    getcreateProfile() {
        const web3 = new Web3;
        this.buyersGenerated++;
        let buyer = "Buyer" + this.buyersGenerated;
        let buyerID = web3.utils.soliditySha3(web3.eth.abi.encodeParameters(['string'],[buyer]));
        return {
            buyer: buyerID
        };

    }

    getupdateProfile() {  
        const web3 = new Web3;
        var x = this.subscriptionsGenerated % this.subscriptionsperBuyer;
        if (x === 0) {
            this.buyersGenerated++;
        }
        let buyer = "Buyer" + this.buyersGenerated;
        let buyerID = web3.utils.soliditySha3(web3.eth.abi.encodeParameters(['string'],[buyer]));
        let seller = "Seller"
        let sellerID = web3.utils.soliditySha3(web3.eth.abi.encodeParameters(['string'],[seller]));
        this.subscriptionsGenerated++;
        return {
            buyer: buyerID,
            time: 1,
            samples: 1,
            seller: sellerID,
            interval: 1,
            period: 1,
            age: 1,
            type: 1,
            dimensions: 1,
            resell: true
        };

    }
   
}

module.exports = SimpleState;
