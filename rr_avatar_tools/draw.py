import bpy
import gpu
from gpu_extras.batch import batch_for_shader

import rr_avatar_tools

coords = (
    (-1, -1, -1),  # 0
    (+1, -1, -1),  # 1
    (-1, +1, -1),  # 2
    (+1, +1, -1),  # 3
    (-1, -1, +1),  # 4
    (+1, -1, +1),  # 5
    (-1, +1, +1),  # 6
    (+1, +1, +1),  # 7
)

wire_indices = (
    (0, 1),
    (0, 2),
    (1, 3),
    (2, 3),
    (4, 5),
    (4, 6),
    (5, 7),
    (6, 7),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
)

wire_shader = gpu.shader.from_builtin("POLYLINE_UNIFORM_COLOR")
wire_batch = batch_for_shader(
    wire_shader, "LINES", {"pos": coords}, indices=wire_indices
)

cube_indices = (
    (4, 2, 0),  # -X face
    (4, 6, 2),  # -X face
    (1, 3, 5),  # +X face
    (3, 7, 5),  # +X face
    (1, 4, 0),  # -Y face
    (4, 1, 5),  # -Y face
    (2, 6, 3),  # +Y face
    (7, 3, 6),  # +Y face
    (2, 1, 0),  # -Z face
    (3, 1, 2),  # -Z face
    (4, 5, 6),  # +Z face
    (6, 5, 7),  # +Z face
)

cube_shader = gpu.shader.from_builtin("UNIFORM_COLOR")
cube_batch = batch_for_shader(
    cube_shader, "TRIS", {"pos": coords}, indices=cube_indices
)


def draw_avatar_bounding_boxes():
    region = bpy.context.region
    vm = bpy.context.region_data.perspective_matrix
    bounding_box_list = bpy.context.scene.avatar_bounding_box_list

    show_both_wrists = [b for b in bounding_box_list if b.name == "WRIST.BOTH"][
        0
    ].select

    for bb in bounding_box_list:
        visible = bb.select

        if bb.name.startswith("WRIST"):
            visible |= show_both_wrists

        if not visible:
            continue

        m = rr_avatar_tools.avatar.bounds.bounding_boxes[bb.name]
        m = vm @ m

        # Wireframe
        wire_shader.uniform_float("ModelViewProjectionMatrix", m)
        wire_shader.uniform_float("color", (0, 0, 0, 1))
        wire_shader.uniform_float("viewportSize", (region.width, region.height))
        wire_shader.uniform_float("lineWidth", 2)

        wire_batch.draw(wire_shader)

        # Solid
        cube_shader.uniform_float("ModelViewProjectionMatrix", m)
        cube_shader.uniform_float("color", (0, 0, 0, 0.25))

        gpu.state.blend_set("ALPHA")
        gpu.state.face_culling_set("BACK")
        cube_batch.draw(cube_shader)
        gpu.state.face_culling_set("NONE")
        gpu.state.blend_set("NONE")


def draw_roomie_bounding_boxes():
    region = bpy.context.region
    vm = bpy.context.region_data.perspective_matrix
    bounding_box_list = bpy.context.scene.roomie_bounding_box_list

    # show_both_wrists = [b for b in bounding_box_list if b.name == "WRIST.BOTH"][
    #     0
    # ].select
    show_both_wrists = False

    for bb in bounding_box_list:
        visible = bb.select

        if bb.name.startswith("WRIST"):
            visible |= show_both_wrists

        if not visible:
            continue

        # m = bounding_boxes[bb.name]
        m = rr_avatar_tools.roomie.bounds.bounding_boxes.get(bb.name)

        if not m:
            continue

        m = vm @ m

        # Wireframe
        wire_shader.uniform_float("ModelViewProjectionMatrix", m)
        wire_shader.uniform_float("color", (0, 0, 0, 1))
        wire_shader.uniform_float("viewportSize", (region.width, region.height))
        wire_shader.uniform_float("lineWidth", 2)

        wire_batch.draw(wire_shader)

        # Solid
        cube_shader.uniform_float("ModelViewProjectionMatrix", m)
        cube_shader.uniform_float("color", (0, 0, 0, 0.25))

        gpu.state.blend_set("ALPHA")
        gpu.state.face_culling_set("BACK")
        cube_batch.draw(cube_shader)
        gpu.state.face_culling_set("NONE")
        gpu.state.blend_set("NONE")


def register():
    bpy.types.SpaceView3D.draw_handler_add(
        draw_avatar_bounding_boxes, (), "WINDOW", "POST_VIEW"
    )
    bpy.types.SpaceView3D.draw_handler_add(
        draw_roomie_bounding_boxes, (), "WINDOW", "POST_VIEW"
    )


def unregister():
    bpy.types.SpaceView3D.draw_handler_remove(draw_avatar_bounding_boxes, "WINDOW")
    bpy.types.SpaceView3D.draw_handler_remove(draw_roomie_bounding_boxes, "WINDOW")
