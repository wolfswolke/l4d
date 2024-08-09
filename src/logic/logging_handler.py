import sys
import traceback
from datetime import datetime


class bcolors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class LOGGER:
    # Better logger pls
    def log(self, level, handler, content):
        dt = datetime.now()
        ts = dt.strftime('%Y-%m-%d_%H:%M:%S')
        if level == "info":
            print(bcolors.OKGREEN + f"{ts} " + "LOG: " + level + " - " + handler + " - " + str(content) + bcolors.ENDC)
        elif level == "error":
            print(bcolors.FAIL + f"{ts} " + "LOG: " + level + " - " + handler + " - " + str(content) + bcolors.ENDC)
        elif level == "warning":
            print(bcolors.WARNING + f"{ts} " + "LOG: " + level + " - " + handler + " - " + str(content) + bcolors.ENDC)
        elif level == "debug":
            print(bcolors.OKCYAN + f"{ts} " + "LOG: " + level + " - " + handler + " - " + str(content) + bcolors.ENDC)
        elif level == "boot":
            print(bcolors.OKBLUE + f"{ts} " + "LOG: " + level + " - " + handler + " - " + str(content) + bcolors.ENDC)
        else:
            print(bcolors.FAIL + f"{ts} " + "LOG: " + level + " - " + handler + " - " + str(content) + bcolors.ENDC)

    def log_exception(self, exc):
        """
        Logs an exception with detailed information.

        Args:
        - logger (logging.Logger): The logger instance.
        - exc (Exception): The exception to log.
        """
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_info = traceback.extract_tb(exc_tb)
        filename, line, func, text = tb_info[-1]

        self.log(level="error", handler=filename, content=f"Exception in {func} at {filename}:{line} - {exc_value} (Code: {text})")


logger = LOGGER()
