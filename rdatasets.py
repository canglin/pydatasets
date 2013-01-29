import os
from pandas import read_csv, Int64Index


def read_doc(url):
    assert False


def set_dataset_modules():
    dsets = read_csv('datasets.csv').convert_objects()
    dsets.columns = map(lambda x: x.lower(), dsets.columns)
    packages = dsets.package
    datasets = dsets.item
    titles = dsets.title

    for (_, title), (_, package), (_, dataset) in zip(titles.iteritems(),
                                                      packages.iteritems(),
                                                      datasets.iteritems()):
        with open('__init__.py', 'a') as f:
            f.write("""
from .{package} import {dataset}
""".format(package=package.lower(), dataset=datasets.lower()))

        if not os.path.isdir(package):
            os.mkdir(package)

        with open(os.path.join(package, '__init__.py'), 'w') as f:
            f.write("""
'''
{doc}
'''
from .. import data
{dataset} = data('{package}', '{dataset}')
title = "{title}"
""".format(package=package, dataset=dataset.lower(), title=title,
           doc=doc.read()))



def data(package, dataset, ext='csv'):
    df = read_csv(os.path.join(os.pardir, package, dataset) + os.extsep + ext,
                  index_col=0).convert_objects()

    if isinstance(df.index, Int64Index):
        df.reset_index(drop=True, inplace=True)

    return df
