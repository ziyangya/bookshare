"""
@File : trade.py
@Author: Zyeoh
@Desc :
@Date : 2019/10/10
"""
from view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        # 将trades_gifts和trade_wishes原始数据转为我们要的view_models的实际的数据
        self.trades = []
        self.__parse(goods)

    # 执行具体的数据转换
    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    # 将原始数据转换为页面显示的数据
    def __map_to_trade(self, single):
        if single.create_datetime:
            # python的时间类型才strftime方法，需要将create_time转换为时间类型
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


class MyTrades:

    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []
        # 会当做参数传入到很多函数，这样定义简单方便
        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list
        self.trades = self.__parse()

    # 解析过程
    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    # 避免多层嵌套
    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'trades_count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id
        }
        return r