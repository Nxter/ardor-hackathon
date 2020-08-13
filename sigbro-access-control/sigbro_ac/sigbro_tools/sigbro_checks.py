# -*- coding: UTF-8 -*-
from .sigbro_alerts import *
from .sigbro_ardor import *
from .sigbro_mysql import *
from .sigbro_requests import *
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=2, width=120)

PUBLIC_KEY = environ.get("PUBLIC_KEY", "68d3dccd1bd854c88fdef5d072c97591a26d8ba05615fd3f5d7ef31a83a2843a")
SIGNER_BASEURL = environ.get("SIGNER_BASEURL", "https://sigbro-signer.api.nxter.org")
SIGNER_TOKEN = environ.get('SIGNER_TOKEN', '1234567890') # sigbro_signer_access_token from Ansible

req = sigbroRequests()

CHAINS = [
    {"name": "ARDR", "decimals": 100000000, "chain": 1},
    {"name": "IGNIS", "decimals": 100000000, "chain": 2},
    {"name": "AEUR", "decimals": 10000, "chain": 3},
    {"name": "BITSWIFT", "decimals": 100000000, "chain": 4},
    {"name": "MPG", "decimals": 100000000, "chain": 5},
]


def __get_decimals( chain: int):
    for cc in CHAINS:
        if int(cc["chain"]) == chain:
            return int(cc["decimals"])
    return 100000000


def __get_chain_name(chain: int):
    for cc in CHAINS:
        if int(cc["chain"]) == chain:
            return cc["name"]
    return "Unknown chain"


def check_block_for_alerts(block, alerts, network, debug):
    
    # check transactions from block if they exists
    if int(block["numberOfTransactions"]) > 0:
        
        for tx in block["transactions"]:
            
            # this is an ARDOR block. We do not check it, just Ignis tx
            if "attachment" in tx and "childTransactionFullHashes" in tx["attachment"] and len(tx["attachment"]["childTransactionFullHashes"]) > 0:
                ctxs = tx["attachment"]["childTransactionFullHashes"]
                chain = int(tx["attachment"]["chain"])
                
                # check only IGNIS
                if chain != 2:
                    break

                ardor = sigbroArdor(network=network)
                for ctx in ctxs:
                    child_tx = ardor.getTransaction(fullHash=ctx, chain=chain)
                    if child_tx:
                        
                        senderRS = None
                        recipientRS = None
                        type = None
                        subtype = None
                        chain = None
                        amountNQT = None
                        amount = None
            
                        if "senderRS" in child_tx:
                            senderRS = child_tx["senderRS"]
                        if "recipientRS" in child_tx:
                            recipientRS = child_tx["recipientRS"]
                        if "type" in child_tx:
                            type = child_tx["type"]
                        if "subtype" in child_tx:
                            subtype = child_tx["subtype"]
                        if "chain" in child_tx:
                            chain = child_tx["chain"]
                        if "amountNQT" in child_tx:
                            amountNQT = child_tx["amountNQT"]
                            
                        log.debug(msg='check_block_for_alerts', sender=senderRS, recipient=recipientRS, type=type, subtype=subtype, amount=amountNQT)
                        
                        if senderRS not in alerts and recipientRS in alerts and chain == 2 and type == 0 and subtype == 0:
                            # this is Ignis and Ordinary Payment
                            # we have incoming transaction not from ourself
                            if debug:
                                log.debug(msg="found suitable transaction ^^^")
                                
                            try:
                                amount = int(int(amountNQT) / __get_decimals(chain))
                            except:
                                amount = 0
                                pass
                            
                            if amount > 0:
                                check_and_update_status(senderRS=senderRS, amount=amount, network=network, debug=debug)


def check_and_update_status(network:str, senderRS: str, amount: int, debug: bool):
    """
    check account and increase the status if possible
    """
    status = None
    if amount < 1:
        status = None
    elif  amount < 10:
        status = 'member'
    elif amount < 50:
        status = 'silver'
    elif amount < 250:
        status = 'gold'
    else:
        status = 'platinum'
        
    if status == None:
        log.debug(msg="Strange user", network=network, sender=senderRS, amount=amount, status=status)
        return
        
    
    current_status = acl_accounts.get_or_none( acl_accounts.network == network, acl_accounts.accountRS == senderRS)
    
    if current_status == None:
        # new user!!
        log.info(msg="New user!", network=network, sender=senderRS, amount=amount, status=status)
        acl_accounts.create(network=network, accountRS=senderRS, status=status, timestamp=datetime.utcnow().strftime("%s"))
        set_property_to_the_user(network=network, account=senderRS, status=status)
    elif current_status.status == 'member' and status != 'member':
        log.info(msg="User increased his status!", network=network, sender=senderRS, amount=amount, old_status=current_status.status, status=status)
        acl_accounts.replace(network=network, accountRS=senderRS, status=status, timestamp=datetime.utcnow().strftime("%s")).execute()
        set_property_to_the_user(network=network, account=senderRS, status=status)
    elif current_status.status == 'silver' and ( status == 'gold' or status == 'platinum' ):
        log.info(msg="User increased his status!", network=network, sender=senderRS, amount=amount, old_status=current_status.status, status=status)
        acl_accounts.replace(network=network, accountRS=senderRS, status=status, timestamp=datetime.utcnow().strftime("%s")).execute()
        set_property_to_the_user(network=network, account=senderRS, status=status)
    elif current_status.status == 'gold' and status == 'platinum':
        log.info(msg="User become a platinum user!", network=network, sender=senderRS, amount=amount, old_status=current_status.status, status=status)
        acl_accounts.replace(network=network, accountRS=senderRS, status=status, timestamp=datetime.utcnow().strftime("%s")).execute()
        set_property_to_the_user(network=network, account=senderRS, status=status)
    else:
        log.info(msg="User keep the same status!", network=network, sender=senderRS, amount=amount, old_status=current_status.status, status=status)
        acl_accounts.replace(network=network, accountRS=senderRS, status=status, timestamp=datetime.utcnow().strftime("%s")).execute()
        set_property_to_the_user(network=network, account=senderRS, status=status)

def sign_tx(network: str, tx: dict):
    """ send tx to signer """
    url = f"{SIGNER_BASEURL}/api/v1/sign"
    header = {'X-Sigbro-Token': SIGNER_TOKEN}
    rez = req.post(url=url, params=tx, headers=header)
    pp.pprint(rez)
    
def set_property_to_the_user(network: str, account: str, status: str):
    """ try to make a tx for signer """
    ardr = sigbroArdor(network=network)
    tx = ardr.setAccountProperty(chain=2, recipient=account, publicKey=PUBLIC_KEY, property='sigbro', value=status)
    if tx and 'errorCode' in tx:
        log.error(msg=tx['errorDescription'], network=network, account=account, status=status)
        msg = f"{tx['errorDescription']}\nnetwork={network}\naccount={account}\nstatus={status}"
        send_alert_to_telegram(message=msg)
    else:
        sign_tx(network=network, tx=tx)


    
