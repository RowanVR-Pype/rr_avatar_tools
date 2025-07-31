from . import main
from . import create
from . import everything
from . import export
from . import setup


modules = (
    main,
    create,
    export,
    setup,
    everything,
)


classes = sum([m.classes for m in modules], ())


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()
