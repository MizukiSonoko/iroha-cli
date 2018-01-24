#!/bin/bash

#
# Copyright 2018 Takeshi Yonezu. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# Change localhost to Iroha's real IP address
IROHA_HOST=localhost:50051
CREATOR_ID=admin@test

function send {
  echo "=== $* ==="
  read junk

  docker run -t --rm --name irohac -v $(pwd):/root/.irohac hyperledger/irohac irohac --hostname=${IROHA_HOST} --account_id=${CREATOR_ID} $*
}

send CreateDomain --default_role user --domain_id iroha

send CreateAsset --asset_name usd --domain_id iroha

send GetAssetInfo --asset_id usd#iroha

send CreateAccount --account_name alice --domain_id iroha --main_pubkey 359f925e4eeecfdd6aa1abc0b79a6a121a5dd63bb612b603247ea4f8ad160156

send GetAccount --account_id alice@iroha

send CreateAccount --account_name bob --domain_id iroha --main_pubkey 59f925e4eeecfdd6aa1abc0b79a6a121a5dd63bb612b603247ea4f8ad160156

send GetAccount --account_id bob@iroha

send AddAssetQuantity --account_id alice@iroha --asset_id usd#iroha --amount 200

send GetAccountAssets --account_id alice@iroha --asset_id usd#iroha

send AddAssetQuantity --account_id bob@iroha --asset_id usd#iroha --amount 100

send GetAccountAssets --account_id bob@iroha --asset_id usd#iroha

send TransferAsset --src_account_id bob@iroha --dest_account_id alice@iroha --asset_id usd#iroha --description Transfer_Asset --amount 20

send GetAccountAssets --account_id alice@iroha --asset_id usd#iroha
send GetAccountAssets --account_id bob@iroha --asset_id usd#iroha

exit 0
