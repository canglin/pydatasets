import os
import re
import urllib2
import contextlib

import numpy as np

from pandas import read_csv, Int64Index


# def read_doc(url):
#     assert False


# def set_dataset_modules():
#     dsets = read_csv('datasets.csv').convert_objects()
#     dsets.columns = map(lambda x: x.lower(), dsets.columns)
#     packages = dsets.package
#     datasets = dsets.item
#     titles = dsets.title

#     for (_, title), (_, package), (_, dataset) in zip(titles.iteritems(),
#                                                       packages.iteritems(),
#                                                       datasets.iteritems()):
#         with open('__init__.py', 'a') as f:
#             f.write("""
# from .{package} import {dataset}
# """.format(package=package.lower(), dataset=datasets.lower()))

#         if not os.path.isdir(package):
#             os.mkdir(package)

#         with open(os.path.join(package, '__init__.py'), 'w') as f:
#             f.write("""
# '''
# {doc}
# '''
# from .. import data
# {dataset} = data('{package}', '{dataset}')
# title = "{title}"
# """.format(package=package, dataset=dataset.lower(), title=title,
#            doc=doc.read()))


def clean_columns(df, lower=True):
    rx = re.compile(r'\.')
    und = lambda x: rx.sub('_', x)

    transform = und

    if lower:
        und_and_lower = lambda x: und(x).lower()
        transform = und_and_lower

    df.columns = map(transform, df.columns)


_datasets = read_csv('datasets.csv').convert_objects()
clean_columns(_datasets)
datasets = _datasets
_paths = ('datasets' + os.sep + datasets.package + os.sep + datasets.item +
          os.extsep + 'csv')
datasets['file_size'] = _paths.map(os.path.getsize)


def doc(package, dataset):
    ds = datasets
    pkg = ds.package == package
    dset = ds.item == dataset
    doc_url = ds[pkg & dset].doc.item()

    with contextlib.closing(urllib2.urlopen(doc_url)) as f:
        doc_content = f.read()

    return doc_content


def data(package, dataset, ext='csv'):
    path = os.path.join(os.curdir, 'datasets', package,
                        dataset) + os.extsep + ext
    df = read_csv(path, index_col=0).convert_objects()

    if isinstance(df.index, Int64Index):
        if np.array_equal(df.index.values, np.arange(1, max(df.shape) + 1)):
            df.reset_index(drop=True, inplace=True)

    clean_columns(df)
    return df
