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


def save_form_to_db(filedata, record):
    try:
        engine = DbConnect(DB_STRING).init_app()
        Session = sessionmaker(bind=engine)
        session = Session()
        # form = Form()
        # form.first_name = filedata.get('first_name')
        # form.last_name = filedata.get('last_name')
        # form.origin_doc_link = filedata.get('origin_doc_link')
        # form.description = filedata.get('description')
        # form.fields_config = filedata.get('fields_config')
        # session.add(form)
        add_data(filedata, session, record)
        session.commit()
        session.close()

    except Exception as err:
        print(err)


# @timer
def start(record):
    save_form_to_db(filedata,record)


def record_count():
    engine = DbConnect(DB_STRING).init_app()
    Session = sessionmaker(bind=engine)
    session = Session()
    rows = session.query(Form).count()
    session.close()
    return rows


if __name__ == '__main__':
    print(record_count())
    ts = time.time()
    with Pool(processes=5) as p:
        p.map(start, [5000,5000,5000,5000,5000])
    tf = time.time() - ts
    print("add 25000 records")
    print("-"* 120)
    print(f"Execution time with 5 process: {tf}")
    print("++++")
    print(record_count())
    ts = time.time()
    start(25000)
    tf = time.time() - ts
    print("-"* 120)
    print(f"Execution time without multiprocessing: {tf}")
    print("+"* 120)
    print(record_count())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
