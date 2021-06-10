"""Template robot with Python."""
from RPA.Browser.Selenium import Selenium
import logging
import os
import sys
from time import sleep

website = "https://downloads.robocorp.com/rcc/releases/index.html"
stdout = logging.StreamHandler(sys.stdout)
DOWNLOAD_TIMEOUT = 30

logging.basicConfig(
    level=logging.INFO,
    format="[{%(name)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=[stdout],
)

logger = logging.getLogger("robot")
browser = Selenium()


def check_downloaded_items():
    return browser.execute_javascript(
        """return document.querySelector('downloads-manager').shadowRoot.getElementById('downloadsList').items;"""
    )


def are_all_downloads_complete():
    download_items = check_downloaded_items()
    all_done = True
    for item in download_items:
        if item["state"] != "COMPLETE":
            all_done = False
            break

    return {"all_done": all_done, "items": download_items}


def minimal_task():
    # ROBOT_ROOT - basically current directory
    # ROBOT_ARTIFACTS - directory defined in robot.yaml with `artifactsDir`

    browser.set_download_directory(os.environ["ROBOT_ARTIFACTS"])
    browser.open_available_browser(website, browser_selection="chrome")
    browser.click_element("(//ul//li/a)[1]")
    browser.execute_javascript("window.open('about:blank','_blank');")
    browser.switch_window("NEW")
    browser.go_to("chrome://downloads")

    for _ in range(DOWNLOAD_TIMEOUT):
        result = are_all_downloads_complete()
        if result["all_done"]:
            logger.info("All downloads are complete")
            for item in result["items"]:
                logger.info(
                    "FILE: '%s' downloaded from '%s'" % (item["filePath"], item["url"])
                )
            break
        else:
            logger.info("Downloading...")
        sleep(1)
    logger.info("Done.")


if __name__ == "__main__":
    minimal_task()