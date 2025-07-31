from . import main


modules = (main,)


classes = sum((main.classes,), ())


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()
