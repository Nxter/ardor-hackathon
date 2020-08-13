"""Basic communication with ARDOR blockchain"""
# -*- coding: UTF-8 -*-

from .sigbro_requests import sigbroRequests
from .sigbro_logs import sigbroLogs

log = sigbroLogs()


class sigbroArdor:
    """SIGBRO ARDOR"""

    req = None
    network = "mainnet"
    blockchain = None

    def __init__(self, network: str = "mainnet"):
        """Initialization"""
        self.req = sigbroRequests()
        self.network = network
        if self.network == "mainnet":
            self.blockchain = "https://random.api.nxter.org/ardor"
        else:
            self.blockchain = "https://random.api.nxter.org/tstardor"

    def getLastBlockHeight(self):
        """Get last block height from blockchain"""
        url = f"{self.blockchain}?requestType=getBlock"
        rez = self.req.get(url)

        if rez and rez["height"]:
            return rez["height"]
        else:
            return -1

    def getBlock(self, height: int):
        """Get block info."""
        url = f"{self.blockchain}?requestType=getBlock&height={height}&includeTransactions=True&includeExecutedPhased=True"
        rez = self.req.get(url)

        if rez and "generatorRS" in rez:
            return rez
        else:
            return False

    def getTransaction(self, fullHash: str, chain: int):
        """Get block info."""
        url = f"{self.blockchain}?requestType=getTransaction&fullHash={fullHash}&chain={chain}"
        rez = self.req.get(url)

        if rez and "fullHash" in rez:
            return rez
        else:
            return False

    def getVoterPhasedTransactions(self, accountRS: str):
        """get voter phased transactions for all child chains"""
        response = list()

        for chain in range(2, 6):
            # from childchain 2 to 5
            url = f"{self.blockchain}?requestType=getVoterPhasedTransactions&account={accountRS}&chain={chain}&firstIndex=0&lastIndex=10"
            rez = self.req.get(url)
            if rez and "transactions" in rez and len(rez["transactions"]) > 0:
                for tx in rez["transactions"]:
                    response.append(tx)

        return response

    def getAssetPhasedTransactions(self, asset: str) -> list:
        """get assets approval for every childchain"""
        response = list()

        for chain in range(2, 6):
            # from childchain 2 to 5
            url = f"{self.blockchain}?requestType=getAssetPhasedTransactions&asset={asset}&chain={chain}&withoutWhitelist=true&firstIndex=0&lastIndex=20"
            rez = self.req.get(url)
            if rez and "transactions" in rez and len(rez["transactions"]) > 0:
                for tx in rez["transactions"]:
                    response.append(tx)

        return response

    def getAsset(self, asset: str):
        """Get asset info."""
        url = f"{self.blockchain}?requestType=getAsset&asset={asset}"
        rez = self.req.get(url)

        if rez and "name" in rez:
            return rez
        else:
            log.error(msg=f"Cannot get asset info [ asset = {asset} ]", error=rez)
            return False

    def getAccountAssets(self, account: str) -> dict:
        url = f"{self.blockchain}?requestType=getAccountAssets&account={account}&includeAssetInfo=true"
        rez = self.req.get(url)

        if rez and "accountAssets" in rez:
            return rez
        else:
            log.error(msg="Cannot scrape for assets", error=rez)
            return False

    def setAccountProperty(self, chain: int, recipient: str, publicKey: str, property: str, value: str):
        """
        
        :param chain:  2 for Ignis
        :param recipient:  accountRS
        :param publicKey: publicKey for sender
        :param property: sigbro
        :param value: member/silver/gold/platinum
        :return: response
        """
        url = f"{self.blockchain}?requestType=setAccountProperty"
        params = {
            'chain':chain,
            'recipient': recipient,
            'publicKey': publicKey,
            'feeNQT': -1,
            'deadline': 120,
            'broadcast': False,
            'property': property,
            'value': value
        }
        
        rez = self.req.post(url=url, params=params, encoded='www')
        return rez


        
        