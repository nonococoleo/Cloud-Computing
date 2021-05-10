import logging
import hashlib
import boto3
import time

import config


def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    FORMAT = '%(levelname)7s [%(asctime)s - %(filename)20s:%(lineno)3s] - %(message)s'
    logging.basicConfig(format=FORMAT)
    logger.setLevel(level)
    return logger


def get_md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()


def count_people(data):
    female, male = 0, 0
    neg, mild, pos = 0, 0, 0
    for i in data:
        if i["Gender"] == "Male":
            male += 1
        elif i["Gender"] == "Female":
            female += 1

        if i["Emotions"] == "Positive":
            pos += 1
        elif i["Emotions"] == "Mild":
            mild += 1
        elif i["Emotions"] == "Negitive":
            neg += 1
    return {"visitor": str(male + female), "male": str(male), "female": str(female), "emo_neg": str(neg),
            "emo_pos": str(pos), "emo_mild": str(mild)}


def upload_image(owner, file, bucket):
    s3 = get_boto_client('s3')
    bucket = bucket
    obj_name = f'{owner}-{time.time()}.jpg'
    s3.upload_file(file, bucket, obj_name)
    return obj_name


def get_boto_client(type, region=None):
    cred = config.aws
    return boto3.client(type, aws_access_key_id=cred["access_key_id"], aws_secret_access_key=cred["secret_access_key"],
                        region_name=region)
