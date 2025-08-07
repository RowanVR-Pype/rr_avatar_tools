import bpy

from rr_avatar_tools.roomie.panels.base import RecRoomRoomiePanel
from rr_avatar_tools.roomie import operators


class SCENE_PT_RRRoomieToolsSetupPanel(RecRoomRoomiePanel):
    bl_label = "Setup"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rec Room Roomie Tools"

    @classmethod
    def poll(cls, context):
        prefs = bpy.context.preferences.addons["rr_avatar_tools"].preferences
        if not prefs.enable_roomie_tools:
            return False

        return not super().poll(context)

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)
        column.scale_y = 2

        # Ensure file is correctly set up
        operator = operators.setup.RR_OT_RoomieSetupSetupFile

        column.operator(operator.bl_idname, text=operator.bl_label, icon="FILE_TICK")


classes = (SCENE_PT_RRRoomieToolsSetupPanel,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
