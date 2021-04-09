import logging
import os
import sys

from apscheduler.schedulers.background import BackgroundScheduler

from filswan_miner.aria2c import Aria2c
from filswan_miner.aria2_service import check_download_status, start_downloading
import subprocess

from filswan_miner.common.config import read_config
from filswan_miner.common.swan_client import SwanClient
from filswan_miner.common.logging import get_logger


def downloader(config_path: str):

    logger = get_logger('swan_miner_deal_downloader')


    config = read_config(config_path)
    MINER_FID = config['main']['miner_fid']
    ARIA2_HOTS = config['aria2']['aria2_host']
    ARIA2_PORT = config['aria2']['aria2_port']
    ARIA2_SECRET = config['aria2']['aria2_secret']
    ARIA_CONF = config['aria2']['aria2_conf']

    OUT_DIR = config['aria2']['aria2_download_dir']
    api_url = config['main']['api_url']
    api_key = config['main']['api_key']
    access_token = config['main']['access_token']
    miner_fid = config['main']['miner_fid']

    aria2_client = Aria2c(ARIA2_HOTS, ARIA2_PORT, ARIA2_SECRET)
    swan_client =  SwanClient(api_url, api_key, access_token)
    MAX_DOWNLOADING_TASKS = 10

    # subprocess.Popen(["aria2c", "--conf-path=" + ARIA_CONF])
    logger.info("Start check_download_status.... ")
    sched = BackgroundScheduler()
    sched.add_job(
        check_download_status,
        args=[aria2_client, swan_client, miner_fid],
        trigger='cron',
        minute='*/1',
        hour='*'
    )
    sched.start()
    start_downloading(MAX_DOWNLOADING_TASKS, MINER_FID, OUT_DIR, aria2_client, swan_client)