import schedule
import time
from datetime import datetime

from app.storage.sub_store import SubStore
from app.storage.ticker_store import TickerStore
from scheduler import scheduled_task
from app.config import TICK_PATH, SUB_PATH, TASK_FREQ

def main():

    #create the two store objects
    tick_list = TickerStore(file_path=TICK_PATH)
    sub_list = SubStore(file_path=SUB_PATH, ticker_store=tick_list)

    print(f"{datetime.now()}: Scheduler started")

    #run the scheduled tasks at a routine interval
    schedule.every(TASK_FREQ).minutes.do(lambda: scheduled_task(tick_list, sub_list))

if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)

