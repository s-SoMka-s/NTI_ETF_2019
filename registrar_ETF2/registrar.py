#!/usr/bin/env python
#
import requests
import json
from json import load
from web3 import Web3, HTTPProvider
import sys
w3 = Web3(HTTPProvider("https://sokol.poa.network"))
gas = json.loads(requests.get("https://gasprice.poa.network").content)["fast"]*1000000000
with open('account.json') as file:
    account_config = load(file)
with open("MyContract.bin") as bin_file:
    bytecode = bin_file.read()

with open("MyContract.abi") as abi_file:
    abi = json.loads(abi_file.read())
account = w3.eth.account.privateKeyToAccount(account_config["account"])
contract = w3.eth.contract(abi=abi, bytecode=bytecode)


def delete():
    with open("database.json") as file:
        contractAdress = load(file)["registrar"]
    contract_by_address = w3.eth.contract(address=contractAdress, abi=abi)
    data = contract_by_address.functions.getOwnerName().call()
    if data == "":
        print("No name found for your account")
        return
    else:
        tx_wo_sign = contract_by_address.functions.delOwnerName().buildTransaction({
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 400000,
            'gasPrice': int(gas)
        })

        signed_tx = account.signTransaction(tx_wo_sign)
        try:
            txId = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        except ValueError:
            print("No enough funds to delete name")
        else:
            data = contract_by_address.functions.getOwnerName().call()
            txReceipt = w3.eth.waitForTransactionReceipt(txId)
            if txReceipt["status"] == 1:
                print("Successfully deleted by " + str(txId.hex()))


def deploy():
    tx_wo_sign = contract.constructor().buildTransaction({
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 400000,
        'gasPrice': int(gas)
    })

    signed_tx = account.signTransaction(tx_wo_sign)
    txId = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    txReceipt = w3.eth.waitForTransactionReceipt(txId)

    print("Contract address: " + txReceipt['contractAddress'])
    with open("database.json", "x") as file:
        file.write(json.dumps({
            "registrar": txReceipt['contractAddress'],
            "startBlock": txReceipt['blockNumber']}))
    with open("database.json") as file:
        contractAdress = load(file)["registrar"]
    contract_by_address = w3.eth.contract(address=contractAdress, abi=abi)
    tx_wo_sign = contract_by_address.functions.setOwnerAddress(account.address).buildTransaction({
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 400000,
        'gasPrice': int(gas)
    })

    signed_tx = account.signTransaction(tx_wo_sign)
    txId = w3.eth.sendRawTransaction(signed_tx.rawTransaction)


def add(name):
        with open("database.json") as file:
            contractAdress = load(file)["registrar"]
        contract_by_address = w3.eth.contract(address=contractAdress, abi=abi)
        data = contract_by_address.functions.getOwnerName().call()
        if data == "":
            tx_wo_sign = contract_by_address.functions.setOwnerName(name).buildTransaction({
                'from': account.address,
                'nonce': w3.eth.getTransactionCount(account.address),
                'gas': 400000,
                'gasPrice': int(gas)
            })

            signed_tx = account.signTransaction(tx_wo_sign)
            try:
                txId = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            except ValueError:
                print("No enough funds to add name")
            else:
                txReceipt = w3.eth.waitForTransactionReceipt(txId)
                if txReceipt["status"] == 1:
                    print("Successfully added by " + str(txId.hex()))
        else:
            print("One account must correspond one name")


def getacc(name):
    with open("database.json") as file:
        contractAdress = load(file)["registrar"]
    contract_by_address = w3.eth.contract(address=contractAdress, abi=abi)
    data = contract_by_address.functions.getOwnerName().call()
    if name == data:
        print(account.address)
    else:
        print("No account registered for this name")


if sys.argv[1] == "--deploy":
    deploy()
elif sys.argv[1] == "--add":
    add(str(sys.argv[2]))
elif sys.argv[1] == "--del":
    delete()
elif sys.argv[1] == "--getacc":
    getacc(sys.argv[2])


