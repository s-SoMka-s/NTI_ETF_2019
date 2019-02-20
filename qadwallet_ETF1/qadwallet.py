#!/usr/bin/env python

from web3 import Web3, HTTPProvider
from eth_account import Account
import sys
import math

### Put your code below this comment ###
#1
url = "https://sokol.poa.network"
w3 = Web3(HTTPProvider(url))


def norm_balance(balance):
    n = 0
    num = balance
    while True:
        n += 1
        num /= 1000
        if math.trunc(num) == 0:
            n -= 1
            break

    balance /= 10 ** (3*n)
    balance = round(balance,6)

    balance_str = str(balance)
    while True:
        if balance_str[len(balance_str)-1] == 0:
            del(balance_str[len(balance_str)-1])
        else:
            break
    type = ""
    if n == 0:
        type = " wei"
    elif n == 1:
        type = " kwei"
    elif n == 2:
        type = " mwei"
    elif n == 3:
        type = " gwei"
    elif n == 4:
        type = " szabo"
    elif n == 5:
        type = " finney"
    else:
        type = " poa"
    res = balance_str + type
    return res


def get_acct(pKey):
    acct = Account.privateKeyToAccount(pKey)
    address = acct.address
    return acct


def get_balance(pKey):
    acct = get_acct(pKey)
    balance = w3.eth.getBalance(acct.address)
    print_str = 'Balance on ' + '"' + acct.address.replace("0x", "") + '"' + ' is ' + norm_balance(balance)
    print(print_str)


def send_tx(sender_pKey, recipient, val):
    recipient = "0x" + recipient
    sender = get_acct(sender_pKey)
    value = int(val)
    transaction = {
        "to": recipient,
        "value": value,
        "gas": 21000,
        "gasPrice": 1000000000,
        "nonce": w3.eth.getTransactionCount(sender.address)
    }
    signed = sender.signTransaction(transaction)
    try:
        hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    except ValueError:
        print("No enough funds for payment")
    else:
        res = "Payment of " + norm_balance(value) + " to "
        res += '"' + recipient.replace("0x", "") + '"'
        res += " scheduled"
        print(res)
        res2 = "Transaction Hash: " + str(hash.hex())
        print(res2)


def check_tx(tx_hash):
    obj = w3.eth.getTransaction(tx_hash)
    if obj == None:
        print("No such transaction in the chain")
    else:
        bl_hash = obj.blockHash
        if bl_hash == None:
            res = "Delay in payment of "
            val = norm_balance(obj.value)
            res = res + val + ' to "' + obj.to.replace("0x", "") + '"'
        else:
            res = "Payment of "
            val = norm_balance(obj.value)
            res = res + val + ' to "' + obj.to.replace("0x", "") + '"' + " confirmed"
        print(res)


if sys.argv[1] == "--key" and len(sys.argv) == 3:
    get_balance(sys.argv[2])
elif sys.argv[1] == "--tx":
    check_tx(sys.argv[2])
elif len(sys.argv) == 7 and sys.argv[3] == "--to" and sys.argv[5] == "--value":
    send_tx(sys.argv[2], sys.argv[4], sys.argv[6])
