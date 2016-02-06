import importlib

__author__ = 'simon'

import os
from os.path import dirname, basename, isfile
import glob
import pkgutil
import base

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

all_my_base_classes = {}
pkg_dir = os.path.dirname(__file__)

for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)

supported_drivers = {cls.__name__: cls for cls in base._AuctionSite.__subclasses__()}

for cls in base._AuctionSiteUsingGET.__subclasses__():
    supported_drivers[cls.__name__] = cls
