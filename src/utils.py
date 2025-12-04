import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def random_delay(delay_range=(2, 5)):
    """Random sleep to avoid being blocked."""
    time.sleep(random.uniform(*delay_range))


def press_esc(driver):
    """Press ESC key to close popups."""
    try:
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()
    except:
        pass
