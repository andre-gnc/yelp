import os
from time import sleep

import pandas
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.common.by import By


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

item_no = 120
excel_entries = 0
item_dict = {}
page = 0
page_test = 'yes'
test_page_amount = 5
categories = ''
phone = ''
website = ''

# url = 'https://www.yelp.com/search?find_desc=plumbing&find_loc=Atlanta%2C+GA&ns=1'
url = 'https://www.yelp.com/search?find_desc=plumbing&find_loc=Atlanta%2C%20GA&start=120'

while True:

    page += 1

    driver = make_driver_chrome(url)
    driver.set_window_position(150, 200)
    # driver.minimize_window()
    sleep(5)

    # wait = WebDriverWait(driver, TIMEOUT)
    # tag = wait.until(ec.presence_of_element_located((By.CLASS_NAME,
    # 'lemon--ul__373c0__1_cxs.undefined.list__373c0__2G8oH')))
    place_tags = driver.find_elements_by_class_name('lemon--div__373c0__1mboc.container__373c0__3HMKB'
                                                    '.hoverable__373c0__VqkG7.margin-t3__373c0__1l90z.margin'
                                                    '-b3__373c0__q1DuY.padding-t3__373c0__1gw9E.padding'
                                                    '-r3__373c0__57InZ.padding-b3__373c0__342DA.padding'
                                                    '-l3__373c0__1scQ0.border--top__373c0__3gXLy.border'
                                                    '--right__373c0__1n3Iv.border--bottom__373c0__3qNtD.border'
                                                    '--left__373c0__d1B7K.border-color--default__373c0__3-ifU')

    for place_counter, place_tag in enumerate(place_tags, 1):
        if place_counter <= 10 or place_counter >= 31:
            continue
        place_url = place_tag.find_element_by_class_name(
            'lemon--a__373c0__IEZFH.link__373c0__1UGBs.link-color--inherit__373c0__1J-tq.link-size'
            '--inherit__373c0__3K_7i').get_attribute('href')

        # print(place_counter - 10)
        print(item_no + 1)
        company_driver = make_driver_chrome(place_url)
        company_driver.set_window_position(150, 200)
        sleep(5)

        try:
            name = company_driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[3]/div/div/div['
                                                        '2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/h1').text
        except NoSuchElementException:
            name = 'Grab it manually please!'
        print('Name: ' + name)

        try:
            category_tags = company_driver.find_element_by_class_name(
                'lemon--a__373c0__IEZFH.link__373c0__2-XHa.editCategories__373c0__3oys3.link--chiclet__373c0__eqf92'
                '.link-color--blue-dark__373c0__4vqlF.link-size--default__373c0__fPIdG').find_element_by_xpath(
                '..').find_elements_by_class_name(
                'lemon--a__373c0__IEZFH.link__373c0__2-XHa.link-color--inherit__373c0__2f-vZ.link-size'
                '--inherit__373c0__nQcnG')
            categories = ''
            for category_tags_counter, category_tag in enumerate(category_tags, 1):
                categories = categories + category_tag.text + ' '
        except NoSuchElementException:
            categories = 'Grab it manually please!'
        print('Categories: ' + categories)

        try:
            address_tag = company_driver.find_element_by_tag_name('address')
            address_items = address_tag.find_elements_by_tag_name('p')
            address = ''
            for address_item_counter, address_item in enumerate(address_items, 1):
                address = address + address_item.text + ' '
            # print('Address Tag amount: ' + str(len(address_tag)))
        except NoSuchElementException:
            address = 'Grab it manually please!'
        print('Address: ' + address)

        try:
            phone_tags = company_driver.find_element_by_class_name(
                'lemon--span__373c0__3997G.icon__373c0__2dvNm.icon--24-phone-v2.icon--v2__373c0__1rfbs'
                '.icon__373c0__3n-2P').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_elements_by_tag_name('p')
            for phone_tags_counter, phone_tag in enumerate(phone_tags, 1):
                if phone_tags_counter == 2:
                    phone = phone_tag.text
                    print('Phone: ' + phone)
        except NoSuchElementException:
            phone = 'Grab it manually please!'
            print('Phone: ' + phone)

        try:
            website_tags = company_driver.find_element_by_class_name(
                'lemon--span__373c0__3997G.icon__373c0__2dvNm.icon--24-external-link-v2.icon--v2__373c0__1rfbs'
                '.icon__373c0__3n-2P').find_element_by_xpath('..').find_element_by_xpath(
                '..').find_elements_by_tag_name('div')
            for website_tags_counter, website_tag in enumerate(website_tags, 1):
                if website_tags_counter == 2:
                    website = website_tag.text
        except NoSuchElementException:
            website = 'No website.'
        print('Website: ' + website)

        print('Profile: ' + place_url)
        print(item_no + 1)
        print('\n')

        excel_entries += 1
        item_no += 1
        item_dict[item_no] = [name, categories, address, phone, website, place_url]

        if excel_entries == 10:
            df_items = pandas.DataFrame.from_dict(
                item_dict, orient='Index',
                columns=['Name', 'Categories', 'Address', 'Phone', 'Website', 'Profile'])
            df_items.to_excel('data.xlsx')
            # df_items.to_csv('data.csv')
            excel_entries = 0

        company_driver.quit()

    try:
        url = driver.find_element_by_class_name('lemon--a__373c0__IEZFH.link__373c0__2MnoO.next-link.navigation'
                                                '-button__373c0__23BAT.link-color--inherit__373c0__23vKF.link-size'
                                                '--inherit__373c0__cQmDm').get_attribute('href')
        print('Next url: ' + url)
    except NoSuchElementException:
        print('Last page. It\'s finished')
        driver.quit()
        break

    if page == test_page_amount and page_test == 'yes':
        driver.quit()
        print('Next url: ' + url)
        break

    driver.quit()

df_items = pandas.DataFrame.from_dict(
    item_dict, orient='Index', columns=['Name', 'Categories', 'Address', 'Phone', 'Website', 'Profile'])
df_items.to_excel('data.xlsx')
# df_items.to_csv('data.csv')
