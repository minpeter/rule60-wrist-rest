"""Rule 60 V3 honeycomb wrist rest by minpeter, licensed CC BY 4.0.
uv run build.py 2.4
Units: mm. Left stays on desk; lower the right half to engage both joints.
"""
from pathlib import Path
import argparse
import json
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import trimesh
import manifold3d as md

parser = argparse.ArgumentParser()
parser.add_argument('rib', type=float, choices=(1.91, 2.1, 2.25, 2.4))
RIB = parser.parse_args().rib
PATTERN = f'rib-{RIB:g}'
ROOT = Path(__file__).resolve().parent / PATTERN
ROOT.mkdir(exist_ok=True)
WIDTH, DEPTH, HEIGHT, HALF = 295., 80., 21., 147.5
JOINT_Y = (28., 56.)
CLEARANCE = .20  # Per mating face, not diametral; sliding, not press fit.
ROW = 10 / np.sqrt(3)

def top(y):
    return (10 + y / 10) * 21 / 18

def solid(mesh):
    result = md.Manifold(md.Mesh64(np.asarray(mesh.vertices, dtype=np.float64),
                                   np.asarray(mesh.faces, dtype=np.uint64)))
    assert result.status() == md.Error.NoError
    return result

def hull(points):
    return solid(trimesh.convex.convex_hull(points))

def mesh_of(obj):
    data = obj.simplify(.00001).to_mesh64()
    mesh = trimesh.Trimesh(data.vert_properties[:, :3], data.tri_verts)
    # Boolean intersections at the rounded frame can leave ~1e-8 mm edges.
    # Weld at 1e-6 mm precision and remove only index-collapsed triangles.
    mesh.merge_vertices(digits_vertex=6)
    f = mesh.faces
    mesh.update_faces((f[:,0]!=f[:,1]) & (f[:,1]!=f[:,2]) & (f[:,0]!=f[:,2]))
    # Welding may collapse a vanishing Boolean sliver to two opposite faces.
    _, inverse, counts = np.unique(np.sort(mesh.faces, axis=1), axis=0,
                                   return_inverse=True, return_counts=True)
    for group in np.flatnonzero(counts > 1):
        normals = mesh.face_normals[inverse == group]
        assert len(normals) == 2 and (np.dot(normals[0], normals[1]) < -.999 or
            max(mesh.area_faces[inverse == group]) < 1e-12), (
            normals.tolist(),mesh.area_faces[inverse == group].tolist())
    mesh.update_faces(counts[inverse] == 1)
    mesh.remove_unreferenced_vertices()
    return mesh

def save(name, obj):
    mesh = mesh_of(obj)
    assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split()) == 1, (
        name, mesh.is_watertight, mesh.is_winding_consistent,
        [(m.volume, m.bounds.tolist()) for m in mesh.split()])
    mesh.export(ROOT / (name + '.stl'), file_type='stl_ascii')
    return mesh

def wedge(x0, x1, y0, y1, inset=0):
    return hull([[x, y, z] for x in (x0, x1) for y in (y0, y1)
                 for z in (0, top(y) - inset)])

outline = md.CrossSection.square([WIDTH - 12, DEPTH - 12]).offset(6, circular_segments=48).translate([6, 6])
inner = outline.offset(-2.2, circular_segments=48)
holes = []
bevels = []
radius = 4.5 - RIB/np.sqrt(3)
for col in range(-23, 23):
    x = HALF + 4.5 + col * 6.75
    for row in range(-6, 7):
        y = 40 + (row + (col % 2)*.5) * 4.5*np.sqrt(3)
        holes.append(md.CrossSection([[
            [x+radius*np.cos(a), y+radius*np.sin(a)]
            for a in np.arange(6)*np.pi/3]]))
        # 0.2 mm, 45-degree relief at the wrist-contact aperture edge.
        bevels.append(md.Manifold.hull_points([
            [x+r*np.cos(a), y+r*np.sin(a), z]
            for z,r in ((2.,radius),(2.2,radius+.2/np.cos(np.pi/6)))
            for a in np.arange(6)*np.pi/3]))
