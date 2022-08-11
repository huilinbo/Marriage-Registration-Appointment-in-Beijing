#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ddddocr
import itchat
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# 二维码登录微信
itchat.auto_login(enableCmdQR=2, hotReload=True)

while True:

    available = False

    # 领证的手机版页面，比较好操作
    url = "https://ggfw.mzj.beijing.gov.cn/weimarryout/marryout/marry/stepOne.do?method=wxStepOne&tag=1&opType=IA"
    nameMan = "张三"
    idMan = "123456789098765432"    # 身份证号
    noMan = "12345678901"   # 手机号
    regIdMan = 1    # 男生户口注册地的索引
    nameWoMan = "李四"
    idWoMan = "123456789098765432"
    noWoMan = "12345678901"
    regIdWoMan = 1  # 女生户口注册地的索引
    regPlaceId = 6  # 领证地点的索引
    dateId = 2  # 领证日期的索引

    driver = webdriver.Chrome()     # 安装谷歌浏览器驱动 https://blog.csdn.net/zhoukeguai/article/details/113247342
    driver.get(url)
    driver.find_element(By.XPATH, '//*[@id="container"]/div[20]/div/div/div[2]/ul/li[1]').click()   # 点击进入下一页
    sleep(1)
    # 填写相关信息
    driver.find_element(By.XPATH, '//*[@id="container"]/div[3]/div/input').send_keys(nameMan)
    Select(driver.find_element(By.XPATH, '//*[@id="certTypeMan"]')).select_by_index(1)
    driver.find_element(By.XPATH, '//*[@id="container"]/div[5]/div/input').send_keys(idMan)
    driver.find_element(By.XPATH, '//*[@id="container"]/div[6]/div/input').send_keys(noMan)
    Select(driver.find_element(By.XPATH, '//*[@id="regSjMan"]')).select_by_index(regIdMan)
    driver.find_element(By.XPATH, '//*[@id="container"]/div[9]/div/input').send_keys(nameWoMan)
    Select(driver.find_element(By.XPATH, '//*[@id="certTypeWoman"]')).select_by_index(1)
    driver.find_element(By.XPATH, '//*[@id="container"]/div[11]/div/input').send_keys(idWoMan)
    driver.find_element(By.XPATH, '//*[@id="container"]/div[12]/div/input').send_keys(noWoMan)
    Select(driver.find_element(By.XPATH, '//*[@id="regSjWoman"]')).select_by_index(regIdWoMan)
    Select(driver.find_element(By.XPATH, '//*[@id="deptCode"]')).select_by_index(regPlaceId)
    sleep(5)    # 等待网页反应
    Select(driver.find_element(By.XPATH, '//*[@id="bookDate"]')).select_by_index(dateId)

    # 判断还能不能预约
    if driver.find_element(By.XPATH, '//*[@id="bookTimeId"]/tbody/tr[2]/td[4]').text != '70':
        driver.find_element(By.XPATH, '//*[@id="bookTimeId"]/tbody/tr[2]/td[1]/input').click()
        available = True
    elif driver.find_element(By.XPATH, '//*[@id="bookTimeId"]/tbody/tr[3]/td[4]').text != '45':
        driver.find_element(By.XPATH, '//*[@id="bookTimeId"]/tbody/tr[3]/td[1]/input').click()
        available = True

    if available:
        # 导出验证码
        with open('./tmp.png', 'wb') as file:
            file.write(driver.find_element(By.XPATH, '//*[@id="checkImage"]').screenshot_as_png)

        # 识别验证码
        ocr = ddddocr.DdddOcr()
        with open('./tmp.png', 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        driver.find_element(By.XPATH, '//*[@id="container"]/div[18]/div/input').send_keys(res)
        # 点击预约！
        driver.find_element(By.XPATH, '//*[@id="container"]/div[19]/div/a').click()

        # 微信提醒已预约成功
        users = itchat.search_friends(name="微信备注名")    # 给女生发消息（给自己发消息似乎不能成功）
        itchat.send('已成功预约！', toUserName=users[0]['UserName'])
        print(users[0]['UserName'])
        itchat.send('已成功预约！', toUserName='filehelper')    # 给文件浏览器发消息

        # 预约成功后退出
        exit()
    
    # 每隔30秒爬取一次
    sleep(30)

