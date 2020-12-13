import logging
import argparse
import os
import random

import fetch
import input
import db
from tqdm import tqdm
import yaml

import output
import resolver

logging.basicConfig(filename='/tmp/ncee-spider.log',
                    filemode='a',
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%m/%d/%Y %H:%M:%S %p",
                    level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Program to get NCEE score.',
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('mode', action="store", choices=[
                    'i', 'e', 's', 'f'], help='choose import or export', type=str)
parser.add_argument('-f', action="store", dest='src_file', type=str, required=False,
                    help='student info from excel file')
parser.add_argument('-o', action="store", dest='output_file', type=str, required=False,
                    help='output excel file')
parser.add_argument('-t', action="store", dest='output_content_type', type=int, required=False,
                    help='output content type. 0: 总分，1: 小分，2：录取. default: 0')
parser.add_argument('-s', action="store", dest='query_order', type=int, required=False,
                    help='order to query student. 0: 随机，1: 顺序，2：倒序. default: 0')
parser.add_argument('-c', action="store", dest='config_file', type=str, required=False,
                    help='config file path, default is ./configuration.yaml')


args = parser.parse_args()
print(args)

if args.config_file is None:
    config = yaml.safe_load(open((os.path.dirname(__file__) if '__file__' in globals() and len(
        os.path.dirname(__file__)) > 0 else '.') + '/configuration.yaml'))
else:
    config = yaml.safe_load(open(args.config_file))
print(config)

db.init()

if args.mode == 'i':  # import
    if not args.src_file:
        print("Student file was not specified, please use -f")
        exit(-1)
    students = input.read_student_excel(args.src_file)
    for stu in tqdm(students):
        db.insert_student(stu)
elif args.mode == 's':  # statics
    print("statics info:")
    cs = db.count_students()
    print("count of students：{}".format(cs))
    cbs = db.count_badinfo_students()
    print("count of bad info students：{}".format(cbs))
    cu = db.count_unfinished_students()
    print("count of unfinished students：{}".format(cu))
elif args.mode == 'f':  # fetch
    students = db.query_unfinished_students()
    if args.query_order == 1:
        pass
    elif args.query_order == 2:
        students = students[::-1]
    else:
        args.query_order = 0
        random.shuffle(students)
    for stu in tqdm(students, desc='fetch', position=0):
        for i in tqdm(range(1, config['spider']['max_retry'] + 1), desc='try', position=1, leave=False):
            stu_id, sfzh = stu['考生号'], stu['身份证号']
            while True:
                base64img = None
                while base64img is None:
                    base64img, cookie = fetch.get_captcha()
                oci, limited = fetch.baidu_oci(
                    config, fetch.captcha_to_img(base64img))
                if limited:  # oci request limited
                    logging.error(
                        'oci service request limit reached, we will exit!!!')
                    exit(-1)
                if oci is not None:
                    break
            # print([str(stu_id), str(sfzh[-4:]), oci, cookie])
            content = fetch.query_student(
                str(stu_id), str(sfzh[-4:]), oci, cookie)
            ok = resolver.is_result_ok(content)
            db.append_score_result(stu_id, content=content)
            if ok:
                logging.debug("fetch score successfully")
                db.insert_recognized_captcha(base64img, oci)
                break
            else:
                logging.debug("fetch score failed, msg is: {}".format(
                    resolver.get_error_msg(content)))


elif args.mode == 'e':  # export
    if not args.output_file:
        print("Output file was not specified, please use -o")
        exit(-1)
    if args.output_content_type is None:
        args.output_content_type = 0
    output.export_scores_to_excel(args.output_file, args.output_content_type)
