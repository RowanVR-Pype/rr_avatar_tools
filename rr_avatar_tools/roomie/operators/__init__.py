from . import setup
from . import export
from . import create

packages = (setup, create, export)


classes = sum([p.classes for p in packages], ())


def register():
    for module in packages:
        module.register()


def unregister():
    for module in packages:
        module.unregister()