field = md.CrossSection.batch_boolean(holes, md.OpType.Add) ^ inner
seam = md.CrossSection.square([1.5, DEPTH]).translate([HALF-.75, 0])
field -= seam
(ROOT / 'surface.json').write_text(json.dumps({
    'pattern': PATTERN, 'rib_width_mm': RIB, 'opening_radius_mm': radius,
    'skin_thickness_mm': 2.2, 'aperture_edge_bevel_mm': .2}, indent=2))
skin_flat = (outline-field).extrude(2.2)
skin_flat -= md.Manifold.batch_boolean(bevels, md.OpType.Add) ^ (inner-seam).extrude(2.3)
skin = skin_flat.transform(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 7/60, 1, top(0)-2.2]])
full = skin + ((outline - inner).extrude(HEIGHT) ^ wedge(0, WIDTH, 0, DEPTH))
# Eight 10 x 4 x 1 mm adhesive-pad sites; markers do not recess the pad.
# Sloping ledge backs avoid a broad unsupported ceiling in print orientation.
for x in (30.,117.5,177.5,265.):
    for back in (False,True):
        full += hull([[xx, DEPTH-y if back else y, z]
                      for xx in (x-7,x+7)
                      for y,z in ((0,0),(6,0),(6,2),(2.2,5.8),(0,5.8))])
        y = 77 if back else 3
        ring = md.CrossSection.square([10.8,4.8],center=True) - md.CrossSection.square([10,4],center=True)
        full -= ring.extrude(.2).translate([x,y,0])
# The existing continuous mating walls taper into a normal top lattice rib.
points = []
for y in (0, DEPTH):
    for dx, z in [(-4, 0), (4, 0), (-4, top(y)-6), (4, top(y)-6),
                  (-.75, top(y)-2), (.75, top(y)-2)]:
        points.append([HALF+dx, y, z])
full += hull(points)
# Male roots anchor in the existing mating wall; only the female sockets need
# the deeper surrounding blocks and their top-support webs.
left = full ^ md.Manifold.cube([HALF, DEPTH, HEIGHT+1])
for y in JOINT_Y:
    full += wedge(HALF-10, HALF+10, y-10, y+10, 2.5)
    for x in (HALF-10, HALF-5, HALF, HALF+5, HALF+10):
        full += wedge(x-.55, x+.55, y-10, y+10, 2)

right = full ^ md.Manifold.cube([HALF, DEPTH, HEIGHT+1]).translate([HALF, 0, 0])
# Broaden each root with a tapered gusset, joining the original flanks at
# X=1.6. Head width and projection remain unchanged; receiver follows the root.
profile = md.CrossSection([[[-2,-5.6],[0,-5.6],[1.6,-4.8],[6,-7],
                           [6,7],[1.6,4.8],[0,5.6],[-2,5.6]]])
# Flat 1mm-wide root landing at Z=10 is the insertion stop. Beyond it, the
# top slopes 45 degrees down to Z=5 at the tip, avoiding a 6mm cantilever.
ramp = hull([[x, y, z] for x, ztop in [(-2, 10), (1, 10), (6, 5)]
             for y in (-8, 8) for z in (0, ztop)])
tongue = profile.extrude(10) ^ ramp
# Bottom-open sockets let the right body descend over the stationary tongues.
# A flat roof at Z=10 meets only the horizontal root landing, not the ramp.
slot = profile.offset(CLEARANCE, join_type=md.JoinType.Miter).extrude(11).translate([0, 0, -1])
# Flared bottom 0.6 mm guides insertion; clearance above it stays 0.20 mm.
entry = profile.offset(CLEARANCE, join_type=md.JoinType.Miter).scale([1.06,1.06])
slot += entry.extrude(.6, scale_top=[1/1.06,1/1.06])
for y in JOINT_Y:
    left += tongue.translate([HALF, y, 0])
    right -= slot.translate([HALF, y, 0])
installed = [save('left-installed', left), save('right-installed', right)]
trimesh.Scene(installed).export(ROOT / 'assembly.glb')
(ROOT / 'render-meshes.json').write_text(json.dumps([
    {'vertices': m.vertices.tolist(), 'faces': m.faces.tolist()} for m in installed]))

angle = 180 - np.degrees(np.arctan(7/60))
def print_part(name, obj):
    obj = obj.rotate([angle, 0, 0])
    obj = obj.translate(-mesh_of(obj).bounds[0])
    save(name, obj)
    return obj

