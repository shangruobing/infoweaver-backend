import jieba
import jieba.posseg as pseg
from datetime import date, timedelta
import calendar
import re

jieba.enable_paddle()


def get_jieba_date(string) -> str:
    words = pseg.cut(string, use_paddle=True)
    for dates, flag in words:
        if flag == 'TIME':
            return dates


def get_match_type(string) -> str:
    patterns = [r'天', r'周', r'月', r'年']

    for i in patterns:
        if re.search(i, string):
            return re.search(i, string).group()


def get_delta_date(delta):
    return (date.today() + timedelta(days=delta)).strftime("%Y-%m-%d")


def calculate_date_range(date_type, string):
    start_date = ''
    end_date = ''
    if date_type == '天':
        if string == "今天":
            start_date = date.today().strftime("%Y-%m-%d")
        if string == "昨天":
            start_date = get_delta_date(-1)
        if string == "明天":
            start_date = get_delta_date(1)

    elif date_type == '周':
        if string == "本周":
            start_date = get_delta_date(- date.today().weekday())
            end_date = get_delta_date(- date.today().weekday() + 6)

        if string == "上周":
            start_date = get_delta_date(- date.today().weekday() - 7)
            end_date = get_delta_date(- date.today().weekday() - 1)

        if string == "下周":
            start_date = get_delta_date(date.today().weekday() + 1)
            end_date = get_delta_date(date.today().weekday() + 7)

    elif date_type == '月':
        year = date.today().year
        month = date.today().month

        if string == "本月":
            _, days = calendar.monthrange(year, month)
            start_date = date(year, month, 1)
            end_date = date(year, month, days)

        if string == "上个月":
            _, days = calendar.monthrange(year, month - 1)
            start_date = date(year, month - 1, 1)
            end_date = date(year, month - 1, days)

        if string == "下个月":
            _, days = calendar.monthrange(year, month + 1)
            start_date = date(year, month + 1, 1)
            end_date = date(year, month + 1, days)

    elif date_type == '年':
        year = date.today().year
        if string == "今年":
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)

        if string == "去年":
            start_date = date(year - 1, 1, 1)
            end_date = date(year - 1, 12, 31)

        if string == "明年":
            start_date = date(year + 1, 1, 1)
            end_date = date(year + 1, 12, 31)

    return start_date, end_date


def str_date_range(string):
    string = get_jieba_date(string)
    date_type = get_match_type(string)
    start_date, end_date = calculate_date_range(date_type, string)
    print("start_date", start_date)
    print("end_date", end_date)
    return start_date, end_date
