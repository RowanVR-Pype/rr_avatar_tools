import bpy

from rr_avatar_tools.roomie.panels.base import RecRoomRoomieOperatorPanel
from rr_avatar_tools.roomie import operators


class SCENE_PT_RRRoomieToolsCreatePanel(RecRoomRoomieOperatorPanel):
    bl_label = "Create"
    rr_operators = operators.create.panel

    def draw_header(self, context):
        self.layout.label(text="", icon="PLUS")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.scale_y = 1.3
        row.operator(
            "rr.create_roomie_item",
            text="Create Roomie Item",
            icon="COLLECTION_NEW",
        )


classes = (SCENE_PT_RRRoomieToolsCreatePanel,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
