import os
import time
import logging

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, url: str = None) -> None:
        logger.debug("Initialising bot!")
        self.__options = ChromeOptions()
        # self.__options.add_argument('headless')

        self._url = url
        self.__driver: Chrome = None
        self.__service: Service = None

    def __str__(self) -> str:
        return f"Bot | url={self._url}"

    @property
    def url(self) -> str:
        return self._url

    @property
    def driver(self) -> Chrome:
        return self.__driver

    @staticmethod
    def _get_current_folder() -> str:
        return os.getcwd()

    @staticmethod
    def _format_date(date: datetime) -> str:
        return str(date).split(".")[0]

    def start(self) -> None:
        logger.debug(f"Configuring bot!")
        self.__service = Service(ChromeDriverManager().install())
        self.__driver = Chrome(service=self.__service, options=self.__options)
        time.sleep(5)

    def terminate(self) -> None:
        logger.debug("Stopping bot")
        self.__driver.close()


if __name__ == "__main__":
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), "robot_log.log"),
        filemode='w',
        level=logging.DEBUG,
        format="[LOG %(asctime)s module=%(name)s]: %(message)s"
    )

    bot = Bot(url="https://teams.microsoft.com")
    bot.start()
