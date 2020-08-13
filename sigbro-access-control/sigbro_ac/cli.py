# -*- coding: UTF-8 -*-

import click
import sentry_sdk
from sigbro_ac.sigbro_tools import *


log = sigbroLogs()
req = sigbroRequests()

### Init Sentry
SENTRY_INIT = environ.get("SENTRY_INIT", "")
if len(SENTRY_INIT) > 10 :
    sentry_sdk.init(SENTRY_INIT)


@click.group()
def cli():
    """Scan Nxt or Ardor network for new events."""

@cli.command(name="init_db")
@click.option("-r", "--rewind", help="Rewind for several blocks back", type=int, default=0)
@click.option("-h", "--height", help="Set specific hight of blockchain", type=int, default=0)
@click.option("--network", help="mainnet or testnet for scan", type=str, default="mainnet")
def initialize_db(rewind, height, network):
    """Create database and setup records for every network"""
    
    init_db()
    
    if network == 'mainner':
        pass
    else:
        network = 'testnet'

    if height > 0:
        main_id = acl_scanner.replace(network=network, block=height).execute()
        log.info(msg=f"Updated {network} ardor record", record_id=main_id, height=height)
    else:
        # init Ardor
        ardr = sigbroArdor(network=network)
        last = ardr.getLastBlockHeight()

        # replace record if exists
        if last > 0:
            main_id = acl_scanner.replace(network=network, block=last - rewind).execute()
            log.info(msg=f"Updated {network} ardor record", record_id=main_id, rewind=rewind, height=last - rewind)


@cli.command(name="scan")
@click.option("--readonly", help="Do not update last block counter", type=bool, default=False, is_flag=True)
@click.option("--network", help="Mainnet or testnet for scan", type=str, default="mainnet")
@click.option("--debug", help="Do not send any email and update database", type=bool, default=False, is_flag=True)
def scan_blockchain(readonly: bool, network: str, debug: bool) -> None:
    """Scan the blockchain until the end."""

    ardr = sigbroArdor(network=network)
    ardr_last_block = acl_scanner.get(acl_scanner.network == network).block

    if not ardr_last_block:
        log.error(msg="Initialize first")
        return
    
    ardr_last_block = ardr_last_block + 1  # try to get next block
    next_block_exists = True
    alerts_list = ['ARDOR-H2W5-VZAB-9XFZ-38885']

    while next_block_exists:
        """Scan blockchain forward"""
        block = ardr.getBlock(height=ardr_last_block)

        if block and "errorCode" not in block:
            if debug:
                log.debug(
                    msg="Scaned",
                    height=block["height"],
                    blockid=block["block"],
                    generator=block["generatorRS"],
                    number_of_transactions=block["numberOfTransactions"],
                )

            # got block, need to check it for any relevant alert
            check_block_for_alerts(
                block=block,
                alerts=alerts_list,
                network=network,
                debug=debug,
            )

            # update lastblock if not readonly was set
            if not readonly:
                acl_scanner.update(block=ardr_last_block).where(acl_scanner.network == network).execute()
        else:
            log.debug(msg="Next block doest not exists.")
            next_block_exists = False
            continue

        if "nextBlock" in block:
            ardr_last_block = ardr_last_block + 1
        else:
            next_block_exists = False


if __name__ == "__main__":
    cli()
