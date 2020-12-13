import db
import resolver
import pandas as pd

XIAOFENG_MAP = {
    "ptyw":
        {
            "k": "第1-5题，第7题，第10-12题，第14题，第17-19题",
            "z1": "第6题",
            "z2": "第8题",
            "z3": "第9题",
            "z4": "第13题",
            "z5": "第15题",
            "z6": "第16题",
            "z7": "第20题",
            "z8": "第21题",
            "z9": "第22题"
        },
    "ptls":
        {
            "k": "第1-12题",
            "z1": "填空题（13-16）",
            "z2": "第17题",
            "z3": "第18题",
            "z4": "第19题",
            "z5": "第20题",
            "z6": "第21题",
            "z7": "选考题（22-23）"
        },
    "ptws":
        {
            "k": "第1-12题",
            "z1": "填空题（13-16）",
            "z2": "第17题",
            "z3": "第18题",
            "z4": "第19题",
            "z5": "第20题",
            "z6": "第21题",
            "z7": "选考题（22-23）"
        },
    "ptwy": {"k": "第1-60题", "z1": "语法填空（61-70）", "z2": "短文改错", "z3": "书面表达"},
    "ptlz":
        {
            "k": "第1-21题",
            "z1": "第22题",
            "z2": "第23题",
            "z3": "第24题",
            "z4": "第25题",
            "z5": "第26题",
            "z6": "第27题",
            "z7": "第28题",
            "z8": "第29题",
            "z9": "第30题",
            "z10": "第31题",
            "z11": "第32题",
            "z12": "物理选考题（33-34）",
            "z13": "化学选考题（35-36）",
            "z14": "生物选考题（37-38）"
        },
    "ptwz":
        {
            "k": "第1-35题",
            "z1": "第36题",
            "z2": "第37题",
            "z3": "第38题",
            "z4": "第39题",
            "z5": "第40题",
            "z6": "第41题",
            "z7": "第42题",
            "z8": "地理选考题（43-44）",
            "z9": "历史选考题（45-47）"
        },
    # "sxyw":
    #     {
    #         "k": "第1-15题",
    #         "z1": "第16题",
    #         "z2": "第17-20题",
    #         "z3": "第21-23题",
    #         "z4": "第24题",
    #         "z5": "第25题"
    #     },
    # "sxsx": {
    #     "k": "第1-18题",
    #     "z1": "填空题（19-24）",
    #     "z2": "第25题",
    #     "z3": "第26题",
    #     "z4": "第27题",
    #     "z5": "第28题",
    #     "z6": "第29题",
    #     "z7": "第30题"
    # },
    # "sxwy": {"k": "第1-80题", "z1": "书面表达"},
    # "sxjsj":
    #     {"k": "第1-45题", "z1": "填空题（46-60）", "z2": "第61题", "z3": "第62题", "z4": "第63题", "z5": "第64题", "z6": "第65题"},
    "ptjs": {
        "k": "信息技术第1-20题，选考题（26-35）；通用技术第1-15题",
        "z1": "信息技术填空题（21-25）",
        "z2": "信息技术选考题（36）",
        "z3": "通用技术填空题（16-17）",
        "z4": "通用技术第18题",
        "z5": "通用技术第19题"
    }
}

KM_NAME_MAP = {
    "ptyw": '普通语文',
    "ptls": '普通理数',
    "ptws": '普通文数',
    "ptwy": '普通外语',
    "ptlz": '普通理综',
    "ptwz": '普通文综',
    "sxyw": '普通理数',
    # "sxsx": '',
    # "sxwy": '',
    # "sxjsj": '',
    "ptjs": '普通技术',
}


def gen_base_info(stu):
    d = {}
    d['班级'] = stu['班级']
    d['考生号'] = str(stu['考生号'])

    d['身份证号（后四位）'] = str(stu['身份证号'])[-4:]
    d['姓名'] = stu['姓名']
    msg = ''
    scores = stu['scores']
    roks = list(filter(lambda r: r['state'] == resolver.OK, scores['results']))
    content = None
    # 取得content
    if len(roks) > 0:
        r = roks[-1]
        content = r['content']
    else:
        if len(list(filter(lambda r: r['state'] == resolver.BAD_INFO, scores['results']))) > 0:
            msg = '信息有误'
        else:
            r = list(filter(lambda r: r['state'] not in [resolver.OK, resolver.BAD_INFO], scores['results']))[0]
            msg = resolver.get_error_msg(r['content'])
    return d, content, msg


def export_scores_to_excel(result_path, type=0):
    students = db.query_students_with_scores()
    if type == 0:
        data = []
        for stu in students:
            d, content, msg = gen_base_info(stu)
            d['注释'] = msg
            if content is not None:
                s = resolver.parse_score(content)
                if s is None:
                    d['注释'] = '解析出错'
                else:
                    d['语文成绩'] = s['yw']
                    d['数学成绩'] = s['sx']
                    d['外语成绩'] = s['wy']
                    d['综合成绩'] = s['zh']
                    d['技术成绩'] = s['js']
                    d['本科总分(含加分)'] = s['bkpmf']
                    d['本科分平行排名'] = int(s['bkpm'])
                    d['高职(专科)总分(含加分)'] = s['zkpmf']
                    d['高职(专科)分平行排名'] = s['zkpm']
                    d['体育本科平行排名'] = s['ty2bpm']
                    d['体育高职(专科)平行排名'] = s['tyzkpm']
            data.append(d)
        df = pd.DataFrame(data)
        df.to_excel(result_path)
    elif type == 1:  # 小分
        data = {}
        for k in XIAOFENG_MAP.keys():
            data[k] = []
        for stu in students:
            d, content, msg = gen_base_info(stu)
            ss = None
            if content is not None:
                ss = resolver.parse_scores(content)
            for k in XIAOFENG_MAP.keys():
                dk = d.copy()
                dk['注释'] = msg
                if content is not None:
                    if ss is None:
                        dk['注释'] = '解析出错'
                    else:
                        km = list(filter(lambda s: s['kmCode'] == k, ss))
                        km = km[0] if len(km) > 0 else None
                        if km is not None:
                            kmt = XIAOFENG_MAP[k]
                            for kmtk in kmt.keys():
                                dk[kmt[kmtk]] = km[kmtk]
                            dk['总分'] = km['zf']
                        else:
                            dk['注释'] = '无该科成绩'
                data[k].append(dk)
        with pd.ExcelWriter(result_path) as writer:
            for k in XIAOFENG_MAP.keys():
                df = pd.DataFrame(data[k])
                df.to_excel(writer, sheet_name=KM_NAME_MAP[k])
    elif type == 2:  # 录取
        data = []
        for stu in students:
            d, content, msg = gen_base_info(stu)
            d['注释'] = msg
            if content is not None:
                s = resolver.parse_luqu(content)
                if s is None:
                    d['注释'] = '无录取信息'
                else:
                    d['录取状态'] = s['lqzt']
                    d['院校代号'] = s['yxdh']
                    d['录取院校'] = s['yxmc']
                    d['录取批次'] = s['pcmc']
                    d['录取专业'] = s['zymc']
                    d['科类名称'] = s['klmc']
                    d['录取时间'] = s['lqsj']
            data.append(d)
        df = pd.DataFrame(data)
        df.to_excel(result_path)
