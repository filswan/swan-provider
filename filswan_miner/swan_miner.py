import threading
import time
from filswan_miner.swan_miner_deal_downloader import downloader
from filswan_miner.swan_miner_deal_scanner import scanner
from filswan_miner.swan_miner_deal_importer import importer


def start(config_path: str):

    swan_miner_downloader = threading.Thread(target=downloader,args=(config_path,))
    swan_miner_importer = threading.Thread(target=importer,args=(config_path,))
    swan_miner_scanner = threading.Thread(target=scanner,args=(config_path,))

    swan_miner_downloader.start()
    swan_miner_importer.start()
    swan_miner_scanner.start()