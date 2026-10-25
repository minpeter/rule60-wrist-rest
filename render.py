"""Render installed and exploded geometry with Blender, not generated artwork."""
from pathlib import Path
import json
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent / 'rib-2.4'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
parts = []
for i, data in enumerate(json.loads((ROOT / 'render-meshes.json').read_text())):
    mesh = bpy.data.meshes.new(f'part-{i}')
    mesh.from_pydata(data['vertices'], [], data['faces'])
    mesh.update()
    obj = bpy.data.objects.new(f'part-{i}', mesh)
    bpy.context.collection.objects.link(obj)
    parts.append(obj)

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = .55
    return m

body = material('Opaque geometry inspection material', (.16, .18, .20))
receiver = material('Receiver inspection material', (.20, .36, .48))
for i, o in enumerate(parts):
    o.data.materials.clear()
    o.data.materials.append(body if i == 0 else receiver)

bpy.context.view_layer.update()
allpoints = [o.matrix_world @ Vector(c) for o in parts for c in o.bound_box]
print('WORLD BOUNDS', [min(p[i] for p in allpoints) for i in range(3)],
      [max(p[i] for p in allpoints) for i in range(3)])
ground = material('Warm studio ground', (.76, .74, .70))
bpy.ops.mesh.primitive_plane_add(size=2000, location=(147.5, 40, -1))
bpy.context.object.data.materials.append(ground)
ground_object = bpy.context.object
bpy.ops.object.camera_add(location=(430, -390, 370))
cam = bpy.context.object
cam.rotation_euler = (Vector((147.5, 40, 8)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 385
bpy.context.scene.camera = cam
for loc, power, size in [((80, -100, 350), 2200000, 250), ((300, 250, 250), 1500000, 200)]:
    bpy.ops.object.light_add(type='AREA', location=loc)
    light = bpy.context.object
    light.data.energy, light.data.shape, light.data.size = power, 'DISK', size
    light.rotation_euler = (Vector((147.5, 40, 0)) - light.location).to_track_quat('-Z', 'Y').to_euler()
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.world.color = (.3, .3, .3)
scene.render.resolution_x, scene.render.resolution_y = 1400, 850
scene.render.resolution_percentage = 100
scene.render.filepath = str(ROOT / 'assembled.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'preview.blend'))
bpy.ops.render.render(write_still=True)
# Direct top view makes continuity of the triangular field easy to judge.
original_location = cam.location.copy()
original_rotation = cam.rotation_euler.copy()
cam.location = (147.5, 40, 400)
cam.rotation_euler = (0, 0, 0)
scene.render.filepath = str(ROOT / 'top.png')
bpy.ops.render.render(write_still=True)
cam.location = original_location
cam.rotation_euler = original_rotation
parts[1].location.z += 24
scene.render.filepath = str(ROOT / 'exploded.png')
bpy.ops.render.render(write_still=True)
ground_object.hide_render = True
cam.location = (225, -65, -110)
cam.rotation_euler = (Vector((147.5, 42, 10)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.ortho_scale = 125
bpy.ops.object.light_add(type='AREA', location=(150, -20, -100))
bpy.context.object.data.energy = 700000
bpy.context.object.data.size = 100
bpy.context.object.rotation_euler = (Vector((147.5,40,0))-bpy.context.object.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath = str(ROOT / 'joint-underside.png')
bpy.ops.render.render(write_still=True)
parts[1].location.z = 0
cam.location = (147.5,40,-400)
cam.rotation_euler = (Vector((147.5,40,0))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale = 340
scene.render.filepath = str(ROOT / 'pad-sites.png')
bpy.ops.render.render(write_still=True)
