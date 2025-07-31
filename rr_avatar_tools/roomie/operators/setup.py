import bpy

from rr_avatar_tools.preferences import RRAvatarToolsPreferences


class RR_OT_RoomieSetupSetupFile(bpy.types.Operator):
    """Setup file for avatar work"""

    bl_idname = "rr.roomie_setup_setup_file"
    bl_label = "Setup File"
    bl_options = {"REGISTER", "UNDO"}

    rr_require_source_art_path = True
    rr_required_mode = "OBJECT"

    suboperations = (bpy.ops.rr.setup_roomie_ensure_collections,)

    @classmethod
    def poll(cls, context):
        if not context.scene.get("rec_room_setup"):
            return True

        return any([op.poll() for op in cls.suboperations])

    def execute(self, context):
        bpy.ops.rr.setup_ensure_objects_in_good_state()

        for operation in self.suboperations:
            if not operation.poll():
                continue

            operation()

        context.scene["rec_room_setup"] = True

        return {"FINISHED"}


class RR_OT_SetupRoomieEnsureCollections(bpy.types.Operator):
    """Create roomie collections"""

    bl_idname = "rr.setup_roomie_ensure_collections"
    bl_label = "Create Roomie Collections"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def preferences(self) -> RRAvatarToolsPreferences:
        return bpy.context.preferences.addons["rr_avatar_tools"].preferences

    @classmethod
    def poll(cls, context):
        if not bpy.data.collections.get("Roomie"):
            return True

        return False

    def find_or_create_collection(self, name):
        result = bpy.data.collections.get(name)

        if not result:
            result = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(result)

        return result

    def execute(self, context):
        self.find_or_create_collection("Roomie")

        return {"FINISHED"}


classes = (RR_OT_RoomieSetupSetupFile, RR_OT_SetupRoomieEnsureCollections)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
