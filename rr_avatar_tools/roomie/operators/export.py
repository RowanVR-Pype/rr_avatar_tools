import os
from typing import Set

import bpy

import rr_avatar_tools
import rr_avatar_tools.data
from rr_avatar_tools.roomie.operators.base import RecRoomRoomieOperator
from rr_avatar_tools.utils import put_file_in_known_good_state


class RR_OT_ExportGenericRoomieItems(RecRoomRoomieOperator):
    """Setup file for roomie work"""

    bl_idname = "rr.export_generic_roomie_items"
    bl_label = "Export Roomie Items"
    bl_options = {"REGISTER", "UNDO"}

    rr_require_source_art_path = False
    rr_require_source_art_path = False
    rr_required_mode = "OBJECT"

    @classmethod
    def poll(cls, context):
        prefs = bpy.context.preferences.addons["rr_avatar_tools"].preferences

        any_item_selected = bpy.ops.rr.export_roomie_items.poll()
        export_path_set = bool(prefs.generic_export_path)

        return any_item_selected and export_path_set

    def execute(self, context):
        return self.execute_(context)

    @put_file_in_known_good_state
    def execute_(self, context):
        if bpy.ops.rr.export_roomie_items.poll():
            bpy.ops.rr.export_roomie_items()

        count = len(
            [
                p
                for p in bpy.context.scene.roomie_export_list
                if p.select and p.can_export()
            ]
        )

        self.report({"INFO"}, f"Exported {count} item(s)")

        return {"FINISHED"}


class RR_OT_ExportRoomieItems(RecRoomRoomieOperator):
    """Export selected"""

    bl_idname = "rr.export_roomie_items"
    bl_label = "Export Roomie Items"
    bl_options = {"REGISTER", "UNDO"}

    rr_require_rec_room_path = False
    rr_required_mode = "OBJECT"

    @classmethod
    def poll(cls, context):
        return any(g.select for g in cls.export_groups())

    @classmethod
    def export_groups(cls):
        collections = [c.get("rec_room_roomie_uuid") for c in cls.export_collections()]
        return [
            i
            for i in bpy.context.scene.roomie_export_list
            if i.can_export() and i.uuid in collections
        ] or []

    @classmethod
    def export_collections(cls):
        return [
            c for c in rr_avatar_tools.data.roomie_items if c.name.startswith("RM1_")
        ]

    def layer_collections(self):
        def walk_view_layers(collection):
            return sum(
                [walk_view_layers(c) for c in collection.children], start=[collection]
            )

        return walk_view_layers(bpy.context.view_layer.layer_collection)

    def set_active_collection(self, collection):
        collections = [
            c for c in self.layer_collections() if c.collection == collection
        ]

        if collections:
            bpy.context.view_layer.active_layer_collection = collections[0]

    def execute(self, context):
        from io_scene_fbx import export_fbx_bin
        from rr_avatar_tools import settings

        for collection, group in zip(self.export_collections(), self.export_groups()):
            if not group.select:
                continue

            self.set_active_collection(collection)

            basepath = self.preferences().generic_export_path

            # Create output directory if needed
            if not os.path.exists(basepath):
                os.makedirs(basepath)

            filepath = os.path.join(basepath, f"{collection.name}.fbx")

            export_fbx_bin.save(
                self, context, filepath=filepath, **settings.full_body_export_fbx
            )

            if self.preferences().copy_images_on_export:
                bpy.ops.rr.export_roomie_item_textures(target=collection.name)

        return {"FINISHED"}


class RR_OT_ExportSelectRoomieItemMeshes(RecRoomRoomieOperator):
    """Select all meshes for given roomie item"""

    bl_idname = "rr.export_select_roomie_item_meshes"
    bl_label = "Select Roomie Item Meshes"
    bl_options = {"REGISTER", "UNDO"}

    rr_require_rec_room_path = False
    rr_required_mode = "OBJECT"

    target: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        collection = bpy.data.collections[self.target]

        for mesh in [o for o in collection.objects if o.type == "MESH"]:
            # Set active if None
            bpy.context.view_layer.objects.active = (
                bpy.context.view_layer.objects.active or mesh
            )

            # Select mesh object
            mesh.select_set(True)

        return {"FINISHED"}


