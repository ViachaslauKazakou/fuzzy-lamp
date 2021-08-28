import base64
import cgi
import io
import json
import logging
import os
import hashlib
import time

import boto3
import botocore
import re
from multidict import CIMultiDict
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import datetime
import logging

from providers import DbConnect
from settings import DB_STRING
from psql.models import Form
from multiprocessing import Pool


logger = logging.getLogger()
logger.setLevel(logging.INFO)

filedata = {
    "first_name": "name",
    "last_name": "lname",
    "origin_doc_link": "http://mysite.com",
    "description": "no description",
    "fields_config": {}
}


def timer(data):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = data(*args, **kwargs)
        finish = time.time()-start
        print(f"Execution time: {finish}")
        return result
    return wrapper


def add_data(filedata, session, record):
    for form in range(record):
        form = Form()
        form.first_name = filedata.get('first_name')
        form.last_name = filedata.get('last_name')
        form.origin_doc_link = filedata.get('origin_doc_link')
        form.description = filedata.get('description')
        form.fields_config = filedata.get('fields_config')
        session.add(form)


def save_form_to_db(record):
    try:
        engine = DbConnect(DB_STRING).init_app()
        Session = sessionmaker(bind=engine)
        session = Session()
        add_data(filedata, session, record)
        session.commit()
        session.close()

    except Exception as err:
        print(err)

@timer
def start(record):
    save_form_to_db(record)


def record_count():
    engine = DbConnect(DB_STRING).init_app()
    Session = sessionmaker(bind=engine)
    session = Session()
    rows = session.query(Form).count()
    session.close()
    return rows


@timer
def start_pool(num_proc, record):
    rec_pool = int(record/num_proc)
    print([rec_pool]*num_proc)
    with Pool(processes=num_proc) as proc:
        proc.map(save_form_to_db, [rec_pool]*num_proc)


if __name__ == '__main__':
    record = 25000
    proc = 5
    print(f"Records: {record_count()}, start populate with multi processes")
    start_pool(proc, record)
    print(f"added {record} records")
    print("-" * 120)
    print(f"Records: {record_count()}, start populate without processes")
    start(record)
    print("+" * 120)
    print(f"Records: {record_count()}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
