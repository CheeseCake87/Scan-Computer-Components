# scan-computer-components-daily-runner.py
import logging
import subprocess
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from time import sleep

from fetcher import process_urls

CMD = Path.cwd()
LOG_FILE = CMD / "daily.log"

ENABLE_RUNNER = True

rfh = RotatingFileHandler(filename=LOG_FILE, mode="a", maxBytes=1000000, backupCount=1)
rfh.setLevel(logging.INFO)

l = logging.getLogger('daily-runner')
l.setLevel(logging.INFO)
l.addHandler(rfh)

def main():
    start_dtn = datetime.now()

    l.debug(f"Daily runner started : {start_dtn}")

    fired = False

    while True:
        # fire every minute
        while_dtn = datetime.now()
        time = while_dtn.strftime("%-H%M")
        int_time = int(time)
        time_range = range(930, 932)

        l.debug(f"Check, {time_range}, current({int_time}) : {while_dtn}")

        if int_time in time_range:
            if not fired:
                l.info(f"Daily runner triggered : {while_dtn}")

                if ENABLE_RUNNER:

                    fired = True

                    l.info(" -- ")

                    process_urls()

                    git_pricing = subprocess.run(["git", "add", "pricing/pricing_data.json"], capture_output=True, text=True)
                    if git_pricing.stdout:
                        l.info(f"{git_pricing.stdout}")
                    if git_pricing.stderr:
                        l.error(f"{git_pricing.stderr}")

                    git_commit = subprocess.run(["git", "commit", "-m", "update pricing"], capture_output=True, text=True)
                    if git_commit.stdout:
                        l.info(f"{git_commit.stdout}")
                    if git_commit.stderr:
                        l.error(f"{git_commit.stderr}")

                    git_push = subprocess.run(["git", "push"], capture_output=True, text=True)
                    if git_push.stdout:
                        l.info(f"{git_push.stdout}")
                    if git_push.stderr:
                        l.error(f"{git_push.stderr}")

                    l.info(" -- ")

                else:

                    l.info(" -- Daily runner disabled.")


        else:

            l.debug(f"Daily runner not in range : {while_dtn}")

            if fired:

                l.debug(" -- Fired flag reset.")

                fired = False

        sleep(60)

if __name__ == '__main__':
    main()
