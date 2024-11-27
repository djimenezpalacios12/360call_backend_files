import datetime
import logging.handlers
import os
from pathlib import Path
import colorlog


class MyLogger:
    logger: logging.Logger = None

    @staticmethod
    def configure(verbose=1):
        log_dir_path = Path(os.path.abspath("./logs"))
        log_dir_path.mkdir(parents=True, exist_ok=True)
        file_name_format = (
            "{year:04d}{month:02d}{day:02d}-{hour:02d}-{minute:02d}-{second:02d}.log"
        )
        file_msg_format = (
            "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
        )
        console_msg_format = (
            "[MS Archivos] [%(asctime)s] [%(levelname)-1s]: %(message)s"
        )

        logger = logging.getLogger("mylogger")
        logger.setLevel(logging.DEBUG)

        if verbose == 1:
            max_bytes = 5 * 1024**2
            backup_count = 50
            t = datetime.datetime.now()
            file_name = file_name_format.format(
                year=t.year,
                month=t.month,
                day=t.day,
                hour=t.hour,
                minute=t.minute,
                second=t.second,
            )
            file_name = os.path.join(log_dir_path, file_name)
            file_handler = logging.handlers.RotatingFileHandler(
                filename=file_name, maxBytes=max_bytes, backupCount=backup_count
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(file_msg_format)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        cformat = "%(log_color)s" + console_msg_format
        colors = {
            "DEBUG": "green",
            "INFO": "cyan",
            "WARNING": "bold_yellow",
            "ERROR": "bold_red",
            "CRITICAL": "bold_purple",
        }
        date_format = "%Y-%m-%d %H:%M:%S"
        formatter = colorlog.ColoredFormatter(cformat, date_format, log_colors=colors)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        MyLogger.logger = logger
