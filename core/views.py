from django.shortcuts import render, get_object_or_404, redirect, reverse
from web3 import Web3
from . import contract
from .models import Contract, Account
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


def home(request):
    print(w3.personal.listAccounts)
    return render(request, 'home.html')


def etherf(request):
    w3.personal.unlockAccount(w3.eth.accounts[0], "presto")
    contract.mining()
    return redirect(reverse("core:account_info", args=[0]))



def create_account(request):
    created_account = w3.personal.newAccount('presto')
    Account.objects.create(
        address= created_account
    )
    csv = {"address": created_account}
    return render(request, 'account_info.html',csv)


def account_info(request, pk=0):
    account = w3.eth.accounts[pk]
    balance = w3.eth.getBalance(account)
    presto = Contract.objects.get(pk=1).address
    abi = contract.get_abi('./core/Presto.sol', "PrestoToken")['abi']
    presto_contract = w3.eth.contract(
       address=presto,
       abi=abi
    )
    token = presto_contract.functions.balanceOf(account).call
    csv = {
        "address": account,
        "balance": balance,
        "token": token
    }

    return render(request, 'account_info.html', csv)


def deploy(request):
    new_contract = contract.deploy('./core/Presto.sol', "PrestoToken")
    address = new_contract.address
    creator = new_contract.creator
    abi = new_contract.abi
    csv = {'address': address, 'creator': creator, "abi": abi}
    return render(request, 'contract_info.html', csv)


def send_token(request):
    accounts = w3.eth.accounts
    csv = {'accounts': accounts}

    if request.method == "POST":
        account = Account.objects.get(address=request.POST.get('address')).address
        balance = w3.eth.getBalance(account)
        presto = Contract.objects.get(pk=1).address
        abi = contract.get_abi('./core/Presto.sol', "PrestoToken")['abi']
        presto_contract = w3.eth.contract(
            address=presto,
            abi=abi
        )
        token = presto_contract.functions.balanceOf(account).call()
        csv = {
            "address": account,
            "balance": balance,
            "token": token
        }
        return render(request, 'account_info_ajax.html', csv)

    return render(request, 'sendtoken.html', csv)


def send_eth(request):
    if request.method == "POST":
        from_account = request.POST.get('from')
        to_account = request.POST.get('to')
        value = int(request.POST.get('value'))
        # 코인베이스 변경
        w3.miner.setEtherbase = from_account
        w3.personal.unlockAccount(from_account, "presto")

        w3.eth.sendTransaction({'to': to_account, 'from': from_account, 'value': value})
        contract.mining()

    accounts = w3.eth.accounts
    csv = {'accounts': accounts}
    return render(request, 'sendtoken.html', csv)


def send_presto(request):
    if request.method == "POST":
        from_account = request.POST.get('from')
        to_account = request.POST.get('to')
        value = int(request.POST.get('value'))
        print(w3.isChecksumAddress(to_account))
        # 코인베이스 변경
        w3.miner.setEtherbase = from_account
        w3.personal.unlockAccount(from_account, "presto")

        presto = Contract.objects.get(pk=1).address
        abi = contract.get_abi('./core/Presto.sol', "PrestoToken")['abi']
        presto_contract = w3.eth.contract(
            address=presto,
            abi=abi
        )
        print(presto_contract.all_functions())
        presto_contract.functions.transfer(to_account, value).transact({'from':from_account})
        contract.mining()

    accounts = w3.eth.accounts
    csv = {'accounts': accounts}
    return render(request, 'sendtoken.html', csv)