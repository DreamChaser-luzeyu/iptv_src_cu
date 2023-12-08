STYLE_RST = "\033[0m"
# ----- Background Color
STYLE_BKG_RED = "\033[41m"
STYLE_BKG_GREEN = "\033[42m"
STYLE_BKG_YELLOW = "\033[43m"
# ----- Text Color
STYLE_TEXT_RED = "\033[91m"
STYLE_TEXT_GREEN = "\033[92m"
STYLE_TEXT_YELLOW = "\033[33m"
STYLE_TEXT_BLUE = "\033[34m"
# ----- Log Color
STYLE_ERR = STYLE_TEXT_RED
STYLE_WARN = STYLE_TEXT_YELLOW
STYLE_INFO = STYLE_TEXT_BLUE
STYLE_INFO_OK = STYLE_TEXT_GREEN
STYLE_DEBUG = ""
# ----- Control
CTRL_CLEAR = "\033[2J"

from enum import Enum


class LogLevel(Enum):
    no_log_ = 0
    log_err_ = 1
    log_warn_ = 2
    log_info_ = 3
    log_debug_ = 4


class Logger:
    def __init__(self, log_level):
        self.log_level_ = log_level

    def log_debug(self, log_str):
        if self.log_level_.value >= LogLevel.log_debug_.value:
            print(f"{STYLE_DEBUG}[Debug] {log_str}{STYLE_RST}")

    def log_info(self, log_str):
        if self.log_level_.value >= LogLevel.log_info_.value:
            print(f"{STYLE_INFO}[Info ] {log_str}{STYLE_RST}")

    def log_ok(self, log_str):
        if self.log_level_.value >= LogLevel.log_info_.value:
            print(f"{STYLE_INFO_OK}[Info ] {log_str}{STYLE_RST}")

    def log_warn(self, log_str):
        if self.log_level_.value >= LogLevel.log_warn_.value:
            print(f"{STYLE_WARN}[Warn ] {log_str}{STYLE_RST}")

    def log_err(self, log_str):
        if self.log_level_.value >= LogLevel.log_err_.value:
            print(f"{STYLE_ERR}[Error] {log_str}{STYLE_RST}")

    def log_clear(self):
        print(f"{CTRL_CLEAR}")


logger_gv = Logger(LogLevel.log_debug_)


def append_local() -> None:
    import os
    files = os.listdir("filtered_list")
    logger_gv.log_debug(files)
    for local_file_name in files:
        local_file_str: str = ""
        local_file_obj = None
        try:
            local_file_obj = open("filtered_list/" + local_file_name, encoding="utf-8")
            local_file_str = local_file_obj.read()
        except Exception as e:
            logger_gv.log_warn("Error reading IPTV src file: {}".format(e))
        finally:
            if local_file_obj: local_file_obj.close()
        full_file_obj = None
        try:
            full_file_obj = open("full_filtered.m3u", encoding="utf-8", mode="a")
            full_file_obj.write(local_file_str)
        except Exception as e:
            logger_gv.log_warn(e)
        finally:
            if full_file_obj: full_file_obj.close()


if __name__ == '__main__':
    logger_gv.log_info("IPTV filtered generator")
    append_local()
