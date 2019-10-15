"""
@File : book.py
@Author: Zyeoh
@Desc :
@Date : 2019/9/21
"""


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.pages = book['pages']
        self.pubdate = book['pubdate']
        self.binding = book['binding']
        self.isbn = book['isbn']

    @property
    def intro(self):
        # 过滤器，通过自定义规则（lambda函数），让传入数据的每一项进行筛选返回False过滤，返回True保留，
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]
