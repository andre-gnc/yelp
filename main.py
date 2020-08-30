import os
# from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def make_soup(ms_url):
    # Make soups of each url.
    response = requests.get(ms_url)
    data = response.text
    ms_soup = BeautifulSoup(data, 'html.parser')
    return ms_soup


def make_driver_chrome(mdc_url):
    mdc_driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver.exe'))
    mdc_driver.get(mdc_url)
    return mdc_driver


TIMEOUT = 30

url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA'

driver = make_driver_chrome(url)
driver.set_window_position(150, 200)
driver.minimize_window()

wait = WebDriverWait(driver, TIMEOUT)
tag = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'lemon--ul__09f24__1_cxs')))
place_tags = tag.find_elements_by_class_name('lemon--div__09f24__1mboc.container__09f24__21w3G'
                                             '.hoverable__09f24__2nTf3.margin-t3__09f24__5bM2Z.margin'
                                             '-b3__09f24__1DQ9x.padding-t3__09f24__-R_5x.padding-r3__09f24__1pBFG'
                                             '.padding-b3__09f24__1vW6j.padding-l3__09f24__1yCJf.border'
                                             '--top__09f24__1H_WE.border--right__09f24__28idl.border'
                                             '--bottom__09f24__2FjZW.border--left__09f24__33iol.border-color'
                                             '--default__09f24__R1nRO')
print(len(place_tags))

for place_counter, place_tag in enumerate(place_tags, 1):
    if place_counter == 1 or place_counter == 2 or place_counter == 33:
        continue
    place_url = place_tag.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[1]/div[1]/div[2]/div[2]/ul/li['
                                                '6]/div/div/div/div[2]/div[1]/div/div[1]/div/div['
                                                '1]/div/div/h4/span/a').get_attribute('href')
    print(place_counter - 2)
    driver.get(place_url)
    name = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div['
                                        '1]/div[1]/div/div/div[1]/h1').text
    print('Name: ' + name)
    categories = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[4]/div/div/div[2]/div/div/div['
                                              '1]/div/div[1]/div[1]/div/div/span[2]').text
    print('Categories: ' + categories)
    phone = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div['
                                         '2]/div/div/section[1]/div/div[2]/div/div[2]/p[2]').text
    print('Phone: ' + phone)
    address_tag = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[4]/div/div/div[2]/div/div/div['
                                               '1]/div/div[1]/section[3]/div[2]/div[1]/div/div/div/div[1]')
    address_items = address_tag.find_elements_by_class_name('lemon--p__373c0__3Qnnj.text__373c0__2U54h.text-color'
                                                            '--normal__373c0__NMBwo.text-align--left__373c0__1Uy60')
    address = ''
    for address_item_counter, address_item in enumerate(address_items, 1):
        address = address + address_item.text + ' '
    print('Address: ' + address)
    print('Website: ' + place_url)
    hours = driver.find_elements_by_class_name('lemon--p__373c0__3Qnnj.text__373c0__2U54h.no-wrap__373c0__2vNX7.text'
                                               '-color--normal__373c0__NMBwo.text-align--left__373c0__1Uy60')
    # hours = driver.find_elements_by_class_name('lemon--tr__373c0__14NN0.table-row__373c0__3wipe')
    print(len(hours))
    # hour_each = ''
    for hours_counter, hour in enumerate(hours, 1):
        if hours_counter == 1:
            print('Mon: ' + hour.text)
        elif hours_counter == 2:
            print('Tue: ' + hour.text)
        elif hours_counter == 3:
            print('Wed: ' + hour.text)
        elif hours_counter == 4:
            print('Thu: ' + hour.text)
        elif hours_counter == 5:
            print('Fri: ' + hour.text)
        elif hours_counter == 6:
            print('Sat: ' + hour.text)
        elif hours_counter == 7:
            print('Sun: ' + hour.text)

    break

driver.quit()
