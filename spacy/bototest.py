import boto3
from concurrent.futures import ThreadPoolExecutor
from sys import getsizeof
from io import BytesIO
from os import getpid
import psutil
import tempfile


def task(bucket_name, key):
    s3 = boto3.session.Session().resource('s3')
    return s3.Object(bucket_name, key)


def main():
    process = psutil.Process(getpid())
    a = task(bucket_name='sparkbeyond-infrastructure',key='qa/spacy/en_core_web_lg-2.1.0/vocab/key2row')
    print(getsizeof(a))
    print(process.memory_info().rss)
    with tempfile.TemporaryFile() as buffer:
        a.download_fileobj(buffer)
        print(getsizeof(buffer))
        print(process.memory_info().rss)
        print(dir(buffer.read()))
    print(process.memory_info().rss)


if __name__ == '__main__':
    main()
