from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


BASE_URL = 'https://develop.opencast.org'


def navigate(driver, path):
    driver.get(f'{BASE_URL}{path}')


def wait_for(driver, element):
    WebDriverWait(driver, 20).until(
            expected_conditions.presence_of_element_located(element))


def main():
    driver = webdriver.Firefox()
    navigate(driver, '')
    assert 'Opencast' in driver.title
    elem = driver.find_element(By.ID, 'email')
    elem.clear()
    elem.send_keys('admin')
    elem = driver.find_element(By.ID, 'password')
    elem.clear()
    elem.send_keys('opencast')
    elem.send_keys(Keys.RETURN)

    wait_for(driver, (By.ID, 'menu-toggle'))

    navigate(driver, '/ltitools')
    elem = driver.find_element(By.TAG_NAME, 'h1')
    assert 'Welcome to the LTI Module' == elem.text

    driver.get('https://develop.opencast.org/ltitools/index.html?subtool=series')

    wait_for(driver, (By.TAG_NAME, 'header'))

    elem = driver.find_element(By.TAG_NAME, 'header')
    assert elem.text.startswith('Results 1-')

    elem = driver.find_elements(By.CSS_SELECTOR, '.list-group-item')[0]
    elem.click()
    assert 'Player' in driver.title

    driver.get('https://develop.opencast.org/ltitools/index.html?subtool=upload&series=')

    wait_for(driver, (By.TAG_NAME, 'form'))

    elem = driver.find_element(By.TAG_NAME, 'h2')
    assert elem.text.startswith('Upload new event')

    driver.close()


if __name__ == '__main__':
    main()
