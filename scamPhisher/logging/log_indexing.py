import logging
import os
from datetime import datetime

class Logging:
    def __init__(
        self,
        log_dir: str = "../Documents",
        log_file: str = "scamFlow.log",
        level: int = logging.DEBUG if os.getenv("ENV") == "dev" else logging.INFO
    ) -> None:
        
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_file)
        
        logging.basicConfig(
            filename=log_path,
            level=level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%m-%d-%y %H:%M"
        )
        
        self.logger = logging.getLogger("ScamFlowLogger")

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", "%m-%d-%y %H:%M"
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

    def info(self, msg: str) -> str:
        self.logger.info(msg)
        now = datetime.now().strftime("%m-%d-%y %H:%M")
        return f"{now} [INFO] {msg}"

    def warning(self, msg: str) -> str:
        self.logger.warning(msg)
        now = datetime.now().strftime("%m-%d-%y %H:%M")
        return f"{now} [WARNING] {msg}"

    def error(self, msg: str) -> str:
        self.logger.error(msg)
        now = datetime.now().strftime("%m-%d-%y %H:%M")
        return f"{now} [ERROR] {msg}"
