#disable caching in browser or performance may suffer

import os
import time
import platform
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from browsermobproxy import Server

"""
adj = Energy, Height Energy, Overdrive, Suspense, Character Arm-Space, Pray Towards, 
    Emotion, Jump Length, Reaction, Posture, Arm Height, Stance, Punch Height, 
    Hit Stance Height, Step Width, Head Turn, Lean, Target, Distance, Consciousness,
    Energy Level, Injury, Body Type, Surprise Level, Arms, Anger, Direction, Focus, 
    Stance Height, Style, Location, Speed, Range, Catch Height, Intensity, Stride
"""

def choose_fname(product_info):
    product_name = product_info.split("\n")[0]
    product_name = product_name.replace("/", "_")
    if not os.path.isfile("output/{}.json".format(product_name)):
        return "output/{}.json".format(product_name)
    j=1
    while os.path.isfile("output/{} ({}).json".format(product_name, j)):
        j += 1
    return "output/{} ({}).json".format(product_name, j)


def get_product_content():
    global chrome, product_id, proxy, product
    try:
        har = proxy.new_har(str(product_id), options={'captureContent':True, 'captureBinaryContent':True})
        product_info = product.text
        print(product_id, product_info)
        if "Pack" in product_info:
            product_id +=1
            return "OK" 
        product.click()
        elenemt = WebDriverWait(chrome, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "editor-loading-screen")))
        element = WebDriverWait(chrome, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, "editor-loading-screen")))
        download = WebDriverWait(chrome, 60).until(EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Download')]")))
        time.sleep(1)
        download.click()
        select_fr = Select(chrome.find_element_by_xpath("//div[@class='form']//div[3]//select"))
        select_fr.select_by_index(1)
        download = WebDriverWait(chrome, 60).until(EC.presence_of_element_located((By.XPATH, "(//button[contains(.,'Download')])[2]")))
        time.sleep(3)
        download.click()
        time.sleep(10)                
        product_id += 1
        return "OK"
    except AssertionError:
        return get_product_content()
    except IndexError:
        print(fname)
        return "IndexError"
    except KeyError:
        return "KeyError"
    except TimeoutException:
        return "TimeoutException"
    except:
        return "exception"  


def mixamo_login(args):
    chrome.get('https://www.mixamo.com/')
    login = WebDriverWait(chrome, 60).until(EC.presence_of_element_located((By.XPATH, "//a[contains(.,'Log in')]")))
    login.click()
    email_box = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    email_box.send_keys(args.email)
    cont = WebDriverWait(chrome, 60).until(EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Continue')]")))
    cont.click()
    time.sleep(60)
    # password_box = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    # password_box.send_keys(password)
    # cont = WebDriverWait(chrome, 60).until(EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Continue')]")))
    # cont.click()
    #email = raw_input('email: ')
    #passwd = raw_input('password: ')
    #passwd_box = chrome.find_element_by_name('password')
    #passwd_box.click()
    #highlight(passwd_box)
    #submit = chrome.find_element_by_xpath("//button[contains(.,'Sign in')]")
    #submit.click()
    #time.sleep(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mixamo Website crawler')
    parser.add_argument('--email', type=str, help='email account to sign in')
    parser.add_argument('--password', type=str, help='account password to sign in')
    args = parser.parse_args()

    if platform.system() == "Linux":
        server = Server(os.path.abspath('browsermob-proxy-2.1.4/bin/browsermob-proxy'))
    else:
        server = Server(os.path.abspath('browsermob-proxy-2.1.4/bin/browsermob-proxy.bat'))
    server.start()
    proxy = server.create_proxy()
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)
    chrome = webdriver.Chrome('chromedriver', chrome_options=options)
    mixamo_login(args)
    product_id = 0
    for page_number in range(1, 53):
        chrome.get('https://www.mixamo.com/#/?page={}&query=&type=Motion%2CMotionPack'.format(page_number))
        try:
            element = WebDriverWait(chrome, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'product-info'))
            )
            products = chrome.find_elements_by_class_name('product-info')
            for product in products:
                i = 0
                while i < 30:
                    result = get_product_content()
                    if result == "OK" or result == "KeyError":
                        break
                    i += 1
        except:
            raise
