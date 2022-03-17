from datetime import date, timedelta
import re
import calendar
import jieba
import jieba.posseg as pseg

jieba.enable_paddle()


def get_jieba_date(string) -> str:
    words = pseg.cut(string, use_paddle=True)
    for word, flag in words:
        if flag == 'TIME':
            return word


def get_match_type(string) -> str:
    patterns = [r'天', r'周', r'月', r'年']

    for i in patterns:
        if re.search(i, string):
            return re.search(i, string).group()


date_format = "%Y%m%d"


def get_delta_date(delta):
    return (date.today() + timedelta(days=delta)).strftime(date_format)


def execute_str2date(date_type, string):
    start_date = ''
    end_date = ''
    if date_type == '天':
        if string == "今天":
            start_date = date.today().strftime(date_format)
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
            start_date = get_delta_date(-date.today().weekday() + 7)
            end_date = get_delta_date(-date.today().weekday() + 13)

    elif date_type == '月':
        year = date.today().year
        month = date.today().month

        if string == "本月":
            _, days = calendar.monthrange(year, month)
            start_date = date(year, month, 1).strftime(date_format)
            end_date = date(year, month, days).strftime(date_format)

        if string == "上个月":
            _, days = calendar.monthrange(year, month - 1)
            start_date = date(year, month - 1, 1).strftime(date_format)
            end_date = date(year, month - 1, days).strftime(date_format)

        if string == "下个月":
            _, days = calendar.monthrange(year, month + 1)
            start_date = date(year, month + 1, 1).strftime(date_format)
            end_date = date(year, month + 1, days).strftime(date_format)

    elif date_type == '年':
        year = date.today().year
        if string == "今年":
            start_date = date(year, 1, 1).strftime(date_format)
            end_date = date(year, 12, 31).strftime(date_format)

        if string == "去年":
            start_date = date(year - 1, 1, 1).strftime(date_format)
            end_date = date(year - 1, 12, 31).strftime(date_format)

        if string == "明年":
            start_date = date(year + 1, 1, 1).strftime(date_format)
            end_date = date(year + 1, 12, 31).strftime(date_format)

    return start_date, end_date


def str_date_range(string):
    string = get_jieba_date(string)
    date_type = get_match_type(string)
    start_date, end_date = execute_str2date(date_type, string)
    return start_date, end_date

# questions = ["去年有什么通知", "今年有什么通知", "明年有什么通知",
#              "上个月有什么通知", "本月有什么通知", "下个月有什么通知",
#              "上周有什么通知", "本周有什么通知", "下周有什么通知",
#              "昨天有什么通知", "今天有什么通知",  "明天有什么通知"]
# for i in questions:
#     start_date, end_date = str_date_range(i)
#     # print(i)
#     print("start_date", start_date)
#     print("end_date", end_date)
#     print()
