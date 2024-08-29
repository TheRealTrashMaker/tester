import re
import time

import requests
from bsedata.bse import BSE


def get_stockcode(stock_name):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "origin": "https://www.bseindia.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.bseindia.com/",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    url = "https://api.bseindia.com/Msource/1D/getQouteSearch.aspx"
    params = {
        "Type": "EQ",
        "text": stock_name,
        "flag": "site"
    }
    response = requests.get(url, headers=headers, params=params)
    stock_code = re.findall(f"{stock_name.lower()}/(.+?)/", response.text)
    if stock_code:
        return stock_code[0]
    else:
        return None


def get_stock_info_pre(stock_code):
    b = BSE(update_codes=True)
    q = b.getQuote(stock_code)
    if q:
        return q
    else:
        return None


def get_stock_current_info(stock_name):
    stock_code = get_stockcode(stock_name=stock_name)
    if stock_code:
        stock_info_pre = get_stock_info_pre(stock_code)
        stock_info = {
            "close_prices": [
                [
                    int(time.time()*1000),
                    stock_info_pre["currentValue"]
                ]
            ],
            "companyName": stock_info_pre["companyName"],
            "current_price": stock_info_pre["currentValue"],
            "percent_change": stock_info_pre["pChange"],
            "prasent": 0,
            "stock": stock_info_pre["securityID"]
        }
        return stock_info
    else:
        return None


if __name__ == '__main__':
    print(get_stock_current_info("POBS"))
