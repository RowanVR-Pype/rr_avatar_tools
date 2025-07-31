from . import main
from . import export
from . import setup


modules = (
    main,
    export,
    setup,
)


classes = sum((main.classes, export.classes, setup.classes), ())


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()
