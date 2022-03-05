from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import telebot
import time

import hmac
from urllib.parse import urlencode

options = Options()
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True

bot = telebot.TeleBot('')
group_id = ''

Key = ''
Secret = ''


class Main:
    def __init__(self):
        self.email = ''
        self.password = ''
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)  # seconds
        self.wallet_usd = 0
        self.wallet_btc = 0
        self.start_usd = 0
        self.start_btc = 0
        self.current_price = 0
        self.last_order_price = 0
        self.coin = 'BTC'
        self.current_percent = 0
        self.order_type = ''
        self.order_price = 0
        self.isNextOperationBuy = True

        self.UPWARD_TREND_THRESHOLD = 0.25
        self.DIP_THRESHOLD = -0.35
        self.PROFIT_THRESHOLD = 0.75
        self.STOP_LOSS_THRESHOLD = -0.75
        self.lastOpPrice = 100.00

    def login(self):
        self.driver.get("https://btc-alpha.com/ru/login")
        login = self.driver.find_element_by_xpath('//*[@id="email"]')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        btn = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div[1]/form/div[3]/button')
        login.send_keys(self.email)
        password.send_keys(self.password)
        btn.click()
        fa = False
        if fa:
            fa_code = input('Введите код аутентификатора (6 цифр): ')
            fa_code_1.fa_code_2, fa_code_3, fa_code_4, fa_code_5, fa_code_6 = fa_code[0], fa_code[1], fa_code[2], \
                fa_code[3], fa_code[4], fa_code[5]
            fa1 = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/form/div[1]/div/div/div[2]/div/div[1]/input')
            fa1.send_keys(fa_code_1)
            fa2 = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/form/div[1]/div/div/div[2]/div/div[2]/input')
            fa2.send_keys(fa_code_2)
            fa3 = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/form/div[1]/div/div/div[2]/div/div[3]/input')
            fa3.send_keys(fa_code_3)
            fa4 = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/form/div[1]/div/div/div[2]/div/div[4]/input')
            fa4.send_keys(fa_code_4)
            fa5 = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/form/div[1]/div/div/div[2]/div/div[5]/input')
            fa5.send_keys(fa_code_5)
            fa6 = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/form/div[1]/div/div/div[2]/div/div[6]/input')
            fa6.send_keys(fa_code_6)

    def open_trade(self):
        self.driver.get(
            "https://btc-alpha.com/ru/demo/BTCd_USDTd?layout=advanced&type=spot")

    def update_current_price(self):
        API_URL = 'https://api3.binance.com/api/v3/avgPrice'
        data = {'symbol': f'{self.coin}USDT'}
        response = requests.get(API_URL, data)
        self.current_price = float(response.json()['price'])

    def get_auth_headers(self, data):
        from time import time
        msg = Key + urlencode(sorted(data.items(), key=lambda val: val[0]))
        sign = hmac.new(Secret.encode(), msg.encode(),
                        digestmod='sha256').hexdigest()
        return {
            'X-KEY': Key,
            'X-SIGN': sign,
            'X-NONCE': str(int(time() * 1000)),
        }

    def update_wallet(self):
        # Получение баланса по АПИ
        response = requests.get(
            'https://btc-alpha.com/api/v1/wallets/', headers=self.get_auth_headers({})).json()
        for resp in response:
            if resp['currency'] == 'USDTd':
                self.wallet_usd = resp['balance']
            if resp['currency'] == 'BTCd':
                self.wallet_btc = resp['balance']

    def buy(self):
        btn = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[1]/div[1]')
        btn.click()
        mrkt = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[2]/div[2]')
        mrkt.click()
        count_percent_25 = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[3]/div[4]/div[1]')
        count_percent_50 = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[3]/div[4]/div[2]')
        count_percent_75 = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[3]/div[4]/div[3]')
        count_percent_100 = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[3]/div[4]/div[4]')
        count_percent_25.click()
        order_btn = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div/div[2]/div[4]/div/div[3]/button')
        order_btn.click()

    def sell(self):
        btn = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[1]/div[2]')
        btn.click()
        mrkt = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[2]/div[2]')
        mrkt.click()
        count_percent_25 = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[3]/div[4]/div[1]')
        count_percent_50 = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[3]/div[4]/div[2]')
        count_percent_75 = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[3]/div[4]/div[3]')
        count_percent_100 = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div[1]/div[2]/div[4]/div/div[3]/div[4]/div[4]')
        count_percent_25.click()
        order_btn = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/main/div/div[2]/div[4]/div/div[3]/button')
        order_btn.click()

    def calculate(self, a, b):
        res = (float(a) * 100 / float(b)) - 100
        res = float('{:.3f}'.format(res))
        return res

    def order_report(self):
        self.update_wallet()
        usd_percent = self.calculate(self.wallet_usd, self.start_usd)
        btc_percent = self.calculate(self.wallet_btc, self.start_btc)
        main_wallet = float(self.wallet_usd) + \
            (float(self.current_price) * float(self.wallet_btc))
        main_percent = self.calculate(main_wallet, self.start_wallet)
        main_fin = main_wallet - self.start_wallet
        usd_percent = float('{:.3f}'.format(usd_percent))
        btc_percent = float('{:.3f}'.format(btc_percent))
        main_percent = float('{:.3f}'.format(main_percent))
        current_price = float('{:.3f}'.format(self.current_price))
        wallet_usd = float('{:.3f}'.format(float(self.wallet_usd)))
        wallet_btc = float('{:.3f}'.format(float(self.wallet_btc)))

        usd_percent = float('{:.3f}'.format(usd_percent))
        last_order_price = float('{:.3f}'.format(self.last_order_price))
        current_percent = float('{:.3f}'.format(self.current_percent))
        order_price = 0
        if usd_percent < 0:
            usd_perc = str(usd_percent) + '% 🔻'
        else:
            usd_perc = str(usd_percent) + '% 🔺'

        if btc_percent < 0:
            btc_perc = str(btc_percent) + '% 🔻'
        else:
            btc_perc = str(btc_percent) + '% 🔺'

        if main_percent < 0:
            main_perc = str(main_percent) + '% 🔻'
        else:
            main_perc = str(main_percent) + '% 🔺'
        if float(self.order_price) == 0:
            pass
        else:
            msg = f'Текущий курс BTC-USD: {current_price}\nБаланс USD: {wallet_usd} : {usd_perc}\nБаланс BTC: {wallet_btc} : {btc_perc}\nОбщий баланс: {main_wallet}\nОбщая прибыль: {main_fin} : {main_perc}\nСумма сделки: {self.order_price}\nТип сделки: {self.order_type} \nПроцент изменения: {current_percent} %'
            bot.send_message(group_id, text=msg)

    def main(self):
        # self.login()
        try:
            self.open_trade()
            self.update_wallet()
            self.update_current_price()
            self.last_order_price = self.current_price
            self.buy()
            # Получение баланса по АПИ
            response = requests.get(
                'https://btc-alpha.com/api/v1/wallets/', headers=self.get_auth_headers({})).json()
            for resp in response:
                if resp['currency'] == 'USDTd':
                    self.start_usd = resp['balance']
                if resp['currency'] == 'BTCd':
                    self.start_btc = resp['balance']
            self.start_wallet = float(
                self.start_usd) + (float(self.start_btc) * float(self.current_price))
            try:
                while True:
                    time.sleep(1)
                    self.update_wallet()
                    self.update_current_price()
                    current_percent = self.calculate(
                        self.current_price, self.last_order_price)
                    self.current_percent = current_percent
                    print('Текущая цена:' + str(self.current_price))
                    print('Цена последней сделки:' +
                          str(self.last_order_price))
                    print(current_percent)
                    percentageDiff = (float(
                        self.current_price) - float(self.lastOpPrice)) / float(self.lastOpPrice) * 100
                    if self.isNextOperationBuy:
                        if percentageDiff >= self.UPWARD_TREND_THRESHOLD or percentageDiff <= self.DIP_THRESHOLD:
                            self.buy()
                            self.order_type = 'Покупка'
                            self.order_price = float(self.driver.find_element_by_xpath('//*[@id="buy-amount"]').get_attribute(
                                "value"))
                            self.last_order_price = self.current_price
                            self.lastOpPrice = self.current_price
                            self.isNextOperationBuy = False
                            self.order_report()
                    else:
                        if percentageDiff >= self.PROFIT_THRESHOLD or percentageDiff <= self.STOP_LOSS_THRESHOLD:
                            self.sell()
                            self.order_type = 'Продажа'
                            self.order_price = float(self.driver.find_element_by_xpath('//*[@id="sell-amount"]').get_attribute(
                                "value"))
                            self.last_order_price = self.order_price
                            self.lastOpPrice = self.current_price
                            self.isNextOperationBuy = True
                            self.order_report()
            except Exception as e:
                bot.send_message(group_id, text=e)
        except:
            self.driver.quit()


Main().main()
