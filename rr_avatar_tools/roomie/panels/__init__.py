from . import main
from . import bounds
from . import create
from . import diagnostics
from . import everything
from . import export
from . import setup


modules = (
    main,
    create,
    export,
    diagnostics,
    bounds,
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
