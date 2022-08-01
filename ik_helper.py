# -*- coding:utf-8 -*-
# ------------------------------------------------------------------
import sys
from random import choice, uniform
import time
import pathlib
import logging
import logging.config
from contextlib import contextmanager, suppress
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
import socket
import pysnooper
from importlib import reload
import os
# from pyvirtualdisplay import Display
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.proxy import Proxy, ProxyType
import logging

from BotHelper.util_driver import moji_hikaku, page_load, myClick, exe_click, mySendkey, slowClick, my_emojiSend, emoji_convert, add_ifin, send_gmail, mail_what, s3_img
from BotHelper import line_push, writeSheet, change_cell
from dotenv import load_dotenv
import re
import random

lg = logging.getLogger(__name__)

# 環境変数を参照
load_dotenv()
SHEET_NAME = os.getenv('SHEET_NAME')


class Ikkr:

    def __init__(self, tem_ple):
        """

        Args:
            tem_ple (dict): 

        """
        self.tem_ple = tem_ple
        self.myid = self.tem_ple['ik'].split(':')[0]
        self.mypw = self.tem_ple['ik'].split(':')[1]
        self.cnm = tem_ple['cnm']

    @pysnooper.snoop()
    def login(self, driver):
        wait = WebDriverWait(driver, 10)
        lg.debug(self.tem_ple['cnm'])

        try:
            if '0' == self.myid[0]:
                page_load(
                    driver, "https://www.194964.com/registration/login/show_login_tel.html")
                time.sleep(2)
                if driver.current_url == "https://sp.194964.com/menu.html":
                    return True
            else:
                page_load(
                    driver, "https://www.194964.com/registration/login/show_login_mail.html")
                time.sleep(2)
                if driver.current_url == "https://sp.194964.com/menu.html":
                    return 1
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='form1']/div[1]/div/select")))
                Select(driver.find_element(By.NAME, "mailAddressDomain")
                       ).select_by_visible_text("その他のアドレス")

            mySendkey(
                driver, "xpath", "//*[@id='form1']/div[1]/input", self.myid)
            time.sleep(1)
            mySendkey(
                driver, "xpath", "//*[@id='form1']/div[2]/input", self.mypw)
            time.sleep(1)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(3)
            if "ログイン失敗" == driver.find_element(By.ID, "title").text:
                imgName = "{0}.png".format(self.myid)
                driver.get_screenshot_as_file(imgName)
                time.sleep(2)
                sub = "{0}{1}{2}ik潰れたよ".format(self.myid, self.mypw, self.cnm)
                line_push(sub, imgName)
                False

            with suppress(socket.timeout, NoSuchElementException, TimeoutException, Exception):
                myClick(
                    driver, "xpath", "//*[@id=\"osusumeList\"]//img")
            time.sleep(3)
            return True

        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            raise

    def basyo_change(self, namae):

        if '青森' in namae:
            return 8
        if '岩手' in namae:
            return 9
        if '福島' in namae:
            return 10
        if '秋田' in namae:
            return 11
        if '宮城' in namae:
            return 12
        if '山形' in namae:
            return 13
        if '福井' in namae:
            return 15
        if '新潟' in namae:
            return 16
        if '石川' in namae:
            return 17
        if '富山' in namae:
            return 18
        if '東京' in namae:
            return 20
        if '神奈川' in namae:
            return 21
        if '埼玉' in namae:
            return 22
        if '茨木' in namae:
            return 23
        if '栃木' in namae:
            return 24
        if '群馬' in namae:
            return 25
        if '千葉' in namae:
            return 26
        if '岐阜' in namae:
            return 28
        if '長野' in namae:
            return 29
        if '山梨' in namae:
            return 30
        if '愛知' in namae:
            return 32
        if '静岡' in namae:
            return 33
        if '三重' in namae:
            return 34
        if '奈良' in namae:
            return 38
        if '滋賀' in namae:
            return 39
        if '京都' in namae:
            return 41
        if '広島' in namae:
            return 44
        if '島根' in namae:
            return 45
        if '鳥取' in namae:
            return 46
        if '山口' in namae:
            return 47
        if '愛媛' in namae:
            return 49
        if '高知' in namae:
            return 50
        if '香川' in namae:
            return 51
        if '徳島' in namae:
            return 52

        else:
            return 20

    @pysnooper.snoop()
    def toko_check(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 15)
        lg.debug(self.tem_ple["cnm"])
        junList = ["今から遊ぼ", "すぐ会いたい", "大人の出会い", "友達・恋人・合コン", "アブノーマル"]
        basyo = ""
        random.seed()
        try:
            page_load(
                driver, "https://sp.194964.com/bbs/show_bbs_write_list.html")
            # 今投稿しているジャンルをチェック
            myjunls = driver.find_elements(
                By.XPATH, "/html/body/article/div[1]/form[1]//div[@class=\'bgMiddle btn\']//p[@class=\'left btnBorderRound\']")
            myjunl = [myjunls[i].text for i in range(len(myjunls))]
            junlSet = set(junList) - set(myjunl)
            # 全部投稿してたら終了
            if junlSet == set():
                return True
            page_load(
                driver, "https://sp.194964.com/other/area/show_pref_setting_list.html")
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/article/div[1]/span[2]")))
            myadd = driver.find_element(By.XPATH,
                                        "/html/body/article/div[1]/span[2]").text
            if any(map(tem_ple["area"].__contains__, ("名古屋", "愛知", "岐阜", "三重", "長野", "静岡"))):
                basyo = random.choice(
                    [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "愛知", "愛知", "愛知", "愛知", "長野", "三重", "岐阜", "静岡"])
            elif any(map(tem_ple["area"].__contains__, ("埼玉", "千葉", "茨城", "栃木", "群馬", "東京"))):
                basyo = random.choice(
                    [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "埼玉", "埼玉", "埼玉", "茨城", "栃木", "群馬", "千葉", "千葉"])
            elif any(map(tem_ple["area"].__contains__, ("青森", "岩手", "宮城", "福島", "秋田", "山形"))):
                basyo = random.choice(
                    [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "宮城", "宮城", "宮城", "青森", "岩手", "福島", "秋田", "山形"])
            elif any(map(tem_ple["area"].__contains__, ("大阪府", "滋賀県", "京都府", "兵庫県", "奈良県", "和歌山県"))):
                basyo = random.choice(
                    [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "大阪府", "滋賀県", "京都府", "兵庫県", "奈良県", "和歌山県"])

            else:
                basyo = tem_ple["area"]
            junl = random.choice(list(junlSet))
            tokois = self.toko(driver, basyo, junl)
            if not tokois:
                tokois = self.toko(driver, basyo, junl)

            return None

        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            driver.refresh()
            return None

    # ピュア 今から遊ぼ,友達・恋人・合コン
    # アダルト すぐ会いたい、大人の出会い、アブノーマル

    @pysnooper.snoop()
    def toko(self, driver, basyo, junl):
        wait = WebDriverWait(driver, 10)
        tem_ple = self.tem_ple
        lg.debug(tem_ple["cnm"])
        basyo_num = self.basyo_change(basyo)
        random.seed()
        ik_list = []
        try:
            page_load(driver, "https://sp.194964.com/menu.html")
            time.sleep(2)
            # myClick(driver,"xpath","//*[@id=\"osusumeList\"]//img[@class=\"delButton\"]")
            time.sleep(1)
            slowClick(
                driver, "xpath", "//a[@href='/bbs/show_bbs.html']")
            time.sleep(2)
            driver.refresh()
            time.sleep(1)
            slowClick(driver, "link_text", "地域を移動")
            time.sleep(2)
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/article/div/div[20]/a")))
            elm = driver.find_element(
                By.XPATH, "/html/body/article/div/div[{0}]/a".format(int(basyo_num)))
            driver.execute_script("arguments[0].click();", elm)
            time.sleep(2)
            page_load(driver, "https://sp.194964.com/menu.html")
            time.sleep(2)
            # # driver.switch_to.active_element()
            # element = driver.switch_to.active_element
            # element.find_element(By.XPATH, "//*[@id=\"PopupScreen\"]//button[@class=\"close\"]").click()
            # myClick(
            #     driver, "xpath", "//*[@id=\"PopupScreen\"]//button[@class=\"close\"]")
            driver.execute_script("scrollBy(0,800);")
            elm = driver.find_elements(By.LINK_TEXT, "書く")
            if junl == "今から遊ぼ" or junl == "友達・恋人・合コン":
                titles = emoji_convert(tem_ple["title_p"])
                texts = emoji_convert(tem_ple["text_p"])
                ik_list.append(titles)
                ik_list.append(texts)
                elm[0].click()
            else:
                titles = emoji_convert(tem_ple["title_a"])
                texts = emoji_convert(tem_ple["text_a"])
                ik_list.append(titles)
                ik_list.append(texts)
                elm[1].click()
            time.sleep(1)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located)
            el = driver.find_element(
                By.XPATH, "//span[@class=\"subMenu100\" and contains(text(), \"{0}\")]".format(junl))
            el.click()
            time.sleep(2)
            select = Select(driver.find_element(By.XPATH,
                                                "//*[@id=\"formID\"]/div[1]/select"))
            select.select_by_index(random.randint(
                1, (len(select.options) - 1)))
            my_emojiSend(
                driver, "xpath", "//*[@id='formID']/div[3]/textarea[1]", ik_list[0])
            time.sleep(1)
            my_emojiSend(
                driver, "xpath", "//*[@id='formID']/div[3]/textarea[2]", ik_list[1])
            elm = driver.find_element(By.NAME, "write")
            driver.execute_script("arguments[0].click();", elm)
            time.sleep(3)
            return True
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            driver.refresh()
            return None

    @pysnooper.snoop()
    def retoko(self, driver, pure_adlut=None):
        # ピュアかｱﾀﾞﾙﾄどっちを再投稿するか
        junlnum = random.randint(1, 2)

        if (pure_adlut != None) and (pure_adlut == "pure"):
            junlnum = 1
        if (pure_adlut != None) and (pure_adlut == "adult"):
            junlnum = 2
        wait = WebDriverWait(driver, 10)
        tem_ple = self.tem_ple
        lg.debug(tem_ple["cnm"])
        junl_list = []
        try:
            driver.get("https://sp.194964.com/bbs/show_bbs_write_list.html")
            time.sleep(3)
            basyos = driver.find_elements(By.XPATH, "//span[@class=\"area\"]")
            basyo = basyos[-1].text
            basyo_num = self.basyo_change(basyo)
            driver.get("https://sp.194964.com/menu.html")
            time.sleep(2)
            slowClick(
                driver, "xpath", "//a[@href='/bbs/show_bbs.html']")
            time.sleep(2)
            slowClick(driver, "link_text", "地域を移動")
            time.sleep(2)
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/article/div/div[20]/a")))
            elm = driver.find_element(
                By.XPATH, "/html/body/article/div/div[{0}]/a".format(int(basyo_num)))
            driver.execute_script("arguments[0].click();", elm)
            time.sleep(2)
            driver.get("https://sp.194964.com/bbs/show_bbs_write_list.html")
            time.sleep(4)
            toko_elem = "/html/body/div[4]/div[{0}]/a".format(junlnum)
            exe_click(driver, "xpath", toko_elem)
            time.sleep(2)

            last_toko = driver.find_elements(
                By.XPATH, "//div[@class=\"bgMiddle btn\"]//div[@class=\"contentsContribute\"]/a")
            driver.execute_script("arguments[0].click();", last_toko[-1])
            time.sleep(2)
            saitoko = driver.find_elements(
                By.XPATH, "/html/body/article//form/button[@type='submit' and contains(text(), '再投稿する')]")
            if len(saitoko) == 0:
                hensyu = driver.find_elements(
                    By.XPATH, "/html/body/article//form/button[contains(text(), \"編集する\")]")
                if len(hensyu) != 0:
                    hensyu[0].submit()
                    time.sleep(2)
                    exe_click(
                        driver, "xpath", "//*[@id=\"formID\"]/div/button[contains(text(), \"募集する\")]")

                else:
                    delete_elem = driver.find_elements(
                        By.XPATH, "/html/body/article//form/button[contains(text(), \"削除する\")]")
                    if len(delete_elem) != 0:
                        delete_elem[0].submit()
                        time.sleep(2)
                        delete_elem2 = driver.find_elements(By.XPATH,
                                                            "/html/body/article//form/button[contains(text(), \"削除する\")]")
                        if len(delete_elem2) != 0:
                            delete_elem2[0].submit()
                            time.sleep(2)
            else:
                exe_click(
                    driver, "xpath", "/html/body/article//form/button[@type='submit' and contains(text(), \"再投稿する\")]")
                time.sleep(3)
                select = Select(driver.find_element(By.XPATH,
                                                    "//*[@id=\"formID\"]/div[1]/select"))
                select.select_by_index(random.randint(
                    1, (len(select.options) - 1)))
                time.sleep(2)
                exe_click(
                    driver, "xpath", "//*[@id=\"formID\"]/div[4]/button")
            time.sleep(3)
            return True
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            driver.refresh()
            return None

    @pysnooper.snoop()
    def toko_all_delete(self, driver, del_min=4):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 15)
        lg.debug(tem_ple["cnm"])
        try:
            page_load(
                driver, "https://sp.194964.com/bbs/show_bbs_write_list.html")
            time.sleep(1)
            checks = driver.find_elements(
                By.XPATH, "//div[@class=\"bgMiddle btn\"]//input[@type=\"checkbox\"]")
            # 投稿数が5超えたら全削除
            if len(checks) < int(del_min):
                return None
            for che in checks:
                # che.click()
                driver.execute_script("arguments[0].click();", che)
            time.sleep(1)
            #exe_click(driver, "xpath", "//div[@class=\"bgMiddle\"]//button[contains(text(), \"チェックを削除\")]")
            exe_click(
                driver, "xpath", "//button[contains(text(), \"チェックを削除\")]")
            time.sleep(1)
            exe_click(
                driver, "xpath", "//button[contains(text(), \"削除する\")]")
            time.sleep(1)

        except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,
                ElementNotInteractableException, Exception) as e:
            lg.exception(e)

    @pysnooper.snoop()
    def user_prof_todb(self, driver, list_you):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 10)
        lg.debug(tem_ple["cnm"])
        ikdict = {'cnm': tem_ple["cnm"], 'kaiwa': list_you}

        try:
            wait.until(EC.presence_of_all_elements_located)
            user_name = driver.find_element(By.ID, "title").text
            ikdict["name"] = user_name
            profs = driver.find_element(By.XPATH, "/html/body/div[6]").text
            profs = profs.split()
            user_age = profs.pop(0)
            ikdict["age"] = user_age
            user_address = profs.pop(0) + profs.pop(0)
            ikdict["address"] = user_address
            user_info = profs
            ikdict["info"] = user_info
            nowdict = self.tb.get((self.Que.name == user_name) & (
                self.Que.age == user_age) & (self.Que.address == user_address))
            if not nowdict:
                self.tb.insert(ikdict)
            else:
                nowdict.update(ikdict)
                self.tb.upsert(nowdict, (self.Que.name == user_name) & (
                    self.Que.age == user_age) & (self.Que.address == user_address))

        except (TypeError, socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
            lg.exception(e)

    @pysnooper.snoop()
    def memo_mitya(self, driver):
        try:
            driver.execute_script("scrollBy(0,420);")
            exe_click(driver, "xpath", "//*[@id=\"icon-row\"]/a[6]")
            time.sleep(2)
            exe_click(
                driver, "xpath", "//*[@id=\"popup-option\"]/ul[1]/li[1]/a")
            time.sleep(1)
            exe_click(driver, "name", "copy")
            exe_click(
                driver, "xpath", "/html/body/article/div[1]/div[2]/form/div[2]/button")
            time.sleep(2)
            driver.execute_script("scrollBy(0,460);")

            slowClick(driver, "xpath", "//div[2]/div[2]/a/p/span")
            time.sleep(2)
            slowClick(driver, "xpath", "//button[@type='submit']")
            time.sleep(1)
            exe_click(
                driver, "xpath", "//*[@id=\"form1\"]/div[1]/div[2]/p[2]/a")

        except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,
                ElementNotInteractableException, Exception) as e:
            pass

    @pysnooper.snoop()
    def ik_msg(self, driver, nakami):
        lg.debug(self.tem_ple['cnm'])
        try:
            # mySendkey(driver,"name","body",nakami)
            my_emojiSend(driver, "name", "body", nakami)
            time.sleep(1)
            exe_click(driver, "id", "sendButton")
            time.sleep(1)
            slowClick(driver, "id", "submitBtn")
            time.sleep(1)
            slowClick(
                driver, "xpath", "//div[@id='popupContent']/div[2]/button")
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)

    @pysnooper.snoop()
    def ik_tel(self, driver):
        lg.debug(self.tem_ple['cnm'])
        wait = WebDriverWait(driver, 10)
        try:
            exe_click(driver, "link_text", "電話に誘う")
            # mySendkey(driver,"name","telNumber",id_pw["IK_ID"])
            driver.find_element(By.XPATH,
                                "/html/body/article/div[1]/form/button").submit()

        except TypeError:
            pass

    @pysnooper.snoop()
    def ik_my_send(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 10)
        lg.debug(tem_ple["cnm"])
        try:
            # メモがある＝Gメール送った人かどうか確認、送ってたらやめる
            wait.until(EC.presence_of_all_elements_located)
            #me_mo = driver.find_element(By.XPATH, "//p/a/span").text
            # if "メモの確認" in me_mo:
            #    return None
            last_send = driver.find_elements(
                By.XPATH, "//*[@id=\"mailboxList\"]//div")
            namae = driver.find_element(
                By.XPATH, "//*[@id=\"title\"]/ul/li[2]").text
            #namae = namae[1:]
            if len(last_send) == 0:
                asiato = tem_ple['asiato'].replace('namae', namae)
                self.ik_msg(driver, asiato)
                return None

            last_sendd = last_send[-1].get_attribute("class")
            if "OTHER" not in last_sendd.upper():
                return None
            my_send = driver.find_elements(
                By.XPATH, "//*[@id=\"mailboxList\"]//div[@class=\"bubble_owner\"]")
            mylis = [myl.text.replace('★プロフィールから送信', '') for myl in my_send]
            my_receive = driver.find_elements(
                By.XPATH, "//*[@id=\"mailboxList\"]//div[@class=\"bubble_other\"]")
            list_you = [yul.text.replace('★プロフィールから送信', '')
                        for yul in my_receive]

            mylis[-1]
            list_you.extend(mylis)
            mysend = mail_what(
                list_you, tem_ple, namae, asi_if=False, logname="ik")
            if not mysend:
                return None

            self.ik_msg(driver, mysend)
            ikok = moji_hikaku(mysend, tem_ple["after_mail"])
            if ikok:
                self.memo_mitya(driver)
                self.user_prof_todb(driver, tem_ple, list_you)
            return None
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            return None

    @pysnooper.snoop()
    def ik_mail(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 10)
        try:
            page_load(
                driver, "https://sp.194964.com/mail/inbox/show_mailbox.html")
            elm = driver.find_element(By.XPATH, "/html/body/nav/div[3]").text
            ex_mg = re.sub("\\D", "", elm)
            if not ex_mg:
                return True
            for i in range(2, 5, 1):
                if 4 < i:
                    exe_click(driver, "xpath",
                              "/html/body/article/div[1]/div[1]/a")
                    driver.execute_script("scrollBy(0,1200);")
                    wait.until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/article/div[2]/form[2]/div/button"))).submit()
                    wait.until(EC.presence_of_all_elements_located)
                    wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/article/div/form[1]/button"))).submit()
                    wait.until(EC.presence_of_all_elements_located)
                    return True
                driver.execute_script("scrollBy(0,200);")
                new_img = driver.find_elements(
                    By.XPATH, "//div[@class=\"bgMiddle btn \"]//span[@class=\"icon-new-box\"]")
                if not new_img:
                    tugi = driver.find_element(By.LINK_TEXT, "{}".format(i))
                    driver.execute_script("arguments[0].click();", tugi)
                    continue
                else:
                    driver.execute_script("arguments[0].click();", new_img[-1])
                    break

            # メッセージ送信
            wait.until(EC.presence_of_all_elements_located)
            namae = driver.find_element(
                By.XPATH, "//*[@id=\"title\"]/ul/li[2]").text
            my_send = driver.find_elements(
                By.XPATH, "//*[@id=\"mailboxList\"]//div[@class=\"bubble_owner\"]")
            # もし自分の送信がなければ
            if len(my_send) == 0:
                meruado = tem_ple['meruado'].replace('namae', namae)
                self.ik_msg(driver, meruado)
                return None

            last_message = my_send[-1].text.replace('★プロフィールから送信', '')
            if moji_hikaku(last_message, tem_ple["after_mail"]):
                lg.debug('this user after mail sended.')
                return None

            my_receive = driver.find_elements(
                By.XPATH, "//*[@id=\"mailboxList\"]//div[@class=\"bubble_other\"]")
            list_you = [yul.text.replace('★プロフィールから送信', '')
                        for yul in my_receive]
            for r_txt in list_you:
                mailado = add_ifin(r_txt)
                if mailado:
                    kenmei = tem_ple['title_mail'].replace('namae', namae)
                    send_gmail(tem_ple['formurl'], tem_ple['namae'],
                               tem_ple['money'], mailado, kenmei)
                    self.ik_msg(driver, tem_ple["after_mail"])
                    return None

            return None
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            return None


