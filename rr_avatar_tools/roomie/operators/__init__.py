from . import setup

modules = (setup,)


classes = sum([p.classes for p in modules], ())


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()
