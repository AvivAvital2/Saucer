# coding: utf8
from __future__ import unicode_literals
import warnings
import boto3
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# These are imported as part of the API
from thinc.neural.util import prefer_gpu, require_gpu

from .cli.info import info as cli_info
from .glossary import explain
from .about import __version__
from .errors import Warnings, deprecation_warning
from . import util
from os.path import join, dirname, realpath, basename
from sys import getsizeof
from cStringIO import StringIO as c_StringIO

model = 'en_core_web_lg-2.0.0'


def init_s3_connection(bucket_name, s3_prefix, model_name=model):
    model_path = ''.join([s3_prefix, model_name])
    locations = {'lexemes': '/vocab/lexemes.bin',
                    'vectors': '/vocab/vectors',
                    'keys': '/vocab/keys',
                    'strings': '/vocab/strings.json',
                    'tagger': '/tagger/model'}

    with open('/tmp/s3_configuration', 'w') as f:
        for bucket in locations.keys():
            f.write('Bucket_{0} {1}\n'.format(bucket, bucket_name))
            f.write('Key_{0} {1}\n'.format(bucket, ''.join([model_path,locations[bucket]])))


def load(name=join(dirname(realpath(__file__)),model), **overrides):
    depr_path = overrides.get('path')
    if depr_path not in (True, False, None):
        deprecation_warning(Warnings.W001.format(path=depr_path))
    return util.load_model(name, **overrides)


def blank(name, **kwargs):
    LangClass = util.get_lang_class(name)
    return LangClass(**kwargs)


def info(model=None, markdown=False, silent=False):
    return cli_info(model, markdown, silent)
