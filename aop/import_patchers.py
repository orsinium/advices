# built-in
import sys
from os import getcwd
from types import ModuleType
from _frozen_importlib_external import PathFinder

# project
from .hooks import AspectFinder
from .module import AspectModule, unwrap_module, wrap_module
from .patchers import patch_object


CWD = getcwd()


def patch_cache():
    """Patch modules in cache
    """
    for module_name, module in sys.modules.copy().items():
        sys.modules[module_name] = wrap_module(module)


def unpatch_cache():
    for module_name, module in sys.modules.items():
        sys.modules[module_name] = unwrap_module(module)


def patch_import():
    """Patch modules finder
    """
    if AspectFinder in sys.meta_path:
        return
    index = sys.meta_path.index(PathFinder)
    sys.meta_path[index] = AspectFinder


def unpatch_import():
    if AspectFinder not in sys.meta_path:
        return
    index = sys.meta_path.index(AspectFinder)
    sys.meta_path[index] = PathFinder


def patch_project(path=CWD):
    """Patch already imported modules in project modules
    """
    module = sys.modules['__main__']
    for obj_name in dir(module):
        if obj_name[:2] == '__':
            continue
        obj = getattr(module, obj_name)
        if isinstance(obj, ModuleType):
            if not isinstance(obj, AspectModule):
                setattr(module, obj_name, wrap_module(obj))
        else:
            setattr(module, obj_name, patch_object(obj))
