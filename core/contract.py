import time
from web3 import Web3, HTTPProvider
from logzero import logger
from solc import compile_files
from .models import Contract

rpc_url = "http://localhost:8545"
w3 = Web3(HTTPProvider(rpc_url))
w3.personal.unlockAccount(w3.eth.accounts[0], "presto", 0)


def mining():
    w3.personal.unlockAccount(w3.eth.coinbase, "presto", 0)
    w3.miner.start(1)
    time.sleep(5)
    w3.miner.stop()


def get_abi(contract_file_name, contract_name):
    compiled_sol = compile_files([contract_file_name])
    interface = compiled_sol['{}:{}'.format(contract_file_name,
                                            contract_name)]

    return interface


def deploy(contract_file_name, contract_name):
    w3.personal.unlockAccount(w3.eth.accounts[0], "presto", 0)
    compiled_sol = compile_files([contract_file_name])
    interface = compiled_sol['{}:{}'.format(contract_file_name,
                                            contract_name)]

    contract = w3.eth.contract(abi=interface['abi'],
                               bytecode=interface['bin'],
                               bytecode_runtime=interface['bin-runtime'])

    #Deploy
    tx_hash = contract.deploy(transaction={"from": w3.eth.accounts[0]})

    logger.info("tx_hash: {}".format(tx_hash))

    #Mining
    mining()

    # contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print(tx_receipt)
    contract_address = tx_receipt['contractAddress']
    logger.info("contract_address:{}".format(contract_address))
    # use contract
    contract_instance = contract(contract_address)
    new_contract = Contract.objects.create(
        address=contract_address,
        creator=tx_receipt['from'],
        abi=interface['abi']
    )

    return new_contract
