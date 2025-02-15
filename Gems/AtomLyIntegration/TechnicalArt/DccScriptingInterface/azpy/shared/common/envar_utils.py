# coding:utf-8
#!/usr/bin/python
#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#
# -- This line is 75 characters -------------------------------------------
from __future__ import unicode_literals

# -------------------------------------------------------------------------
'''! A set of utility functions for enavrs

:file: < DCCsi >/azpy/shared/common/envar_utils.py
:Status: Prototype
:Version: 0.0.1
'''
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# built in's
import os
import sys
import logging as _logging

# 3rd Party
from box import Box
from unipath import Path
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
#  global space
from DccScriptingInterface.azpy.shared import _PACKAGENAME
_PACKAGENAME = f'{_PACKAGENAME}.envar_utils'
_LOGGER = _logging.getLogger(_PACKAGENAME)
_LOGGER.debug('Initializing: {0}.'.format({_PACKAGENAME}))

from DccScriptingInterface.globals import *
# -------------------------------------------------------------------------


# -- envar util ----------------------------------------------------------
def get_envar_default(envar, envar_default=None, envar_set=Box(ordered_box=True)):
    '''
    Check the environment variable (envar)
    Get from the system environment, or the module dictionary (a Box):
    like the test one in __main__ below,
        TEST_ENV_VALUES = Box(ordered_box=True)
        TEST_ENV_VALUES[ENVAR_O3DE_PROJECT] = '${0}'.format(ENVAR_O3DE_PROJECT)

    This dictionary provides a simple way to pack a default set into a
    structure and decouple the getter implementation.

    These envars resolve to specific values at import time.

    Envars set in the environment trump the default values.

    :param var:
    :return: Some value for the variable, current or default.
    '''

    from pathlib import Path

    envar = str(envar)
    value = os.getenv(envar, envar_default)
    if not value:
        value = envar_set.get(envar)
    if value is not None:
        value = Path(os.path.expandvars(value)).as_posix()
    return value
# -------------------------------------------------------------------------


# -- envar util ----------------------------------------------------------
def set_envar_defaults(envar_set, env_root=get_envar_default(ENVAR_O3DE_DEV)):
    """
    Set each environment variable if not alreay set with value.
    Must be safe, will not over-write existing.
    :return: envarSet
    """

    from pathlib import Path

    if env_root:
        env_root = Path(env_root)

    if env_root.exists():
        os.environ[ENVAR_O3DE_DEV] = env_root.as_posix()
        envar_set[ENVAR_O3DE_DEV] = env_root.as_posix()
    else:
        raise ValueError("EnvVar Root is not valid: {0}".format(env_root))

    for envar in iter(envar_set.keys()):
        envar = str(envar)
        value = os.getenv(envar)

        if DCCSI_GDEBUG:
            if not value:
                _LOGGER.debug('~ EnVar value NOT found: {0}\r'.format(envar))

        if not value:
            value = envar_set.get(envar)

        elif value:
            if Path(os.path.expandvars(value)).exists():
                value = Path(os.path.expandvars(value))
                envar_set[envar] = value.as_posix()
                os.environ[envar] = value.as_posix()

            elif value:
                envar_set[envar] = value

    return envar_set
# -------------------------------------------------------------------------


# -- envar util class ----------------------------------------------------
class Validate_Envar(object):
    '''Simple Class to resolve environment references at runtime
    after the project_root has been defined'''

    def __init__(self, envar=''):
        self._envar = envar
        self._envar_value = None

    @property
    def envar(self):
        return self._envar

    @envar.setter
    def envar(self, envar):
        self._envar = envar
        self._envar_value = get_envar_default(self._envar)
        return self._envar

    @envar.getter
    def envar(self):
        return self._envar

    @property
    def envar_value(self):
        return get_envar_default(self._envar_value)

    @envar_value.getter
    def envar_value(self):
        self._envar_value = get_envar_default(self._envar)
        return self._envar_value

    def __str__(self):
        return str('{0}'.format(self.envar_value))

    def __repr__(self):
        return "Validate_Envar(envar='{0}')".format(self.envar)
# -------------------------------------------------------------------------


###########################################################################
# Main Code Block, runs this script as main (testing)
# -------------------------------------------------------------------------
if __name__ == '__main__':
    # imports for local testing
    import json

    # srun simple tests?
    test = True

    # happy print
    _LOGGER.info("# {0} #".format('-' * 72))
    _LOGGER.info('~ config_utils.py ... Running script as __main__')
    _LOGGER.info("# {0} #\r".format('-' * 72))

    # set up base totally non-functional defauls (denoted with $<ENVAR>)
    TEST_ENV_VALUES = Box(ordered_box=True)

    # ^^ that results in "~ EnVar value NOT found: ordered_box"
    # which is a little bit odd, I assume the Box object stores that
    # it should be benign but leaving this comment here in case of funk

    # tes envars
    TEST_ENV_VALUES[ENVAR_O3DE_PROJECT] = '${0}'.format(ENVAR_O3DE_PROJECT)
    TEST_ENV_VALUES[ENVAR_O3DE_DEV] = Path('${0}'.format(ENVAR_O3DE_DEV))

    #  try to fetch and set the base values from the environment
    #  this makes sure all envars set, are resolved on import
    TEST_ENV_VALUES = set_envar_defaults(TEST_ENV_VALUES)

    _LOGGER.info('Pretty print: TEST_ENV_VALUES')
    print(json.dumps(TEST_ENV_VALUES,
                     indent=4, sort_keys=False,
                     ensure_ascii=False), '\r')

    # simple tests
    _ENV_TAG = 'O3DE_DEV'
    foo = get_envar_default(_ENV_TAG)
    _LOGGER.info("~ Results of getVar on tag, '{0}':'{1}'\r".format(_ENV_TAG, foo))

    envar_value = Validate_Envar(envar=_ENV_TAG)
    _LOGGER.info('~ Repr is: {0}\r'.format(str(repr(envar_value))))
    _LOGGER.info("~ Results of ValidEnvars(envar='{0}')=='{1}'\r".format(_ENV_TAG, envar_value))

    # custom prompt
    sys.ps1 = "[azpy]>>"

