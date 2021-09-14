from selenium.webdriver.remote.webdriver import WebDriver
from autoelective import captcha
from autoelective.captcha import CaptchaRecognizer
from autoelective.const import CNN_MODEL_FILE
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time
from datetime import date
import base64
from random import randint
import sys

ele_set={}
captcha_code='qwqw'
global r,js,stuid,passwd
geckodriver_path='./'

def send_message(_s):
    print(_s)

def iaaa_login():
    ff_op=webdriver.FirefoxOptions()
    # ff_op.set_headless()
    driver=webdriver.Firefox(options=ff_op) 
    driver.get('https://elective.pku.edu.cn/')
    # iaaa login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user_name"))
    ).send_keys(stuid)
    driver.find_element_by_id('password').send_keys(passwd)
    driver.find_element_by_id('logon_button').click()
    return driver

def single_loop(driver:webdriver.Firefox):
    try:
        driver.execute_script(js)
        time.sleep(1)
        tmp=driver.find_element_by_id('imgname')
        img_src=tmp.get_attribute('src')
        _begin=img_src.find('base64,')
        im_data=(base64.b64decode(img_src[_begin+len('base64,'):]))
        c=r.recognize(im_data)
        print(c.code)
        captcha_code=c.code
    except:
        print('cap_error')

    # driver.find_element_by_id('validCode').send_keys(captcha_code)
    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,'validCode'))
    ).send_keys(captcha_code)

    # tmp=driver.find_elements_by_class_name('datagrid')
    tmp=WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME,'datagrid'))
    )
    # print(len(tmp))
    # print(tmp[1].text)
    # if(tmp[1].text!=)
    even_class=tmp[0].find_elements_by_class_name('datagrid-even')
    odd_class=tmp[0].find_elements_by_class_name('datagrid-odd')
    class_list=even_class+odd_class
    # print(len(class_list))

    for single_class_num in range(len(class_list)):
        single_class=class_list[single_class_num]
        details=single_class.find_elements_by_class_name('datagrid')
        class_name=details[0].text+','+details[5].text
        if(class_name in ele_set):
            # print(single_class_num)
            ele_frag=[int(_) for _ in details[9].text.split(' / ')]
            print(class_name,str(ele_frag))
            if(ele_frag[0]>ele_frag[1]):
                details[10].click()
                driver.switch_to.alert.accept()
                send_message('ok')
                ele_set.pop(class_name)
                # return
            else:
                # details[10].click()
                # driver.switch_to.alert.accept()
                pass
    driver.refresh()
            

if __name__=="__main__":
    with open('config.json','r') as f:
        config=f.read()
    config_json=json.loads(config)
    stuid=config_json['stuid']
    passwd=config_json['passwd']
    ele_set=config_json['ele_set']
    with open('1.js','r') as f:
        js=f.read()
    r=CaptchaRecognizer(CNN_MODEL_FILE)
    while(ele_set):
        try:
            print('Start Driver')
            driver=iaaa_login()
            if 1:#主修
                WebDriverWait(driver,10).until(
                    EC.element_to_be_clickable((By.ID,'div1'))
                ).click()

            tmp=WebDriverWait(driver,10).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME,'titlelink1'))
            )
            print(len(tmp))
            tmp[3].click()#补退选

            print('Begin Loop')
            while(ele_set):
                single_loop(driver)
                print(time.asctime())
                time.sleep(10+randint(0,5))
            print('hi')
            driver.quit()
        except:
            print('ERROR!!!!!!!')
            driver.quit()