class RR_OT_ExportDeleteRoomieItem(RecRoomRoomieOperator):
    """Delete Roomie Item"""

    bl_idname = "rr.export_delete_roomie_item"
    bl_label = "Delete Roomie Item"
    bl_options = {"REGISTER", "UNDO"}

    rr_require_rec_room_path = False
    rr_required_mode = "OBJECT"

    target: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        collection = bpy.data.collections[self.target]

        scene_collection = context.scene.collection

        for mesh in [m for m in collection.objects if m.type == "MESH"]:
            scene_collection.objects.link(mesh)

        bpy.data.collections.remove(collection)

        return {"FINISHED"}


class RR_OT_ExportToggleRoomieItemVisibilityByLOD(RecRoomRoomieOperator):
    """Toggle visibility"""

    bl_idname = "rr.export_toggle_roomie_item_visibility_by_lod"
    bl_label = "Toggle Roomie Item Visibility"
    bl_options = {"REGISTER", "UNDO"}

    rr_require_rec_room_path = False
    rr_required_mode = "OBJECT"

    lod: bpy.props.EnumProperty(
        name="Target LOD",
        items=[
            ("ALL", "ALL", ""),
            ("LOD0", "LOD0", ""),
            ("LOD1", "LOD1", ""),
            ("LOD2", "LOD2", ""),
        ],
        default="ALL",
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Roomie items
        for collection in rr_avatar_tools.data.roomie_items:
            for object_ in [
                o for o in collection.objects if o.type == "MESH" and "LOD" in o.name
            ]:
                if self.lod == "ALL":
                    object_.hide_set(False)
                    continue

                object_.hide_set(not self.lod in object_.name)

        # Roomie meshes
        for object_ in [
            o
            for o in rr_avatar_tools.data.collections["RM1_Resources"].objects
            if o.type == "MESH" and "LOD" in o.name
        ]:
            if self.lod == "ALL":
                object_.hide_set(False)
                continue

            object_.hide_set(not self.lod in object_.name)

        return {"FINISHED"}


class RR_OT_ExportRoomieItemTextures(RecRoomRoomieOperator):
    """Export Roomie item texture"""

    bl_idname = "rr.export_roomie_item_textures"
    bl_label = "Export Roomie Item Textures"
    bl_options = {"REGISTER", "UNDO"}

    rr_require_rec_room_path = False
    rr_required_mode = "OBJECT"

    target: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def get_images(self, mesh: bpy.types.Mesh):
        images = set()

        material: bpy.types.Material
        for material in mesh.materials:
            i = [n.image for n in material.node_tree.nodes if n.type == "TEX_IMAGE"]
            images = images.union(i)

        return images

    def execute(self, context):
        collection = rr_avatar_tools.data.roomie_items.get(self.target)

        if not collection:
            return {"CANCELLED"}

        images: Set[bpy.types.Image] = set()
        for mesh in [o for o in collection.objects if o.type == "MESH"]:
            i = self.get_images(mesh.data)
            images = images.union(i)

        for image in images:
            name = os.path.basename(image.filepath) or f"{image.name}.png"
            base = self.preferences().generic_export_path
            filepath = os.path.join(base, name)
            image.save(filepath=filepath)

        print(f"Saved {len(images)} images.")

        return {"FINISHED"}


classes = (
    RR_OT_ExportGenericRoomieItems,
    RR_OT_ExportRoomieItems,
    RR_OT_ExportSelectRoomieItemMeshes,
    RR_OT_ExportDeleteRoomieItem,
    RR_OT_ExportToggleRoomieItemVisibilityByLOD,
    RR_OT_ExportRoomieItemTextures,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)
