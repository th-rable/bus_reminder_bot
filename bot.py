import time
import discord
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

optionss = webdriver.ChromeOptions()
optionss.add_argument('headless')

url = 'https://www.kobus.co.kr/mrs/rotinf.do'

client = discord.Client(intents=discord.Intents.default())
token = 'token'

def f1(a,b):
    WebDriverWait(b, 10).until(EC.presence_of_element_located((By.XPATH,a)))
    b.find_element(By.XPATH, a).click()

def refresh():
    browser = webdriver.Chrome('', options=optionss)
    browser.get(url)
    a = '//*[@id="readDeprInfoList"]/p/span[1]'
    f1(a,browser)
    a = '//*[@id="imptDepr"]/p[2]/span[1]'
    f1(a,browser)
    a = '/html/body/div[3]/div/div[2]/div[4]/div/div[1]/div[1]/ul/li[5]/span'
    f1(a,browser)
    a = '//*[@id="tableTrmList"]/li[13]/span'
    f1(a,browser)
    time.sleep(1)
    a = '/html/body/div[3]/div/div[1]/button'
    f1(a,browser)

    a = '//*[@id="deprNxdChc"]' # 날짜
    f1(a,browser)

    a = '//*[@id="alcnSrchBtn"]/button'
    f1(a,browser)

    try:
        WebDriverWait(browser, 3).until(EC.alert_is_present())
        alert = browser.switch_to.alert

        alert.accept()
        WebDriverWait(browser, 3).until(EC.alert_is_present())
        alert = browser.switch_to.alert

        alert.accept()
    except:
        print("no alert")

    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "bus_time")))

    html_comments = browser.find_elements(By.CLASS_NAME, "bus_time")
    print(html_comments[0].text)


    print(len(html_comments))

    buslist = html_comments[0].text.split('\n')

    busarray = np.zeros((100, 5))
    busarray = busarray.astype(str)

    busarray[0][0]=len(buslist)-3

    i = 0
    idx = 1
    for x in range(3, len(buslist)):

        busarray[idx][i] = buslist[x]
        i += 1
        if i % 5 == 0:
            i = 0
            idx += 1

    browser.close()
    return busarray

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.wait_until_ready()
    channel = client.get_channel(ID)
    time.sleep(5)

    nowbusarray=None
    beforebus=None
    isfirst = True
    while True:
        beforebus = nowbusarray
        nowbusarray = refresh()
        print(nowbusarray)

        if isfirst:
            print("** 시작 **")
            isfirst = False
            time.sleep(20)
            continue;

        if beforebus[0,0] == nowbusarray[0,0]:
            print("** 버스 추가 없음 **")
        else:
            print("** 버스 추가 **")
            await channel.send("*** !!!!버스가 새로 추가됨!!!! *** @everyone")
            time.sleep(20)
            continue;

        for x in range(int(nowbusarray[0,0])//5):
            if beforebus[x,4]!=nowbusarray[x,4]:
                print('** 버스 자리 변경 **')
                print('시간 : %s , %s -> %s'%(nowbusarray[x,0],beforebus[x,4],nowbusarray[x,4]))
                await channel.send('** 버스 자리 변경 **')
                await channel.send('시간 : %s , %s -> %s  @everyone' % (nowbusarray[x, 0], beforebus[x, 4], nowbusarray[x, 4]))

        time.sleep(20)

client.run(token)