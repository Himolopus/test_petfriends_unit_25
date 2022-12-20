import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import *


@pytest.fixture(scope='session', params=browsers)
def session_driver(request):
    if request.param == 'chrome':
        driver = webdriver.Chrome()
    elif request.param == 'firefox':
        driver = webdriver.Firefox()
    elif request.param == 'msedge':
        driver = webdriver.Edge()
    else:
        raise TypeError('No allowable browser in settings')

    yield driver
    driver.quit()



@pytest.fixture(autouse=True, scope='class')
def class_preconditions(request, session_driver):
    session_driver.get(login_page)
    session_driver.find_element(By.ID, 'email').send_keys(email)
    session_driver.find_element(By.ID, 'pass').send_keys(password)
    session_driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    if request.cls.__name__ == 'TestAllPets':
        # Переходы напрямую через url так не стоит задача тестировать кнопки
        session_driver.get(all_pets_page)
    elif request.cls.__name__ == 'TestMyPets':
        session_driver.get(my_pets_page)

@pytest.fixture(scope='class')
def all_pets_elements(session_driver):
    elements = dict()
    # Добавляем неявные ожидания для элементов стриницы /all_pets (фикстура используется в классе TestAllPets)
    session_driver.implicitly_wait(10)
    elements['header'] = session_driver.find_element(By.TAG_NAME, 'h1')
    elements['images'] = session_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    elements['names'] = session_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    elements['descriptions'] = session_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    # Возвращаем значение по умолчанию, т.к. вебдрайвер сессионный, а в классe TestMyPets мы используем явные ожидания
    session_driver.implicitly_wait(0)
    return elements


# Вспомогательня функция возвращающая список элементов по xpath локатору, через явное ожидание их появления
def find_elements_with_explicit_waits(driver, xpath, timer=10):
    return WebDriverWait(driver, timer).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

# Агалогичная функция для поиcка одного элемента
def find_element_with_explicit_waits(driver, xpath, timer=10):
    return WebDriverWait(driver, timer).until(EC.presence_of_element_located((By.XPATH, xpath)))


@pytest.fixture(scope='class')
def my_pets_elements(session_driver):
    elements = dict()
    elements['entities'] = find_elements_with_explicit_waits(session_driver, '//tbody/tr')
    elements['info_block'] = find_element_with_explicit_waits(session_driver, '//div[h2]')
    elements['pets_with_photo'] = find_elements_with_explicit_waits(session_driver,
                                                                   '//tr//img[starts-with(@src,"data:image")]')
    elements['names'] = find_elements_with_explicit_waits(session_driver, '//tbody/tr/td[1]')
    elements['types'] = find_elements_with_explicit_waits(session_driver, '//tbody/tr/td[2]')
    elements['ages'] = find_elements_with_explicit_waits(session_driver, '//tbody/tr/td[3]')
    return elements
