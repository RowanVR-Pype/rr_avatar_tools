import bpy


class RR_OT_RoomieSetupSetupFile(bpy.types.Operator):
    """Setup file for avatar work"""

    bl_idname = "rr.roomie_setup_setup_file"
    bl_label = "Setup File"
    bl_options = {"REGISTER", "UNDO"}

    rr_require_source_art_path = True
    rr_required_mode = "OBJECT"

    suboperations = ()

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


classes = (RR_OT_RoomieSetupSetupFile,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
