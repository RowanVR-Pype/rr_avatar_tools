import rr_avatar_tools


def all():
    import importlib as il

    # Reload package
    il.reload(rr_avatar_tools)

    il.reload(rr_avatar_tools.budgets)

    # Reload operators subpackage
    il.reload(rr_avatar_tools.operators)
    il.reload(rr_avatar_tools.operators.setup)

    il.reload(rr_avatar_tools.avatar.operators)
    il.reload(rr_avatar_tools.avatar.operators.base)
    il.reload(rr_avatar_tools.avatar.operators.bake)
    il.reload(rr_avatar_tools.avatar.operators.calisthenics)
    il.reload(rr_avatar_tools.avatar.operators.cleanup)
    il.reload(rr_avatar_tools.avatar.operators.create)
    il.reload(rr_avatar_tools.avatar.operators.diagnostics)
    il.reload(rr_avatar_tools.avatar.operators.export)
    il.reload(rr_avatar_tools.avatar.operators.mesh)
    il.reload(rr_avatar_tools.avatar.operators.setup)
    il.reload(rr_avatar_tools.avatar.operators.transfer)
    il.reload(rr_avatar_tools.avatar.operators.update)
    il.reload(rr_avatar_tools.avatar.operators.weights)

    il.reload(rr_avatar_tools.roomie.operators)
    il.reload(rr_avatar_tools.roomie.operators.base)
    il.reload(rr_avatar_tools.roomie.operators.create)
    il.reload(rr_avatar_tools.roomie.operators.diagnostics)
    il.reload(rr_avatar_tools.roomie.operators.export)
    il.reload(rr_avatar_tools.roomie.operators.setup)

    # Reload panels subpackage
    il.reload(rr_avatar_tools.avatar.panels)
    il.reload(rr_avatar_tools.avatar.panels.base)
    il.reload(rr_avatar_tools.avatar.panels.body)
    il.reload(rr_avatar_tools.avatar.panels.bounds)
    il.reload(rr_avatar_tools.avatar.panels.calisthenics)
    il.reload(rr_avatar_tools.avatar.panels.cleanup)
    il.reload(rr_avatar_tools.avatar.panels.create)
    il.reload(rr_avatar_tools.avatar.panels.diagnostics)
    il.reload(rr_avatar_tools.avatar.panels.everything)
    il.reload(rr_avatar_tools.avatar.panels.experimental)
    il.reload(rr_avatar_tools.avatar.panels.export)
    il.reload(rr_avatar_tools.avatar.panels.main)
    il.reload(rr_avatar_tools.avatar.panels.mask)
    il.reload(rr_avatar_tools.avatar.panels.outfits)
    il.reload(rr_avatar_tools.avatar.panels.setup)
    il.reload(rr_avatar_tools.avatar.panels.tools)
    il.reload(rr_avatar_tools.avatar.panels.transfer)
    il.reload(rr_avatar_tools.avatar.panels.update)

    il.reload(rr_avatar_tools.roomie.panels)
    il.reload(rr_avatar_tools.roomie.panels.base)
    il.reload(rr_avatar_tools.roomie.panels.create)
    il.reload(rr_avatar_tools.roomie.panels.diagnostics)
    il.reload(rr_avatar_tools.roomie.panels.everything)
    il.reload(rr_avatar_tools.roomie.panels.export)
    il.reload(rr_avatar_tools.roomie.panels.main)
    il.reload(rr_avatar_tools.roomie.panels.setup)

    il.reload(rr_avatar_tools.vendor)
    il.reload(rr_avatar_tools.vendor.rigui)

    # Reload handlers subpackage
    il.reload(rr_avatar_tools.handlers)

    # Reload preferences subpackage
    il.reload(rr_avatar_tools.preferences)

    # Reload properties subpackage
    il.reload(rr_avatar_tools.properties)

    il.reload(rr_avatar_tools.data)

    il.reload(rr_avatar_tools.bounds)

    il.reload(rr_avatar_tools.draw)

    il.reload(rr_avatar_tools.resources)

    il.reload(rr_avatar_tools.utils)

    print("rr_avatar_tools: Reload finished.")
