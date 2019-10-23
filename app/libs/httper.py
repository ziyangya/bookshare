"""
@File : http.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/18
"""

import requests


class HTTP:
    """
    使用requests发送HTTP请求
    """
    @staticmethod
    def get(url, return_json=True):
        # return_json控制返回结果是否需要转换为json格式
        # r是对HTTP请求结果的封装，包含很多信息
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
