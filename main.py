from pathlib import Path
import threading
import time
import random

def query_dummy():
    return random.random()

def log_tmp(query_fn, logfile):
    if Path(logfile).is_dir():
        p = Path(logfile)/"tmp_log.csv"
    else:
        p = Path(logfile)

    tmp = query_fn()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(p, "a") as f:
        f.write(f"{timestamp},{tmp:.4f}\n")

def run(query_fn, logfile):
    log_tmp(query_fn, logfile)
    threading.Timer(5.0, lambda: run(query_fn, logfile)).start()

if __name__ == "__main__":
    run(query_dummy, "/home/tomi/Documents/academicos/becas/alemania/centech/pa/git/tmpcontrol")

