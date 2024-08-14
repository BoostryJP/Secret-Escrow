/**
 * Copyright BOOSTRY Co., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 *
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

pragma solidity ^0.8.0;

/// @title Joux's tripartite diffie-hellmann key exchange
contract TripartiteKeyExchange {
    struct G1PublicKey {
        string g1pk_11;
        string g1pk_12;
    }
    mapping(address => G1PublicKey) public G1PK;

    struct G2PublicKey {
        string g2pk_11;
        string g2pk_12;
        string g2pk_21;
        string g2pk_22;
    }
    mapping(address => G2PublicKey) public G2PK;

    event RegisterPublicKey(address indexed account_address);

    // [CONSTRUCTOR]
    constructor() {}

    /// @notice Register public key
    function registerPublicKey(
        string memory g1pk_11,
        string memory g1pk_12,
        string memory g2pk_11,
        string memory g2pk_12,
        string memory g2pk_21,
        string memory g2pk_22
    ) public {
        G1PublicKey storage g1_pubkey = G1PK[msg.sender];
        G2PublicKey storage g2_pubkey = G2PK[msg.sender];

        g1_pubkey.g1pk_11 = g1pk_11;
        g1_pubkey.g1pk_12 = g1pk_12;

        g2_pubkey.g2pk_11 = g2pk_11;
        g2_pubkey.g2pk_12 = g2pk_12;
        g2_pubkey.g2pk_21 = g2pk_21;
        g2_pubkey.g2pk_22 = g2pk_22;

        emit RegisterPublicKey(msg.sender);
    }
}