# 0,足跡があるかないか
# 1,足跡なし　＝　足跡送信
# 2,足跡あり　＝　メルアド落としあるか確認
# 2-1,足跡有でメルアド落としなし　＝＝　メルアド落とし
# 2-2,足跡有でメルアド落とし有　＝＝　メルアドあるか確認
# 2-2-1,足跡有でメルアド落とし有でメルアドなし　＝＝　何もしない
# 2-2-2,足跡有でメルアド落とし有でメルアド有　＝＝　見ちゃいや確認(メモ)
# 2-2-2-1,足跡有でメルアド落とし有でメルアド有で見ちゃいや（メモ）なし　＝＝　gmail送信で見ちゃいや（メモ）
# 2-2-2-2,足跡有でメルアド落とし有でメルアド有で見ちゃいや（メモ）有　＝＝　何もしない


    @pysnooper.snoop()
    def asiato_newface(self, driver, ppn):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 10)
        res_word = ""
        try:
            page_load(driver, "https://sp.194964.com/sns/snsashiato/show.html")
            wait.until(EC.presence_of_all_elements_located)
            new_faces = driver.find_elements(
                By.XPATH, "//*[@id=\"tab1\"]//div[@class=\"type-list-name\"]/img")
            try:
                new_face = new_faces[ppn]
            except IndexError:
                return True
            exe_click(driver, "ok", new_faces[ppn])
            time.sleep(2)
            # 履歴確認
            history_btn = driver.find_element(
                By.XPATH, "*//div[@class=\"user-profile-btn-history\"]").get_attribute('style')
            if "none" not in history_btn:
                print('this user exist history. return')
                return None
            namae = driver.find_element(By.ID, "titleNickname").text
            asiato = tem_ple["asiato"].replace('namae', namae)

            msgbtn = driver.find_elements(By.ID, "messageBtn")
            if len(msgbtn) == 0:
                return None
            exe_click(driver, "id", "messageBtn")
            time.sleep(2)
            # 相手が年齢確認してないと定型文以外送れないので定型文を選択
            exe_click(driver, "id", "message-d-1")
            # my_emojiSend(driver, "id", "send-message", asiato)
            time.sleep(1)
            exe_click(driver, "xpath",
                      "//*[@id=\"submitMessageButton\"]/button")
            time.sleep(1)
            # 0,足跡があるかないか
            return None
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            return None

    @pysnooper.snoop()
    def yaungik_asi(self, driver, ppn):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 10)
        try:
            page_load(driver, "https://sp.194964.com/menu.html")
            slowClick(driver, "xpath", "//a[2]/img")
            wait.until(EC.presence_of_all_elements_located)
            yaunglist = []
            agelist = driver.find_elements(
                By.XPATH, "//*[@id=\"tab1\"]//div[@class=\"type-list-age\"]")
            for a in range(len(agelist)):
                ages = re.sub("\\D", "", agelist[a].text)
                if int(ages) < 35:
                    yaunglist.append(agelist[a])
            try:
                a = yaunglist[ppn]
            except IndexError:
                return True
            driver.execute_script("arguments[0].click();", yaunglist[ppn])
            time.sleep(2)
            namae = driver.find_element(By.ID, "titleNickname").text
            asiato = tem_ple["asiato"].replace('namae', namae)

            msgbtn = driver.find_elements(By.ID, "messageBtn")
            if len(msgbtn) == 0:
                return None
            exe_click(driver, "id", "messageBtn")
            time.sleep(2)
            mySendkey(driver, "id", "send-message", asiato)
            time.sleep(1)
            exe_click(
                driver, "xpath", "//*[@id=\"submitMessageButton\"]/button")
            time.sleep(1)
            return None
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            return None

    @pysnooper.snoop()
    def delete_mitya(self, driver):
        wait = WebDriverWait(driver, 10)
        try:
            driver.get(
                "https://sp.194964.com/sns/snsmylist/show_notsees_list.html")
            time.sleep(5)
            miruna = driver.find_element(By.ID, "title").text
            miruna = miruna.split('/')
            miruna_num = re.sub("\\D", "", miruna[0])
            if int(miruna_num) < 30:
                return
            else:
                exe_click(driver, "link_text", "次を表示")
                exe_click(driver, "link_text", "次を表示")
                for ch in range(1, 10, 1):
                    exe_click(
                        driver, "xpath", "//form[@id='form1']/div[{0}]/div[2]/p/label/span".format(ch))

                exe_click(driver, "xpath", "//button[@type='submit']")
                time.sleep(3)
                exe_click(driver, "xpath", "//button[@type='submit']")

        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)

    @pysnooper.snoop()
    def asipeta(self, driver, ppn):

        wait = WebDriverWait(driver, 10)
        try:
            page_load(
                driver, "https://sp.194964.com/profile/profilesearch/show_profile_search.html")
            exe_click(driver, "id", "input_search_outer")
            exe_click(
                driver, "xpath", "(//a[contains(text(),\"プロフィールを見る\")])[{0}]".format(ppn))
            time.sleep(random.randint(8, 16))
            # exe_click(driver,"link_text","あしあとを残す")
            # exe_click(driver,"xpath","//div[@id='popupContent']/div/button")
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)

    # S3から画像をもってきてプロフに

    @pysnooper.snoop()
    def ik_profimg(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 15)
        lg.debug(tem_ple["cnm"])
        try:
            page_load(driver, "https://sp.194964.com/mypage.html")
            noimg = driver.find_element(By.XPATH, "//*[@id=\"prof\"]//div[@class=\"profile-thumb\"]/img").get_attribute(
                "src")
            if "no-img" not in str(noimg):
                return True
            else:
                page_load(
                    driver, "https://sp.194964.com/sns/snssetting/show_image_register.html")
                eximg = driver.find_elements(
                    By.XPATH, "//*[@id='profileWarningBefore']/div")
                ex_num = re.sub("\\D", "", eximg[0].text)
                if ex_num != "3":
                    return None
                myimg = s3_img()
                # imgpath = "./{0}".format(myimg)
                # imgok = os.path.abspath(imgpath)
                driver.find_element(By.ID, "fileupload").send_keys(myimg)
                time.sleep(5)
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='profile_preview_message']/div/button"))).submit()
                time.sleep(3)

            return False
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            return False

    @pysnooper.snoop()
    def prof_text(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 15)
        lg.debug(tem_ple["cnm"])
        random.seed()
        proftext = tem_ple["prof"].strip()
        try:
            page_load(
                driver, "https://sp.194964.com/sns/snssetting/show_edit_profile_intro.html")
            time.sleep(1)
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/article/form/div/div[1]/textarea")))
            word_a = driver.find_element(
                By.XPATH, "/html/body/article/form/div/div[1]/textarea").text
            word_b = proftext
            profok = moji_hikaku(word_a, word_b)
            if profok == True:
                return True
            wait.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/article/form/div/div[1]/textarea"))).clear()
            my_emojiSend(
                driver, "xpath", "/html/body/article/form/div/div[1]/textarea", proftext)
            time.sleep(1)
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/article/form/div/div[3]/button"))).submit()
            time.sleep(2)

            return True
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            return None

    @pysnooper.snoop()
    def ik_prof1(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 15)
        lg.debug(tem_ple["cnm"])
        random.seed()
        if not tem_ple["height"]:
            tem_ple["height"] = "155～159"
        if not tem_ple["style"]:
            tem_ple["style"] = "普通"
        if not tem_ple["marriage"]:
            tem_ple["marriage"] = "未婚"
        myage = "{0}歳".format(tem_ple["age"])
        try:
            page_load(
                driver, "https://sp.194964.com/config/settingprof/show_profile_setting.html")
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.NAME, "name")))
            myname = driver.find_element(
                By.NAME, "name").get_attribute("Value")
            if myname in self.tem_ple["myname"]:
                self.mydict.update({"namae": "ok"})
            else:
                mySendkey(driver, "name", "name", self.tem_ple["myname"])
            select = Select(driver.find_element(By.NAME, "age"))
            age_now = select.all_selected_options[0].text
            if self.tem_ple["age"] in age_now:
                print('age ok')
            else:
                select.select_by_visible_text(myage)
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME, "height")
                       ).select_by_visible_text(tem_ple["height"])
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME, "style")
                       ).select_by_visible_text(tem_ple["style"])
            with suppress(NoSuchElementException):
                bloodtype = random.choice(range(4))
                select = Select(driver.find_element(By.NAME, "blood"))
                select.select_by_index(bloodtype)
            with suppress(NoSuchElementException):
                select = Select(driver.find_element(By.NAME, "looks"))
                max_select = len(select.options) - 1
                sind = random.randint(1, max_select)
                select.select_by_index(sind)
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME, "married")
                       ).select_by_visible_text(tem_ple["marriage"])

            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/article/div/form//button[contains(text(), \"更新する\")]"))).submit()
            time.sleep(4)
            Ikkr.checktb.upsert(self.mydict, Ikkr.Que.id == self.myid)

            return True
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)

    @pysnooper.snoop()
    def ik_prof2(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 15)
        lg.debug(tem_ple["cnm"])
        random.seed()
        try:
            page_load(
                driver, "https://sp.194964.com/sns/snssetting/show_edit_profile.html")
            with suppress(NoSuchElementException):
                select = Select(driver.find_element(By.NAME, "birthCity"))
                max_select = len(select.options) - 1
                sind = random.randint(1, max_select)
                select.select_by_index(sind)
            select = Select(driver.find_element(By.NAME, "occupation"))
            job_now = select.all_selected_options[0].text
            if self.tem_ple["ik_job"] in job_now:
                print('job ok')
            else:
                select.select_by_visible_text(tem_ple["ik_job"])
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME,
                                           "income")).select_by_index(0)
            with suppress(NoSuchElementException):
                select = Select(driver.find_element(By.NAME, "constellation"))
                max_select = len(select.options) - 1
                sind = random.randint(1, max_select)
                select.select_by_index(sind)
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME, "cigarette")
                       ).select_by_visible_text("吸わない")
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME,
                                           "alcohol")).select_by_index(0)
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME, "child")
                       ).select_by_visible_text("いない")
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME, "eyes")
                       ).select_by_visible_text("二重")
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME,
                                           "freeTime")).select_by_index(-1)
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME,
                                           "ageFrom")).select_by_index(1)
            with suppress(NoSuchElementException):
                Select(driver.find_element(By.NAME, "ageTo")).select_by_index(5)
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/article/form/div//button[contains(text(), \"更新する\")]"))).submit()
            Ikkr.checktb.upsert(self.mydict, Ikkr.Que.id == self.myid)
            time.sleep(2)

        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)

    @pysnooper.snoop()
    def ik_basyo(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 15)
        lg.debug(tem_ple["cnm"])
        random.seed()
        try:
            page_load(
                driver, "https://sp.194964.com/other/area/show_pref_setting_list.html")
            time.sleep(2)
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/article/div[1]/span[2]")))
            myadd = tem_ple["area"]
            if any(map(tem_ple["area"].__contains__, ("名古屋", "愛知", "岐阜", "三重", "長野", "静岡", "愛知県", "岐阜県", "三重県", "長野県", "静岡県"))):
                basyo = random.choice(
                    [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "愛知", "愛知", "愛知", "愛知", "長野", "三重", "岐阜",
                     "静岡"])
            elif any(map(tem_ple["area"].__contains__, ("神奈川", "埼玉", "千葉", "茨城", "栃木", "群馬", "東京", "埼玉県", "千葉県", "茨城県", "栃木県", "群馬県", "東京都", "神奈川県"))):
                basyo = random.choice(
                    [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "神奈川", "神奈川", "埼玉", "埼玉", "埼玉", "茨城", "栃木", "群馬", "千葉",
                     "千葉"])

            elif any(map(tem_ple["area"].__contains__, ("青森", "岩手", "宮城", "福島", "秋田", "山形"))):
                basyo = random.choice(
                    [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "宮城", "宮城", "宮城", "青森", "岩手", "福島", "秋田",
                     "山形"])
            else:
                basyo = tem_ple["area"]
            bnm = int(self.basyo_change(basyo)) - 1
            elem = "/html/body/article/div[2]/div[{0}]/a".format(bnm)
            exe_click(driver, "xpath", elem)
            time.sleep(3)
            lens = driver.find_elements(By.XPATH,
                                        "/html/body/article/div[2]/div")
            max_len = len(lens) - 1
            myRum = random.choice(range(1, max_len))
            elem = "/html/body/article/div[2]/div[{0}]/a".format(myRum)
            exe_click(driver, "xpath", elem)
            time.sleep(3)
            driver.get(
                "https://sp.194964.com/profile/profilesearch/show_profile_search.html")
            time.sleep(4)
            exe_click(driver, "id", "city_button")
            time.sleep(4)
            pref_elem = driver.find_elements(
                By.XPATH, "/html/body/article//input[@name='prefAndCity[]']")
            if len(pref_elem) != 0:
                exe_click(
                    driver, "xpath", "/html/body/article//input[@name='prefAndCity[]']")
                time.sleep(1)
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='prefAndCity']/div[2]/button"))).submit()
                time.sleep(2)
                exe_click(driver, "id", "city_button")
                time.sleep(2)
            bnm = int(self.basyo_change(basyo)) + 3
            elem = "/html/body/article/div[1]/div[{0}]/a".format(bnm)
            exe_click(driver, "xpath", elem)
            time.sleep(3)
            driver.find_element(By.ID, "checkbox1").click()
            driver.execute_script("scrollBy(0,1200);")
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='form1']/div[2]/button"))).submit()
            time.sleep(2)
            exe_click(driver, "id", "input_search_outer")
            return True
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)

    @pysnooper.snoop()
    def ik_prof_basyo(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 15)
        lg.debug(tem_ple["cnm"])
        random.seed()
        myadd = tem_ple["area"]
        if any(map(tem_ple["area"].__contains__, ("名古屋", "愛知", "岐阜", "三重", "長野", "静岡", "愛知県", "岐阜県", "三重県", "長野県", "静岡県"))):
            basyo = random.choice(
                [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "愛知", "愛知", "愛知", "愛知", "長野", "三重", "岐阜",
                 "静岡"])
        elif any(map(tem_ple["area"].__contains__, ("神奈川", "埼玉", "千葉", "茨城", "栃木", "群馬", "東京", "埼玉県", "千葉県", "茨城県", "栃木県", "群馬県", "東京都", "神奈川県"))):
            basyo = random.choice(
                [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "神奈川", "神奈川", "埼玉", "埼玉", "埼玉", "茨城", "栃木", "群馬", "千葉",
                 "千葉"])

        elif any(map(tem_ple["area"].__contains__, ("青森", "岩手", "宮城", "福島", "秋田", "山形"))):
            basyo = random.choice(
                [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "宮城", "宮城", "宮城", "青森", "岩手", "福島", "秋田",
                 "山形"])
        elif any(map(tem_ple["area"].__contains__, ("大阪府", "滋賀県", "京都府", "兵庫県", "奈良県", "和歌山県"))):
            basyo = random.choice(
                [myadd, myadd, myadd, myadd, myadd, myadd, myadd, myadd, "大阪府", "滋賀県", "京都府", "兵庫県", "奈良県", "和歌山県"])

        else:
            basyo = tem_ple["area"]

        try:
            driver.get(
                "https://sp.194964.com/profile/profilesearch/show_profile_search.html")
            time.sleep(4)
            exe_click(driver, "id", "city_button")
            time.sleep(4)
            pref_elem = driver.find_elements(
                By.XPATH, "/html/body/article//input[@name='prefAndCity[]']")
            if len(pref_elem) != 0:
                exe_click(
                    driver, "xpath", "/html/body/article//input[@name='prefAndCity[]']")
                time.sleep(1)
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='prefAndCity']/div[2]/button"))).submit()
                time.sleep(2)
                exe_click(driver, "id", "city_button")
                time.sleep(2)
            bnm = int(self.basyo_change(basyo)) + 3
            elem = "/html/body/article/div[1]/div[{0}]/a".format(bnm)
            exe_click(driver, "xpath", elem)
            time.sleep(3)
            driver.find_element(By.ID, "checkbox1").click()
            driver.execute_script("scrollBy(0,1200);")
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='form1']/div[2]/button"))).submit()
            wait.until(EC.presence_of_all_elements_located)
            # time.sleep(3)
            #Select(driver.find_element(By.NAME, "ageTo")).select_by_index(3)
            time.sleep(2)
            exe_click(driver, "id", "input_search_outer")
            return True
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)

    @pysnooper.snoop()
    def ik_aitai(self, driver):
        tem_ple = self.tem_ple
        wait = WebDriverWait(driver, 10)
        lg.debug(tem_ple["cnm"])
        try:
            page_load(driver, "https://sp.194964.com/mypage.html")
            time.sleep(5)
            exe_click(driver, "id", "btn-meetday")
            time.sleep(2)
            wait.until(EC.presence_of_all_elements_located)
            time.sleep(2)
            aitai = driver.find_elements(
                By.XPATH, "//*[@id=\"calendar\"]//span[@class=\"fc-day-number selectDate\"]")
            elem = driver.find_elements(By.XPATH,
                                        "//*[@id=\"calendar\"]//td[contains(@class, \"fc-future\")]/span")
            for ele in elem:
                ele.click()
            # slowClick(driver,"ok",elem[0])
            time.sleep(1)
            slowClick(driver, "id", "saveBtn")
            time.sleep(5)
            # element = driver.switch_to.active_element
            # element.find_element(By.ID, "successCalendar").click()

            #slowClick(driver, "id", "successCalendar")
            time.sleep(3)
            return None
        except (socket.timeout, NoSuchElementException, TimeoutException,
                ElementClickInterceptedException, ElementNotInteractableException, Exception) as e:
            lg.exception(e)
            return None

    @pysnooper.snoop()
    def toko_mitya_check(self, driver):
        self.toko_all_delete(driver)
        tockis = self.toko_check(driver)
        if not tockis:
            retois = self.retoko(driver)
            if not retois:
                retois = self.retoko(driver)
        self.delete_mitya(driver)
