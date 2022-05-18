import os
import re

import requests
from bs4 import BeautifulSoup as bs, element
from web3 import eth, contract, Web3
import time
import pandas as pd


import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


import time
import numpy as np
from selenium import webdriver

URL_token = 'https://etherscan.io/token/'
infura_url = []

infura_url.append("https://mainnet.infura.io/v3/1c71753252df499cab6273d110ab7e52")
infura_url.append("https://mainnet.infura.io/v3/f6001581b0f34af7abe1af48dda3d835")
infura_url.append("https://mainnet.infura.io/v3/72eb988bdc3d432fa65f2130f1444516")
infura_url.append("https://mainnet.infura.io/v3/3137bd8a2c4a40228f47f4ef18ce24b0")
infura_url.append("https://mainnet.infura.io/v3/c7929b3eaa4e4a38924b8f5dc02c8a43")
infura_url.append("https://mainnet.infura.io/v3/16bd8d41c1084ee1aba7404e088f1670")
infura_url.append("https://mainnet.infura.io/v3/fd567b901f3648128074dfb97c3dfb99")
infura_url.append("https://mainnet.infura.io/v3/8b5d96ae74ec43059b32740f7ccfe595")
infura_url.append("https://mainnet.infura.io/v3/5690a3fd70bf4afca7342d5748af164b")
infura_url.append("https://mainnet.infura.io/v3/aaf7776d32504a87a4d7b62fedda9bdc")

web3 = []
for i in range(len(infura_url)):
    web3.append(Web3(Web3.HTTPProvider(infura_url[i])))

def crawling_data_ether(tx_address,page):
    raw_data = {
        'Txn Hash': [],
        'Method': [],
        'Timestamp': [],
        'From': [],
        'To': [],
        'TokenID': []
    }
    # 드라이버 연결
    driver = webdriver.Chrome()
    driver.maximize_window()
    # 카운팅
    cnt = 0
    try:
        # 웹사이트 이동
        driver.get(URL_token + tx_address)
        # 로딩 대기
        driver.implicitly_wait(5)
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "tokentxnsiframe")))
        elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="maindiv"]/div[2]/table/tbody/tr[1]/td[2]/span/a')))
        # 테이블 서치
        table = driver.find_element(By.XPATH,'//*[@id="maindiv"]/div[2]/table')

        for j in range(1,page+1):
            for i in range(1,26):
                Xpath_Txn_Hash = '//*[@id="maindiv"]/div[2]/table/tbody/tr['+ str(i) +']/td[2]/span/a'
                Xpath_Method = '//*[@id="maindiv"]/div[2]/table/tbody/tr['+ str(i) +']/td[3]/span'
                Xpath_From_Address = '//*[@id="maindiv"]/div[2]/table/tbody/tr['+ str(i) +']/td[8]/a'
                Xpath_To_Address = '//*[@id="maindiv"]/div[2]/table/tbody/tr['+ str(i) +']/td[6]/a'
                Xpath_TokenID = '//*[@id="maindiv"]/div[2]/table/tbody/tr['+ str(i) +']/td[9]/a'
                Xpath_timestamp = '//*[@id="maindiv"]/div[2]/table/tbody/tr['+ str(i) +']/td[5]/span' #title

                Txn_Hash = table.find_element(By.XPATH, Xpath_Txn_Hash).get_attribute('innerText')
                Method = table.find_element(By.XPATH, Xpath_Method).get_attribute('innerText')
                From_Address = table.find_element(By.XPATH, Xpath_From_Address).get_attribute('innerText')
                To_Address = table.find_element(By.XPATH, Xpath_To_Address).get_attribute('innerText')
                Token_Id = table.find_element(By.XPATH, Xpath_TokenID).get_attribute('innerText')
                timestamp = table.find_element(By.XPATH, Xpath_timestamp).get_attribute('title')

                raw_data['Txn Hash'].append(Txn_Hash)
                raw_data['Method'].append(Method)
                raw_data['Timestamp'].append(timestamp)
                raw_data['To'].append(To_Address)
                raw_data['From'].append(From_Address)
                raw_data['TokenID'].append(Token_Id)


    except:
        print("crawling data error")

    finally:
        # 브라우저 (드라이버) 종료
        driver.quit()
        return raw_data


def get_Token_Dataframe(data, w_num):
    table_df = pd.DataFrame(data)
    value = []
    tx_to = []
    for i in range(len(table_df)):
        transaction = web3[w_num].eth.getTransaction(table_df.loc[i]['Txn Hash'])
        value.append(transaction['value'] / 1000000000000000000)
        tx_to.append(transaction['to'])

    table_df['Contract Address'] = tx_to
    table_df['value'] = value
    print(table_df)

    return table_df

def create_csv(Token_address, Name, web3_num, pagenum):
    address = Token_address
    csv_name = Name + ".csv"
    w_num = web3_num
    lastpage = pagenum

    for i in range(1,lastpage+1):

        print(Name, "현재페이지 :", i)

        # web3 초과 요청 방지
        if i + 1 % 500 == 0:
            if w_num < 9:
                w_num = w_num + 1
                print("change web3 : ", w_num)
            else:
                w_num = 0
                print("change web3 : ", w_num)

        global error
        try:
            dic_data = crawling_data_ether(address, i)
            df_data = get_Token_Dataframe(dic_data, w_num)
        except:
            print()
            # try:
            #     error = 1
            #     dic_data = crawling_data_ether(address, i)
            #     df = get_Token_Dataframe(dic_data, w_num)
            #     error = 0
            # except:
            #     error = 2
            #     dic_data = crawling_data_ether(address, i)
            #     df = get_Token_Dataframe(dic_data, w_num)
            #     error = 0

        if not os.path.exists("token/" + csv_name):
            df_data.to_csv("token/" + csv_name, index=False, mode='w', encoding='utf-8-sig')
        else:
            df_data.to_csv("token/" + csv_name, index=False, mode='a', encoding='utf-8-sig', header=False)


def main():



    token_list_df = pd.read_csv('token_contract_list.csv')
    web3_num = 0
    for i in range(len(token_list_df)):
        if web3_num >= 10:
            web3_num = 0
        print("현재 web3_num", web3_num)
        print("현재 진행상황 : ", i)

        token_contract = token_list_df.loc[i]['contract']
        address = token_contract

        url = "https://etherscan.io/token/" + str(address)
        # # 드라이버 연결
        # driver = webdriver.Chrome()
        # # 웹사이트 이동
        # driver.get(URL_token + address)
        # # 로딩 대기
        # driver.implicitly_wait(5)

        #lastpage = driver.find_element(By.XPATH,'//*[@id="maindiv"]/div[1]/nav/ul/li[3]/span/strong[2]').get_attribute('innerText')

        token_name = re.sub(r"[?!$/'.,]", "", token_list_df.loc[i]['Token'])
        if len(token_name) > 151:
            token_name = token_name[0:150]

        create_csv(token_contract, token_name, web3_num, int(1))
        web3_num = web3_num + 1


main()


