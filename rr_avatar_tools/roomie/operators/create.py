import uuid

import bpy

from bpy.props import (
    BoolProperty,
    EnumProperty,
    StringProperty,
)

from rr_avatar_tools.roomie.operators.base import (
    RecRoomRoomieOperator,
    RecRoomRoomieMeshOperator,
)

from rr_avatar_tools.utils import put_file_in_known_good_state


class RR_OT_CreateRoomieItem(RecRoomRoomieMeshOperator):
    """Set up selected meshes as a new item. Select all LODs for a single item before running this command"""

    bl_idname = "rr.create_roomie_item"
    bl_label = "Create Roomie Item"
    bl_options = {"REGISTER", "UNDO"}
    rr_required_mode = "OBJECT"

    foo: StringProperty(name="Foo", description="Foo")

    item_name: StringProperty(name="Item Name", description="")

    item_type: bpy.props.EnumProperty(
        name="Item Type",
        items=[
            ("HAT", "Hat", ""),
            ("EYE", "Eye", ""),
            ("WAIST", "Waist", ""),
            ("MOUTH", "Mouth", ""),
            ("BACK", "Back", ""),
            ("FACE", "Face", ""),
            ("WRIST", "Wrist", ""),
            ("TOPPER", "Topper", ""),
            ("EAR", "Ear", ""),
            ("HAIR", "Hair", ""),
            ("MASK", "Mask", ""),
            ("WINGS", "Wings", ""),
            ("NOSE", "Nose", ""),
        ],
        default="HAT",
    )

    transfer_weights: BoolProperty(
        name="Transfer Weights",
        description="Copy weights based on item type",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return super().poll(context)

    def setup(self):
        first = self.selected_meshes()[0]
        self.item_name = first.name

        try:
            parts = first.name.split("_")
            last = parts[-1]
            if last.upper().startswith("LOD"):
                last = parts[-2]
            self.item_type = last.upper()
        except:
            self.item_type = "HAT"

        self.ensure_name()

        # Don't default to transferring weights if meshes already have weights
        names = [
            vertex_group.name
            for mesh in self.selected_meshes()
            for vertex_group in mesh.vertex_groups
        ]
        self.transfer_weights = not any(map(lambda x: x.startswith("Jnt."), names))

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)

        # Initial values
        self.setup()

        self._execute(context)

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        return {"FINISHED"}

    def execute(self, context):
        return self._execute(context)

    def _execute(self, context):
        if self.item_name == "":
            self.setup()

        self.ensure_name()

        bpy.ops.rr.create_roomie_internal_item(
            item_name=self.item_name, transfer_weights=self.transfer_weights
        )

        return {"FINISHED"}

    def ensure_name(self):
        parts = []

        for part in self.item_name.rstrip(".R").rstrip(".L").split("_"):
            if part.upper() in ("LOD0", "LOD1", "LOD2"):
                continue

            parts.append(part)

        if parts[0].upper() not in ("RM1"):
            parts.insert(0, "RM1")
        else:
            parts[0] = "RM1"

        last = parts[-1].capitalize()

        if last in (
            "Hat",
            "Eye",
            "Waist",
            "Mouth",
            "Back",
            "Face",
            "Wrist",
            "Topper",
            "Ear",
            "Hair",
            "Mask",
            "Wings",
            "Nose",
        ):
            parts[-1] = self.item_type.title()
        else:
            parts.append(self.item_type.title())

        self.item_name = "_".join(parts)

        for mesh in self.selected_meshes():
            prefix = "RM1"

            if not mesh.name.startswith(prefix):
                i = 0
                if mesh.name[2] == "_":
                    i = 3

                mesh.name = f"{prefix}_{mesh.name[i:]}"

            # Ensure we have LOD part
            if not mesh.name.split("_")[-1].startswith("LOD"):
                mesh.name = f"{mesh.name}_LOD0"


class RR_OT_CreateRoomieInternalItem(RecRoomRoomieMeshOperator):
    """Setup file for avatar work"""

    bl_idname = "rr.create_roomie_internal_item"
    bl_label = "Create Roomie Item"
    bl_options = {"REGISTER", "UNDO"}

    item_name: StringProperty(name="Item Name", description="")

    transfer_weights: BoolProperty(
        name="Transfer Weights",
        description="Copy weights based on item type",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.collections.get("Roomie"))

    def execute(self, context):
        # Ensure avatar item collection
        dest = bpy.data.collections.get(self.item_name)
        if not dest:
            dest = bpy.data.collections.new(self.item_name)
            bpy.data.collections["Roomie"].children.link(dest)

        dest.color_tag = "COLOR_02"

        # Mark collection as an avatar item
        if not dest.get("rec_room_roomie_uuid"):
            dest["rec_room_roomie_uuid"] = str(uuid.uuid4())

        # Link in armature
        # TODO: Joshua link in roomie skeleton here
        rig = bpy.data.objects.get("Avatar_Skeleton")
        if not rig:
            self.report({"ERROR"}, "Missing Avatar_Skeleton armature")
            return {"CANCELLED"}

        if dest not in rig.users_collection:
            dest.objects.link(rig)

        for mesh in self.selected_meshes():
            # Remove mesh from all collections
            for collection in mesh.users_collection:
                collection.objects.unlink(mesh)

            dest.objects.link(mesh)

            modifers = [m for m in mesh.modifiers if m.type == "ARMATURE"]
            if len(modifers) > 1:
                for m in modifers:
                    mesh.modifiers.remove(m)
                modifers = []

            if len(modifers) == 0:
                m = mesh.modifiers.new(name="Armature", type="ARMATURE")
                modifers = [m]

            modifer = modifers[0]
            modifer.object = rig
            modifer.show_on_cage = True
            modifer.show_in_editmode = True

            # TODO: Joshua transfer weights from roomie body mesh
            # if self.transfer_weights:
            #     # Set body mesh to active selection
            #     body_mesh = bpy.data.objects.get("BodyMesh_LOD0")
            #     body_mesh.select_set(True)
            #     old_active = bpy.context.view_layer.objects.active
            #     bpy.context.view_layer.objects.active = body_mesh

            #     # Transfer weights
            #     bpy.ops.rr.weights_transfer_weights_from_active_mesh()

            #     # Clear body mesh active and selection
            #     bpy.context.view_layer.objects.active = old_active
            #     body_mesh.select_set(False)

        return {"FINISHED"}


classes = (
    RR_OT_CreateRoomieItem,
    RR_OT_CreateRoomieInternalItem,
)

panel = (RR_OT_CreateRoomieItem,)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
