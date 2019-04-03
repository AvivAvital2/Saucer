# coding: utf8
from __future__ import unicode_literals
import warnings
import sys
import boto3
from concurrent.futures import ThreadPoolExecutor,as_completed

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# These are imported as part of the API
from thinc.neural.util import prefer_gpu, require_gpu

from .cli.info import info as cli_info
from .glossary import explain
from .about import __version__
from .errors import Errors, Warnings, deprecation_warning
from . import util
from os.path import join, dirname, realpath, basename
from sys import getsizeof
from io import BytesIO
from .aws_string_repo import aws_strings
from gc import collect


model = 'en_core_web_lg-2.1.0'

if sys.maxunicode == 65535:
    raise SystemError(Errors.E130)


def get_fileobj(bucket_name, location, s3_path):
    s3 = boto3.session.Session().resource('s3')
    aws_strings[location] = s3.Object(bucket_name, s3_path)
    return


def init_s3_connection(bucket_name, s3_prefix, model_name=model):
    global model
    if model_name is not model: model = model_name
    model_path = ''.join([s3_prefix, model_name])

    locations = {'lexemes': '/vocab/lexemes.bin',
                 'vectors': '/vocab/vectors',
                 'strings': '/vocab/strings.json',
                 'tagger': '/tagger/model'}

    with open('/tmp/s3_configuration', 'w') as f:
        for bucket in locations.keys():
            f.write('Bucket_{0} {1}\n'.format(bucket, bucket_name))
            f.write('Key_{0} {1}\n'.format(bucket, ''.join([model_path,locations[bucket]])))

    with ThreadPoolExecutor(max_workers=len(locations)) as executor:
        future_to_aws_string = {executor.submit(get_fileobj, bucket_name, location, ''.join([model_path, locations[location]])): location for location in locations}
        for future in as_completed(future_to_aws_string):
            future_to_aws_string[future]
            future.result()


def load(name=join(dirname(realpath(__file__)),model), **overrides):
    depr_path = overrides.get("path")
    if depr_path not in (True, False, None):
        deprecation_warning(Warnings.W001.format(path=depr_path))
    return util.load_model(name, **overrides)


def blank(name, **kwargs):
    LangClass = util.get_lang_class(name)
    return LangClass(**kwargs)


def info(model=None, markdown=False, silent=False):
    return cli_info(model, markdown, silent)
