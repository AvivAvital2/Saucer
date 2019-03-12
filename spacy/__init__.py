# coding: utf8
from __future__ import unicode_literals
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# These are imported as part of the API
from thinc.neural.util import prefer_gpu, require_gpu

from .cli.info import info as cli_info
from .glossary import explain
from .about import __version__
from .errors import Warnings, deprecation_warning
from . import util
from os.path import join, dirname, realpath

model = 'en_core_web_lg-2.0.0'

def init_s3_connection(bucket_name, s3_prefix, model_name=model):

    model_path = ''.join([s3_prefix, model_name])

    buckets = ['lexemes', 'vectors', 'keys', 'strings']

    keys = ['/vocab/lexemes.bin',
            '/vocab/vectors',
            '/vocab/keys',
            '/vocab/strings.json']

    with open('/tmp/s3_configuration','w') as f:
        zipper = zip(buckets,[''.join([model_path,key]) for key in keys])
        for bucket in buckets:
            f.write('Bucket_{0} {1}\n'.format(bucket, bucket_name))
            f.write('Key_{0}\n'.format(' '.join(zipper.pop(0))))


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
