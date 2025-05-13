import schedule
import time
from datetime import datetime
import sys
import logging

from app.storage.sub_store import SubStore
from app.storage.ticker_store import TickerStore
from scheduler import scheduled_task
from app.config import TICK_PATH, SUB_PATH, TASK_FREQ

def main():

    #create logger configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S %p',  # 2023-05-15 02:32:10 PM
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)

    #create the two store objects
    tick_list = TickerStore(file_path=TICK_PATH)
    sub_list = SubStore(file_path=SUB_PATH, ticker_store=tick_list)

    logger.info("Scheduler started")

    #run the scheduled tasks at a routine interval
    schedule.every(TASK_FREQ).minutes.do(lambda: scheduled_task(tick_list, sub_list))

if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)

