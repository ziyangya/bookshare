"""
@File : gift.py
@Author: Zyeoh
@Desc :
@Date : 2019/10/13
"""
from .book import BookViewModel
from collections import namedtuple

# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])


# 集合对象,图书详情+ 想要人数
class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        # 会当做参数传入到很多函数，这样定义简单方便
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list

        self.gifts = self.__parse()

    # 解析过程
    def __parse(self):
        # 不要修改实例属性，用临时列表来接收
        temp_gifts = []
        # 对于当前gift有多少人想要,想要的数量是记录在wish_count_list，它包含了很多个gift对应的量
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    # 避免多层嵌套
    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id
        }
        return r
        #         gift模型拿到的也是原始数据
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift
