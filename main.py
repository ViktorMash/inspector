import time
import schedule

from app.core import intalev_handler, period

intalev_handler.check()
schedule.every().day.at(period.launch_time(14, 00)).do(intalev_handler.check)  # 14:00 msk


if __name__ == '__main__':
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as err:
            time.sleep(10)
