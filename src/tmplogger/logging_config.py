import logging
import pathlib
import os


def init_logging_config(ROOT: pathlib.Path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler(ROOT / "general.log"), logging.StreamHandler()],
    )

def get_temperature_logger(ROOT: pathlib.Path):
    temperature_logger = logging.getLogger("temperature_logger")
    temperature_logger.setLevel(logging.INFO)
    temperature_handler = logging.FileHandler(ROOT / "temperature.log")
    temperature_handler.setFormatter(logging.Formatter("%(asctime)s,%(message)s"))
    temperature_logger.addHandler(temperature_handler)
    return temperature_logger

def init_logging_dirs(ROOT: pathlib.Path):
    if not ROOT.is_dir():
        os.mkdir(ROOT)
