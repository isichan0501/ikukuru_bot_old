# -*- coding:utf-8 -*-
from ctypes import util
import pandas as pd
import time
from BotHelper import JsonSearch, get_sheet_with_pd, set_sheet_with_pd, line_push, writeSheet
from BotHelper.util_driver import compose_driver, twitter_login, ouath_twitter_not_login, http_check, wifi_reboot, check_ip, s3_img
from BotHelper.util_driver import moji_hikaku, page_load, myClick, exe_click, mySendkey, slowClick, my_emojiSend, emoji_convert, add_ifin, send_gmail, mail_what, s3_img
import pysnooper
from importlib import reload
import os
from contextlib import contextmanager

from dotenv import load_dotenv
import logging

import util_login
import ik_helper

#-----------debug-----
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        InvalidArgumentException,
                                        JavascriptException,
                                        NoAlertPresentException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager



from BotHelper.util_driver import page_load, myClick, exe_click, mySendkey
#-----debug---------



logging.config.fileConfig('logconf.ini')
lg = logging.getLogger(__name__)



# 環境変数を参照
load_dotenv()
API_URL = os.getenv('API_URL')
CHROME_PROFILE_DIR = os.getenv('CHROME_PROFILE_DIR')
SHEET_NAME = os.getenv('SHEET_NAME')



@contextmanager
def driver_set(prox=False, profdir=None, prof_name=None, ua_name=None):

    driver = compose_driver(proxy_info=prox, userdata_dir=profdir, use_profile=prof_name, use_ua=ua_name)
    try:
        yield driver
    finally:
        driver.quit()

        


def main(tem_ple):

    with driver_set(prox=False, profdir=None, prof_name=None, ua_name=tem_ple['ua']) as driver:

        #まずはwifi再起動
        wifi_reboot(driver)
        is_reboot = http_check(driver)

        
        ik = ik_helper.Ikkr(tem_ple)
        is_login = ik.login(driver)
        if not is_login:
            return False

        #画像設定されていたらTrue、その場合のみ投稿やメッセージ返信に進む
        is_img = ik.ik_profimg(driver)
        if not is_img:
            return False
        ik.ik_prof1(driver)
        ik.ik_prof2(driver)
        ik.prof_text(driver)
        ik.ik_basyo(driver)
        ik.ik_prof_basyo(driver)
        ik.toko_check(driver)
        
        #----メール返信
        for i in range(30):
            is_mail = ik.ik_mail(driver)
            if is_mail:
                break
            
        for loop_num in range(30):
            for ppn in range(9, 1, -1):
                ik.asipeta(driver, ppn)
            
        #----メール返信
        for i in range(30):
            is_mail = ik.ik_mail(driver)
            if is_mail:
                break



if __name__ == "__main__":
    df = get_sheet_with_pd(sheetname=SHEET_NAME)
    #イククルのIDのあるアカウントだけ
    df.dropna(subset=['cnm'], inplace=True)
    ik_index = df.loc[~df['ik'].isnull()].index
    # img = s3_img()
    # import pdb;pdb.set_trace()
    
    for loop_num, n in enumerate(ik_index):
        #テンプレ取得
        tem_ple = df.iloc[n,:]
        # is_main = main(tem_ple)
        
        if tem_ple['cnm'] != 'yuri':
            continue
        #---driver---
        driver = compose_driver(proxy_info=False, userdata_dir=None, use_profile=None, use_ua=tem_ple['ua'])
        ik = ik_helper.Ikkr(tem_ple)
        is_login = ik.login(driver)
        #asiato
        for ppn in range(3):
            is_asiato = ik.asiato_newface(driver, ppn)
            if is_asiato:
                break
        
        # #画像設定されていたらTrue、その場合のみ投稿やメッセージ返信に進む
        # is_img = ik.ik_profimg(driver)
        # ik.ik_prof1(driver)
        # ik.ik_prof2(driver)
        # ik.prof_text(driver)
        # ik.ik_basyo(driver)
        # ik.ik_prof_basyo(driver)
        # ik.toko_check(driver)
        
        import pdb;pdb.set_trace()
        # driver.quit()