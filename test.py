import time

import requests
from datetime import datetime
from flask import Flask, request, jsonify
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

@app.route('/history_1day/<regulation>', methods=['GET'])
def nse_charter(regulation):
    """
    获取股票跌幅数据
    :param regulation: SYMBOL
    :return:
    """
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        # 'cookie': '_ga=GA1.1.1473576843.1720061795; AKA_A2=A; nsit=O5Hno77xSNxqOK1bk4q_BvM-; _abck=B8FA317C7DA408AE9FE4AE65328B0E6F~0~YAAQUGDQFztg0puQAQAAckycoAwLwjR3pD0KJOkwGEAI+pkhWl5Ea5vIIfQsfd2TfMNCRGCXTSe9XE9HaJBTwOs72LU8semDI6NwF4aUHX6pgPVFaespjuYj+tdMuw74jFYri6rTr3GHwZRAffdJBQaU1FgHoiwmluCOzNw1K30/4/dEfkzDSZ5piK6Ivu3hSowZhlCnGEqZwS5b0X1HDfIGKblZVGX9z2vaNQIFgV6twYEypjZFQGBIQKdiJxaboXe1XQ7AB436o8T6Mb57hd7NvQarxfO4xV78K1CQcLWvVe+0njqkAlIB7q31oRnjWuiSz+QOxLdENJScAF+wzj6JPoiNeR+4LsLaD4FKPVGpP1xCNaeF7eRIWC01ugv+6NbC+ZKJRHt0eqCVWhq5eDeprJrGOXiZcK3h~-1~-1~-1; defaultLang=en; ak_bmsc=6D953EE2E6BFF7DB4AC0B95A939FE47D~000000000000000000000000000000~YAAQUGDQFw9i0puQAQAAQlqcoBilXWAi1E8FO8cNiJWhgLiGdIDTmB4hj6GmcvNxTpO8TJbx6XL3Q5Rxt+YmRip8+4/yoeZeO6Q1httZJQWQDKQseLGXzBe20yXHsB05fn1FMq4QaIU+77gvEGLho+owB9FDgT0UbgkXliTEbOM+2bZS8nkRk528t+xiuOUDkSdHj0yqdFcH7UPKIC5tAZ0fMk5007FfK2F7bzENsfN2gl0fXDKM6qAOoz2HBRCJvqsdfB28Xq8qkEOJFuC7hnG/phJwlXcy/bpBb9nefnXI4SxsI3/ChDkevn6VqKUZ4HfO4GJRyK4mKsigdpDXpbVQ0xG9+Rge6e+ErIeLkZqmGMzqKiUwxnNeWnvOe7ZIqSQBvBouuVmmZxvR+rLSd7S8XXIIfUPxp0ylsvG0V1tJ44vZoPAU33tFaOfiyR3k1+AX6SbUhcHbE3IXsQ==; nseQuoteSymbols=[{"symbol":"MALLCOM","identifier":null,"type":"equity"},{"symbol":"EFFWA","identifier":null,"type":"equity"},{"symbol":"960IIFLS26","identifier":null,"type":"bonds"},{"symbol":"ACCENTMIC","identifier":null,"type":"equity"}]; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTcyMDY4MzAyMSwiZXhwIjoxNzIwNjkwMjIxfQ.MZb9BW17CzdZmjDrmjmgNhcz7cHhYKdv0cNlyNngTQI; bm_sz=0C15F5CDFF51FEC3F6DE98C8EC0E74EF~YAAQUGDQF5yR1ZuQAQAACUazoBjj/LGz4sUbkuSnlIFXHmSmNvejdasuAfsQYSV9PdbqkOtf3PH6YrQCNbJgErBKS0sPnnJQTd6cOwAsfQo/vQtfZqlaq/EFKFgifgGsRnpvsDlNrxb8Yidzdtzr0IS8unFNM8pZrpEocM6zsf7XVh1XcRRhAgnZqsB3cnH1zJQSaYgYCIeoQXzNU/2WalvDn2f1RfU1NN5O1v18myVKDWyV/9qxQLjnr7mmbe8Si3syUE8h427eP/DcKBbHhQ8aH/wdrI4WPkYMH0d1Ux3/3dt97HI4mFvs2oD7vQg7Q1RmwGLA4Q/v3dcvhF8x0GpJifxTzCMKbstcXmmrGsmutM5kJKvwf1eYvV2jlPzNhejSoy3tGgHXuGO3PkXre70HPT6w4HkITXpX+yJIRQz0y3zPq0Tfr5h3Z2STkfrser9LYw4LsCmiCqd8/WkCYbr5QXeQncdmLytZMf13NhryIA3fak8G+nlR1+L/n/vI~4408624~4277813; RT="z=1&dm=nseindia.com&si=3baf6c92-35fa-4b8e-84b6-806fe51a5595&ss=lygy2895&sl=6&se=8c&tt=hw0&bcn=%2F%2F17de4c12.akstat.io%2F"; _ga_87M7PJ3R97=GS1.1.1720680771.14.1.1720683028.16.0.0; bm_sv=62C4F6B0B7A3E4FD0FCDC8200A77C4A8~YAAQUGDQFy6m1ZuQAQAAf2OzoBhjk1slm7ifAMSJXVo87ml27pQua72Ia+W8dnrhG99HEJ5zxYNz5xPJgUCNsxD7OKwDn0mzu8stsxYM6rhCsNXf9RbycVFXY5RPx4FCuY0aeWtfz6uTwacah9Yzx7lhn3LH5+jUUEIjXaKDvOJwMAVsveTjeTWnqgzzZgc5gfmhAzeXQerHteroP2rlQe5vsma8qfMWWEg6gJIAeoxnWnLnOiBA+6EYUXevKBkVTiuP3w==~1',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'https://www.nseindia.com/get-quotes/equity?symbol={regulation}',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        'symbol': f'{regulation}',
    }
    session = requests.Session()
    session.get(url='https://www.nseindia.com/', headers=headers)
    response = session.get('https://www.nseindia.com/api/quote-equity', params=params,
                            headers=headers)
    try:
        params_S = {
            'index': response.json()["info"]["identifier"],
            'type': 'symbol',
        }
        response_s = session.get('https://www.nseindia.com/api/chart-databyindex', params=params_S,
                                headers=headers)
        json_data = response_s.json()

        def filter_continuous_prices(data):
            if not data:
                return []

            filtered_data = [data[0]]  # 初始化保留第一个元素

            for i in range(1, len(data)):
                if data[i][1] != data[i - 1][1]:  # 价格不同才添加到结果中
                    filtered_data.append(data[i])

            return filtered_data

        filtered = []
        filtered_datas = filter_continuous_prices(json_data["grapthData"])
        for filtered_data in filtered_datas:
            filtered.append(filtered_data[1])
        new_json_data = {
            "companyName": response.json()["info"]["companyName"],
            "close_prices": filtered,
            "current_price": response.json()["priceInfo"]["lastPrice"],                 # 当前的股票价格
            "percent_change": response.json()["priceInfo"]["change"],    # 今日股票价格的百分比变化
            "prasent": response.json()["priceInfo"]["pChange"],                              # 表示当前的变化值
            "stock": json_data['name']                          # 股票的名称
        }
        # 打印结果
        return new_json_data
    except KeyError:
        new_json_data = {
            "error": f"Invalid parameter {regulation}",
            "note": "此参数是刚发行或即将发行的吗？请切换请求参数重新尝试！！！"
        }
    return new_json_data

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5255, debug=True)