print_bodies = [print_part('left', left), print_part('right', right)]
plate = [m.translate([20, 20+i*100, 0]) for i, m in enumerate(print_bodies)]
# Both dovetails remain in this cropped pair, so the test exercises simultaneous
# alignment and stops, not just an isolated loose tongue in a generic block.
test = []
for i, obj in enumerate((left, right)):
    crop = obj ^ md.Manifold.cube([30, 52, HEIGHT+1]).translate([HALF-15, 16, 0])
    obj = print_part('test-joint-' + ('left' if i == 0 else 'right'), crop)
    test.append(obj.translate([20+i*55, 20, 0]))

def plate_file(name, objects):
    meshes = [mesh_of(obj) for obj in objects]
    combined = trimesh.util.concatenate(meshes)
    assert np.all(combined.bounds[0] >= -.001) and np.all(combined.bounds[1] < [256, 256, 261])
    combined.export(ROOT / (name+'.stl'), file_type='stl_ascii')
    model = ET.Element('model', {'unit':'millimeter', 'xmlns':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'})
    ET.SubElement(model, 'metadata', {'name':'Title'}).text = 'Rule 60 V3 Honeycomb Wrist Rest — No Extra Hardware (v9): ' + PATTERN
    ET.SubElement(model, 'metadata', {'name':'Designer'}).text = 'minpeter'
    ET.SubElement(model, 'metadata', {'name':'License'}).text = 'CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/'
    resources, build = ET.SubElement(model, 'resources'), ET.SubElement(model, 'build')
    for i, m in enumerate(meshes, 1):
        obj = ET.SubElement(resources, 'object', {'id':str(i), 'type':'model', 'name':('left' if i==1 else 'right')})
        mesh = ET.SubElement(obj, 'mesh')
        vs, ts = ET.SubElement(mesh, 'vertices'), ET.SubElement(mesh, 'triangles')
        for v in m.vertices:
            ET.SubElement(vs, 'vertex', dict(zip(('x','y','z'), map(str,v))))
        for f in m.faces:
            ET.SubElement(ts, 'triangle', dict(zip(('v1','v2','v3'), map(str,f))))
        ET.SubElement(build, 'item', {'objectid':str(i)})
    with zipfile.ZipFile(ROOT/(name+'.3mf'), 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('3D/3dmodel.model', ET.tostring(model, encoding='utf-8', xml_declaration=True))
        z.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    return combined.bounds.tolist()

bounds = plate_file('rule60-one-plate', plate)
plate_file('test-joint-plate', test)
# Small feel/adhesion/pad-placement sample; not a full-width stiffness test.
sample = left ^ md.Manifold.cube([45,35,HEIGHT+1]).translate([15,0,0])
sample_border = (md.CrossSection.square([45,35]) -
                 md.CrossSection.square([43,33]).translate([1,1])).translate([15,0])
sample += sample_border.extrude(2.2).transform(
    [[1,0,0,0],[0,1,0,0],[0,7/60,1,top(0)-2.2]])
sample = print_part('surface-pad-sample', sample)
plate_file('surface-pad-sample', [sample.translate([20,20,0])])
# Validate the actual rigid-body assembly path, not only the seated position.
path = {str(float(d)): (left ^ right.translate([0,0,float(d)])).volume()
        for d in np.linspace(0, 22, 89)}
assert max(path.values()) < .001, path
blocked = {'separate_x_1mm': (left ^ right.translate([1,0,0])).volume(),
           'below_stop_0p2mm': (left ^ right.translate([0,0,-.2])).volume()}
assert min(blocked.values()) > .1, blocked
report = {'assembled_dimensions': trimesh.util.concatenate(installed).extents.tolist(),
          'clearance_per_face_mm': CLEARANCE, 'joint_y_mm': JOINT_Y,
          'root_width_mm':11.2, 'head_width_mm':14, 'projection_mm':6,
          'tip_height_mm':5, 'root_stop_height_mm':10,
          'insertion_path_max_overlap_mm3':max(path.values()),
          'blocked_motion_overlap_mm3':blocked, 'plate_bounds':bounds}
assert np.allclose(report['assembled_dimensions'], [295,80,21])
(ROOT/'dimensions.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
