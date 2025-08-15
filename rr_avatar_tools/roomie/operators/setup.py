import bpy

from rr_avatar_tools import resources
from rr_avatar_tools.preferences import RRAvatarToolsPreferences
from rr_avatar_tools.roomie.operators.base import RecRoomRoomieOperator


class RR_OT_RoomieSetupSetupFile(bpy.types.Operator):
    """Setup file for roomie work"""

    bl_idname = "rr.roomie_setup_setup_file"
    bl_label = "Setup File"
    bl_options = {"REGISTER", "UNDO"}

    rr_require_source_art_path = True
    rr_required_mode = "OBJECT"

    suboperations = (
        bpy.ops.rr.setup_roomie_ensure_collections,
        bpy.ops.rr.setup_roomie_import_meshes,
    )

    @classmethod
    def poll(cls, context):
        if not context.scene.get("rec_room_roomie_setup"):
            return True

        return any([op.poll() for op in cls.suboperations])

    def execute(self, context):
        bpy.ops.rr.setup_ensure_objects_in_good_state()

        for operation in self.suboperations:
            if not operation.poll():
                continue

            operation()

        context.scene["rec_room_roomie_setup"] = True

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


class RR_OT_SetupRoomieImportMeshes(RecRoomRoomieOperator):
    """Imports modern bean body meshes"""

    bl_idname = "rr.setup_roomie_import_meshes"
    bl_label = "Import Roomie Meshes"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        collection = bpy.data.collections.get("RM1_Resources")
        if not collection:
            return True

        return False

    @classmethod
    def layer_collections(cls):
        def walk_view_layers(collection):
            return sum(
                [walk_view_layers(c) for c in collection.children], start=[collection]
            )

        return walk_view_layers(bpy.context.view_layer.layer_collection)

    @classmethod
    def get_view_layer(cls, name):
        matches = [c for c in cls.layer_collections() if c.name == name]
        return matches[0] if matches else None

    def execute(self, context):
        # Grab the RM1_Resources collection
        with bpy.data.libraries.load(
            resources.rm1_library, link=True, relative=True
        ) as (data_from, data_to):
            data_to.collections = [
                c for c in data_from.collections if c == "RM1_Resources"
            ]

        bpy.context.view_layer.active_layer_collection = self.get_view_layer("Roomie")

        bpy.ops.object.collection_instance_add(name="RM1_Resources")

        bpy.ops.object.select_all(action="DESELECT")

        # Find LayerCollection
        skin_meshes = bpy.data.objects["RM1_Resources"]
        skin_meshes.select_set(True)

        bpy.ops.object.make_override_library()

        bpy.ops.object.select_all(action="DESELECT")

        # Ensure armature modifers are correctly configured
        col = bpy.data.collections["RM1_Resources"]
        for obj in col.objects:
            for modifier in [m for m in obj.modifiers if m.type == "ARMATURE"]:
                modifier.object = bpy.data.objects.get("Roomie_Skeleton")

        # Link Roomie Skeleton into the Roomie collection
        col = bpy.data.collections["Roomie"]
        roomie_skeleton = bpy.data.objects["Roomie_Skeleton"]
        roomie_skeleton.select_set(True)
        index = bpy.data.collections[:].index(col)
        bpy.ops.object.link_to_collection(collection_index=index)

        return {"FINISHED"}


classes = (
    RR_OT_RoomieSetupSetupFile,
    RR_OT_SetupRoomieEnsureCollections,
    RR_OT_SetupRoomieImportMeshes,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
