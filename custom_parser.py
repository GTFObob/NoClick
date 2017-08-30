from sumy.parsers.html import HtmlParser
from sumy.utils import _HTTP_HEADERS, fetch_url

from contextlib import closing

from custom_article import CustomArticle as Article

import requests, lxml.html

class CustomParser(HtmlParser):
    ''' Custom Parser that allows to omit certain keywords and tweak the original for our use'''

    @classmethod
    def from_url(cls, url, tokenizer):
        data = fetch_url(url)

        # form the lxml tree from the data
        html = lxml.html.fromstring(data)

        # find and store the title in the instance
        title = html.find(".//title").text
        return cls(data, tokenizer, url, title)

    def __init__(self, html_content, tokenizer, url, title):
        super(HtmlParser, self).__init__(tokenizer)
        self._article = Article(html_content, url)
        self._title = title
    
    def get_title(self):
        return self._title