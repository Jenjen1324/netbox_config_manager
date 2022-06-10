#!/usr/bin/env bash

source .env

export VAULT_ADDR='http://127.0.0.1:8200'

vault operator unseal $VAULT_UNSEAL_KEY_1
vault operator unseal $VAULT_UNSEAL_KEY_2
vault operator unseal $VAULT_UNSEAL_KEY_3


# For provisioning:
# vault secrets enable -version=2 kv
# vault secrets enable -path=secret -version=2 kv