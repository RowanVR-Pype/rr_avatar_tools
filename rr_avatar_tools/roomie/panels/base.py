import bpy


class RecRoomRoomiePanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rec Room Roomie Tools"

    @classmethod
    def poll(cls, context):
        # Ensure that the addon and file is correctly setup
        prefs = bpy.context.preferences.addons["rr_avatar_tools"].preferences
        if not prefs.enable_roomie_tools:
            return False

        return not bpy.ops.rr.roomie_setup_setup_file.poll()


class RecRoomRoomieOperatorPanel(RecRoomRoomiePanel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rec Room Roomie Tools"

    rr_operators = []

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)

        for operator in self.rr_operators:
            column.operator(
                operator.bl_idname, text=operator.rr_label or operator.bl_label
            )
