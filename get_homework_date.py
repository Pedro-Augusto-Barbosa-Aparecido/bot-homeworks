import os
import sys
import time
import logging

from robot.bot import Bot
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from configparser import ConfigParser
from colorama import Style, Fore, Back

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class HomeWorkManager(Bot):
    def __init__(self, url):
        super().__init__(url)

        self.homeworks = []

    @staticmethod
    def _logging_time_sleep(_time: int, _for: str = ""):
        time.sleep(_time)
        logger.info(f"Waiting {_time}s for {_for}")

    def make_logging(self, password: str = None, email: str = None) -> None:
        try:
            if (password == '') or (email == ''):
                logger.warning("No email or password, finish process")
                return

            logger.debug(f"Accessing the url: {self._url}")
            self.driver.get(self._url)

            self._logging_time_sleep(15, "Page load")
            logger.info("Inserting email: %s" % email)
            self.driver.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(email)

            self._logging_time_sleep(2, "email insert")
            logger.info(f"Click on Button")
            self.driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()

            self._logging_time_sleep(15, "Page load")
            logger.info(f"Inserting password: [{'*'*len(password)}]")
            self.driver.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(password)

            self._logging_time_sleep(2, "password insert")
            logger.info(f"Click on Button")
            self.driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()

            self._logging_time_sleep(15, "Page load")
            logger.info(f"Click on Button")
            self.driver.find_element(By.XPATH, '//*[@id="idBtn_Back"]').click()

        except Exception as e:
            logger.error(f"Error: {e}")

    @staticmethod
    def _filter_container(container) -> list[WebElement]:
        return container.find_elements(By.CLASS_NAME, 'stv-item-container')

    def _get_all_teams(self):
        logger.info("Initialise homeworks count!")
        self.driver.find_element(By.XPATH, '//*[@id="app-bar-66aeee93-507d-479a-a3ef-8f494af43945"]').click()
        self._logging_time_sleep(15, "Page load")

        iframe = self.driver.find_element(By.XPATH, '/html/body/app-caching-container/div/div/extension-tab'
                                                    '/div/embedded-page-container/div/iframe')
        try:
            self.driver.switch_to.frame(iframe)
            message = self.driver.find_element(By.CLASS_NAME, 'title__2-Ls2')
            print(Fore.LIGHTBLACK_EX + message.text + Style.DIM)

            logger.info("Switch to completed homeworks")
            self.driver.find_element(By.XPATH, '//*[@id="PivotTab_graded"]').click()
            self._logging_time_sleep(10, "Switch to completed homeworks tab")

            homeworks = self.driver.find_element(
                By.XPATH,
                '//*[@id="root"]/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]'
            ).find_elements(By.CLASS_NAME, 'assignment-list-card-link__2tVU3')

            logger.info("Getting all homeworks")

            subject_names = []
            logger.info("Get Subjects names")
            for homework in homeworks:
                subject_names.append(homework.find_element(By.CLASS_NAME, 'assignment-card-class-name-text__37Hag')
                                     .text)

            logger.info("Getting information from all homeworks")
            for index, homework in enumerate(homeworks):
                print(f"Getting homework of subject: {subject_names[index]}")
                homework.click()

                self._logging_time_sleep(10, f"Page of homework {index + 1} load")

                logger.info("Get homework title")
                title = self.driver.find_element(By.XPATH, '//*[@id="assignmentViewerVisibilityContainer"]'
                                                           '/div[2]/div/div[1]/h1').text
                print(f"Title: {title}")
                logger.info("Get Dates")
                dates = []
                for date in self.driver.find_elements(By.CLASS_NAME, 'm-right-xxsmall__2wUsw'):
                    dates.append(date.text)

                self.homeworks.append({
                    "completed": True,
                    "dates": {
                        "start_date": dates[0],
                        "finish_date": dates[1]
                    },
                    "homework_title": title,
                    "subject": subject_names[index]
                })

                logger.info("Return for subjects list")
                self.driver.find_element(By.XPATH, '//*[@id="assignmentViewerVisibilityContainer"]'
                                                   '/div[1]/div[1]/div[1]/div/a').click()
                self.driver.switch_to.default_content()
                self._logging_time_sleep(15, "Subject list page load")
                iframe = self.driver.find_element(By.XPATH, '/html/body/app-caching-container/div/div/extension-tab'
                                                            '/div/embedded-page-container/div/iframe')
                self.driver.switch_to.frame(iframe)
            self.driver.switch_to.default_content()
        except Exception as e:
            logger.exception(e)

    def get_tasks(self):
        self._get_all_teams()


if __name__ == "__main__":
    logging.basicConfig(
        filemode='w',
        filename=os.path.join(os.getcwd(), "report_get_homework.log"),
        level=logging.DEBUG,
        format="[LOG module=%(name)s %(asctime)s]: %(message)s"
    )

    home_work = HomeWorkManager("https://teams.microsoft.com")
    home_work.start()

    try:
        import __dev__
        config = ConfigParser()
        config.read("config_dev.ini")

        logger.info("Make logging")
        home_work.make_logging(config["SECRETS"]["PASSWORD"] or '', config["SECRETS"]["EMAIL"] or '')

    except ImportError:
        logger.warning("You dont are on development environment")

    time.sleep(20)
    home_work.get_tasks()
    home_work.terminate()
