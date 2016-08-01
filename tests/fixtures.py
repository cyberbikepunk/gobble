"""Fixtures for test modules"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
from json import loads
from os import makedirs
from os.path import join, expanduser
from shutil import rmtree
from unittest.mock import patch

from future import standard_library
from pytest import fixture

from gobble.configuration import settings, GOBBLE_MODE
from gobble.configuration import ROOT_DIR

standard_library.install_aliases()


# Sanity check
# -----------------------------------------------------------------------------
class BadTestingConfiguration(Exception):
    pass


if GOBBLE_MODE not in ('Testing', 'Development'):
    sanity = (
        'Please run the tests in Testing or Development mode '
        'or bad things will happen and you will hate yourself'
    )
    raise BadTestingConfiguration(sanity)


# Fake the user's local set-up
# -----------------------------------------------------------------------------
@fixture
def tmp_user_dir(request):
    original = settings.USER_DIR
    settings.USER_DIR = join(expanduser('~'), '.gobble.tmp')
    try:
        makedirs(settings.USER_DIR)
    except IOError:
        pass

    def switch_back():
        settings.USER_DIR = original
        try:
            rmtree(settings.USER_DIR)
        except IOError:
            pass

    request.addfinalizer(switch_back)


# User authentication and permission
# -----------------------------------------------------------------------------
DUMMY_DIR = join(ROOT_DIR, 'assets', 'dummy')


@fixture
def token():
    filepath = join(DUMMY_DIR, 'token.json')
    with io.open(filepath) as file:
        return loads(file.read())


@fixture
def permissions():
    filepath = join('', 'permissions.json')
    with io.open(filepath) as file:
        return loads(file.read())


# Mock Gobble and site-package classes
# -----------------------------------------------------------------------------
@fixture
def mock_package():
    package = patch('datapackage.DataPackage', autospec=True)
    package.descriptor = {'name': 'mexican-budget-samples'}
    snapshot_file = join(SNAPSHOTS_DIR, 'POST.datastore.json')
    with io.open(snapshot_file) as file:
        package.description = loads(file.read())['request_json']
    return package


# noinspection PyShadowingNames
@fixture
def mock_user():
    return patch('gobble.user.User', autospec=True)


@fixture
def mock_batch():
    return patch('gobble.uploader.Batch', autospec=True)


@fixture
def mock_uploader():
    return patch('gobble.uploader.Uploder', autospec=True)
