from . import operators
from . import panels


packages = (
    operators,
    panels,
)


classes = sum([p.classes for p in packages], ())


def register():
    for package in packages:
        package.register()


def unregister():
    for package in packages:
        package.unregister()
