# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ブラウザを開く。
driver = webdriver.Chrome()
driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
# Googleの検索TOP画面を開く。
driver.get("https://www.google.co.jp/")
# 検索語として「selenium」と入力し、Enterキーを押す。
driver.find_element_by_id("lst-ib").send_keys("weblio 対義語")
driver.find_element_by_id("lst-ib").send_keys(Keys.ENTER)
# タイトルに「Selenium - Web Browser Automation」と一致するリンクをクリックする。
driver.find_element_by_link_text("対義語検索 - Weblio類語辞典 - Weblio辞書").click()
sleep(5)
#element = driver.find_elements_by_xpath("//*[@id='headBxTL']")

#driver.find_element_by_id("combo_txt").send_keys("ガリガリ")
#driver.find_element_by_id("combo_txt").send_keys(Keys.ENTER)

# 5秒間待機してみる。

sleep(5)
# ブラウザを終了する。
driver.close()
