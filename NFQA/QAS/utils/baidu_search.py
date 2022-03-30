import re
import requests
from bs4 import BeautifulSoup


def baidu_search(word: str) -> str:
    """
    百度百科检索问题
    :param word: 需要查询的问题
    :return: 百度百科查询结果
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"
    }

    url = f'https://baike.baidu.com/item/{word}'
    response = requests.get(url=url, headers=headers, timeout=10)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')

    li_list = soup.select('.lemma-summary')

    results = [re.sub(r'\[[0-9 \-]+]', '', i.text).strip() for i in li_list]
    result = ''.join(results)
    if len(result) > 100:
        result = result[:100] + "……"
    return result
