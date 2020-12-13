from pymongo import MongoClient

import resolver


connect = None
nceedb = None

def init():
    global connect
    connect = MongoClient()
    global nceedb
    nceedb = connect['ncee_spider']


def insert_student(stu):
    stu = dict(stu)
    stu['_id'] = stu['考生号']
    nceedb['students'].replace_one({'_id': stu['_id']}, stu, upsert=True)


def count_students():
    return nceedb['students'].count_documents({})


def query_finished_student_ids():
    return list(
        map(lambda x: x['_id'], list(
            nceedb['scores'].find({'results': {'$elemMatch': {'state': {"$in": [resolver.OK, resolver.BAD_INFO]}}}},
                                  {'_id': 1}))))


def count_badinfo_students():
    return nceedb['scores'].count_documents({'results': {'$elemMatch': {'state': {"$in": [resolver.BAD_INFO]}}}})


def count_unfinished_students():
    u_ids = query_finished_student_ids()
    return nceedb['students'].count_documents({'_id': {"$nin": u_ids}})


def query_unfinished_students():
    u_ids = query_finished_student_ids()
    return list(nceedb['students'].find({'_id': {"$nin": u_ids}}))


def append_score_result(stuid, content):
    state = resolver.get_state_code(content)
    nceedb['scores'].update({'_id': stuid}, {'$push': {'results': {'state': state, 'content': content}}}, upsert=True)


def insert_recognized_captcha(base64img, ocr):
    nceedb['captcha'].insert_one({'img': base64img, 'txt': ocr})


def count_recognized_captchas():
    return nceedb['captcha'].count()


def query_recognized_captchas():
    return list(nceedb['captcha'].find())


def query_students_with_scores():
    return list(nceedb['students'].aggregate([
        {'$lookup': {
            'from': 'scores',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'scores'
        }},
        {'$unwind': '$scores'}
    ]))
