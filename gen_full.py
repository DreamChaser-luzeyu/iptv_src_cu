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


class Channel:
    def __init__(self, channel_url, channel_name="Unnamed", channel_group="Ungrouped", channel_logo="",
                 channel_country="Unknown", channel_lang="Unknown"):
        self.channel_url_ = channel_url
        self.channel_name_ = channel_name
        self.channel_group_ = channel_group
        self.channel_logo_ = channel_logo
        self.channel_country_ = channel_country
        self.channel_lang_ = channel_lang


def get_remote_url_list(urls_str: str) -> list[str]:
    line_list = urls_str.split("\n")
    url_list = []
    for line in line_list:
        if line.startswith("http"):
            url_list.append(line)
    return url_list


def download_and_append(url: str) -> None:
    import requests
    response_str: str = ""
    response = None
    try:
        response = requests.get(url)
        response_str = response.text
    except Exception as e:
        logger_gv.log_warn(e)
    if response:
        logger_gv.log_debug(response_str)
        logger_gv.log_debug(response.status_code)
    else:
        logger_gv.log_warn("url {} invalid".format(url))
        return
    full_file_obj = None
    try:
        full_file_obj = open("full.m3u", encoding="utf-8", mode="a")
        full_file_obj.write(response_str)
    except Exception as e:
        logger_gv.log_warn(e)
    finally:
        if full_file_obj: full_file_obj.close()
    return


def append_local() -> None:
    import os
    files = os.listdir("local_list")
    logger_gv.log_debug(files)
    for local_file_name in files:
        local_file_str: str = ""
        local_file_obj = None
        try:
            local_file_obj = open("local_list/" + local_file_name, encoding="utf-8")
            local_file_str = local_file_obj.read()
        except Exception as e:
            logger_gv.log_warn("Error reading IPTV src file: {}".format(e))
        finally:
            if local_file_obj: local_file_obj.close()
        full_file_obj = None
        try:
            full_file_obj = open("full.m3u", encoding="utf-8", mode="a")
            full_file_obj.write(local_file_str)
        except Exception as e:
            logger_gv.log_warn(e)
        finally:
            if full_file_obj: full_file_obj.close()




if __name__ == '__main__':
    logger_gv.log_info("IPTV src fetcher")
    remote_url_file_obj = None
    all_url_str: str = ""
    try:
        remote_url_file_obj = open("remote_url_list.txt", encoding="utf-8")
        all_url_str = remote_url_file_obj.read()
    except Exception as e:
        logger_gv.log_warn("Error reading IPTV src file: {}".format(e))
    finally:
        remote_url_file_obj.close()
    url_list: list[str] = get_remote_url_list(all_url_str)
    logger_gv.log_debug(url_list)
    for url in url_list:
        download_and_append(url)
    append_local()