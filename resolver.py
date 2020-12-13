import json
import re

OK = 0
BAD_CAPTCHA = 1
BAD_INFO = 2
UNKNOWN_ERROR = 3


def get_state_code(content):
    if is_result_ok(content):
        return OK
    msg = get_error_msg(content)
    if '验证码错误' in msg:
        return BAD_CAPTCHA
    if '输入信息有误' in msg:
        return BAD_INFO
    return UNKNOWN_ERROR


def is_result_ok(content):
    if 'var _score' in content:
        return True
    else:
        return False


def get_error_msg(content):
    m = re.search(r'var msg = "(.*)";', content)
    if m is not None and len(m.groups()) > 0:
        return m.groups()[0]
    return None


def parse_score(content):
    m = re.search(r"var _score = '(.*)'", content)
    if m is not None and len(m.groups()) > 0:
        return json.loads(m.groups()[0].lower().replace(' ', ''))
    return None


def parse_scores(content):
    m = re.search(r"var _scores = '(.*)'", content)
    if m is not None and len(m.groups()) > 0:
        return json.loads(m.groups()[0].replace(' ', ''))
    return None


def parse_luqu(content):
    m = re.search(r"var _luqu = '(.*)'", content)
    if m is not None and len(m.groups()) > 0:
        json_str = m.groups()[0].replace(' ', '')
        if json_str != '':
            return json.loads(m.groups()[0].replace(' ', ''))
    return None
