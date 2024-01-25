import datetime
import re


def parse_date(date_string):
    # 数字と非数字の部分を分割
    parts = re.split(r'(\D+)', date_string)

    # 数字の部分と非数字（区切り文字）の部分を分離
    numbers = parts[::2]
    separators = parts[1::2]

    # フォーマット文字列を構築
    format_parts = ["%Y", "%m", "%d", "%H", "%M", "%S"]
    format_string = ""
    for num, sep in zip(format_parts, separators + [""]):
        format_string += num + sep

    # 日付を解析
    return datetime.datetime.strptime(date_string, format_string.strip())