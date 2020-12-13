import base64
import time
import requests
import logging
import lzstring
from aip import AipOcr

base_url = 'http://gkcf.jxedu.gov.cn/'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

lz = lzstring.LZString()


# {"Code":1,"Msg":"","Data":{"Txt":"","Img":"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAeAEADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3xY9sjvvY7sfKTwMelPqGWcpHOQjZiTcCw4bjPFc2ni6Q+F9Mvvsol1LUkxbW0fRpPx6KOpPYCtqdCdRXiutvz/yGk2dVUL3dtE5SS4iRh1VnAIrhtbuAnjnTLXU72+jjfTXknhsLi4VZJAwA2pG24/xdBnHXpXR6Lf6U+nXY0m6nnMBJlS6mmeWNsdGEp3qOOnA6+9a1MI4U4z1d1fbTe25HMan22A/cZpB6xIzj81BqWOVZV3KHAzj5kKn8iK5i31rXpdLg1AW+nSJLH5qwqzq5UDJGTkA4q0NK0TxEserTwF2mhRirSldoxkZAPX/CsZ0XDf0MlW5vgWvnpp+Ju/vPO/h8rb/wLP8AhT6xfDiWcNrLHZAJE7mVIxlti9BknucZwTnn2rXlV3jKxvsY9GxnH4VmzWDcopswfF+pXdjo8kNjGDd3WILc7hnexxwuDnAyx46A1zV5oKeGLzwpcz3bTGC6Ns0mSoVGVtqqmc4HOTkn13DgegT2sFyY2liRnibdE7IGMbYxuXI4PNRyadaTqguYEudj+YpnUPtb1GenTtiu2hjPYxUEtNb+d1b8DVStoYT+J7y01C+hu9FvpI1YfY5bO3edJkIyCXUcEntjj1NYU9hfxtdeIdQIstR1QxW8NmpVjboDgbj0kIGWPGR0zgV6GwJUgMVJHUdRVK3t7ecfvIvMe3kZUklbe4OMEgnlSfaohiYw+GNr2v8ALp82k3/loYTg5RaTOVfSTp2paZpMd3ey2NzvinSRgm8KvQbVDY98kdBmt8aaZj9jBVLJFVZPKIUOACvlgA7gAMZyT7Vea0tof37RB/JG6MMAfLwOSuehPenxwwSQsyoQs/zNyQTmsqlZzSv/AE+5EKCjft+nYkWMo6hGCwqm0RhQAP8AI7VJUIeK3eG3VSN+QuOgxzU1Ym5//9k="}}

def get_captcha():
    img = None
    url = base_url + 'captcha/getcode?t={}'.format(int(round(time.time() * 1000)))
    response = requests.get(url, headers=headers)
    logging.debug(">>> {}".format(response))
    js = response.json()
    cookie = response.cookies['_cap_id']
    if js['Code'] == 1:
        img = js['Data']['Img']
    return img, cookie


def query_student(key1, key2, key3, cookie):
    key1 = lz.compressToBase64(key1)
    key2 = lz.compressToBase64(key2)
    key3 = lz.compressToBase64(key3)
    payload = {"key1": key1,
               "key2": key2,
               "key3": key3}
    response = requests.post(base_url, headers=headers, data=payload, cookies={'_cap_id': cookie})
    logging.debug("<<< {}".format({"key1": key1,
                                   "key2": key2,
                                   "key3": key3,
                                   "cookie": cookie,
                                   }))
    content = response.content.decode()
    logging.debug(">>> {}".format(content))
    return content


def captcha_to_img(base64captcha):
    imgdata = base64.b64decode(base64captcha)
    return imgdata


def baidu_oci(config, img_content): # oci, limited
    client = AipOcr(config['baidu-ocr']['app_id'],
                    config['baidu-ocr']['api_key'],
                    config['baidu-ocr']['secret_key'])
    options = {"language_type": "ENG"}
    if bool(config['baidu-ocr']['accurate']):
        resp = client.basicAccurate(img_content, options)
    else:
        resp = client.basicGeneral(img_content, options)
    if 'error_code' in resp:
        logging.error('baidu_oci failed: {}'.format(resp))
        if resp['error_code'] in [4, 17, 19]:
            return None, True
        return None, False
    words = resp['words_result']
    for w in words:
        word = w['words']
        word = ''.join(list(filter(str.isalnum, word)))
        if len(word) == 4:
            return word, False
    logging.error('baidu_oci result is bad: {}'.format(resp))
    return None, False