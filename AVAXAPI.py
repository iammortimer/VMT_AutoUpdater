# -------------------------------- LIBRARIES -------------------------------- #
from web3 import Web3
from web3.middleware import geth_poa_middleware
import Config as config

# ------------------------------- MAIN CLASS -------------------------------- #
class AvalancheAPI(object):
# ------------------------------- INITIALIZE -------------------------------- #
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(config.AVAX_RPC_URL))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.spend = self.web3.toChecksumAddress(config.WAVAX_ADDRESS)
        self.start_balance = self.getBalance()
        self.contractdolla = self.web3.eth.contract(address=self.web3.toChecksumAddress(config.DOLLA_CONTRACT_ADRESS), abi=config.DOLLA_ABI)
        self.contractbiz = self.web3.eth.contract(address=self.web3.toChecksumAddress(config.BIZ_CONTRACT_ADRESS), abi=config.BIZ_ABI)
        self.contractvmt = self.web3.eth.contract(address=self.web3.toChecksumAddress(config.VMT_CONTRACT_ADRESS), abi=config.VMT_ABI)
        print('Starting Balance (AVAX): ', self.start_balance)

# ---------------------------------- UTILS ---------------------------------- #
    def getBalance(self):  # Get AVAX balance
        return self.web3.fromWei(self.web3.eth.get_balance(config.SENDER_ADDRESS), 'ether')

    def getNonce(self):  # Get address nonce
        return self.web3.eth.get_transaction_count(config.SENDER_ADDRESS)

    def get_token_info(self, token_address): # Get symbol and decimal count from contract address
        contract_id = self.web3.toChecksumAddress(token_address)
        sell_token_contract = self.web3.eth.contract(contract_id, abi=config.SELL_ABI)
        symbol = sell_token_contract.functions.symbol().call()
        decimals = sell_token_contract.functions.decimals().call()
        return symbol, decimals

    def get_token_holdings(self, token_address): # Get amount of tokens hold and value(in AVAX) of these tokens
        contract_id = self.web3.toChecksumAddress(token_address)
        sell_token_contract = self.web3.eth.contract(contract_id, abi=config.SELL_ABI)

        balance = sell_token_contract.functions.balanceOf(config.SENDER_ADDRESS).call()  # How many tokens do we have?
        return balance
        
# --------------------------------- VMTycoon --------------------------------- #
    def getTycoonIds(self):
        balance = self.contractvmt.functions.balanceOf(config.SENDER_ADDRESS).call()
        
        Tycoons = []
        if balance > 0:
            for i in range(0, balance):
                TycoonID = self.contractvmt.functions.tokenOfOwnerByIndex(config.SENDER_ADDRESS, i).call()
                Tycoons.append(TycoonID)
                
        return Tycoons
                
    def getLevelInfo(self, level):
        reqDolla= self.contractbiz.functions.dollaLevelingRate(level).call()
        
        return reqDolla

    def getTycoonInfo(self, tid):
        myTycoon= self.contractbiz.functions.stakedVMTycoon(tid).call()
        
        return myTycoon
        
    def addDolla(self, tid, amount):
        sender = self.web3.toChecksumAddress(config.SENDER_ADDRESS)
        nonce = self.web3.eth.get_transaction_count(sender)
        
        approve = self.contractdolla.functions.equipVMTycoon(vmtycoonId = tid, amount = amount).buildTransaction({
            'from': sender,
            'nonce': nonce
        })
        signed_txn = self.web3.eth.account.sign_transaction(approve, private_key=config.PRIVATE_KEY)
        tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx = self.web3.toHex(tx_token)
        return tx
        
    def lvlTycoon(self, tid):
        sender = self.web3.toChecksumAddress(config.SENDER_ADDRESS)
        nonce = self.web3.eth.get_transaction_count(sender)
        
        approve = self.contractbiz.functions.levelUpVMTycoon(tid = tid).buildTransaction({
            'from': sender,
            'nonce': nonce
        })
        signed_txn = self.web3.eth.account.sign_transaction(approve, private_key=config.PRIVATE_KEY)
        tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx = self.web3.toHex(tx_token)
        return tx
