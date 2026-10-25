"""Verify exported v9 geometry, not just in-memory construction."""
from pathlib import Path
import json
import sys
import numpy as np
import trimesh
import manifold3d as md
from shapely import build_area
from shapely.geometry import MultiLineString

root=Path(__file__).resolve().parent/sys.argv[1]
names=('left','right','left-installed','right-installed','test-joint-left',
       'test-joint-right','surface-pad-sample')
parts={n:trimesh.load_mesh(root/(n+'.stl')) for n in names}
for name,m in parts.items():
    assert m.is_watertight and m.is_winding_consistent and len(m.split())==1, name
for name,count in [('rule60-one-plate',2),('test-joint-plate',2),('surface-pad-sample',1)]:
    scene=trimesh.load(root/(name+'.3mf'))
    assert len(scene.geometry)==count
    assert np.all(scene.bounds[0]>=-.001) and np.all(scene.bounds[1]<[256,256,261])

left,right=[md.Manifold(md.Mesh64(parts[n].vertices,parts[n].faces.astype(np.uint64)))
            for n in ('left-installed','right-installed')]
assert np.allclose(trimesh.util.concatenate([parts['left-installed'],parts['right-installed']]).extents,[295,80,21])
dimensions=json.loads((root/'dimensions.json').read_text())
interference=dimensions.get('compression_interference_per_flank_mm')
clearance=dimensions['clearance_per_face_mm']
socket_offset=dimensions.get('socket_offset_per_face_mm',clearance)
expansion=dimensions.get('male_expansion_per_face_mm',0.)
if expansion:
    original_root=root.parent/root.name.split('-male-expanded-')[0]
    m=trimesh.load_mesh(original_root/'right-installed.stl')
    original=md.Manifold(md.Mesh64(m.vertices,m.faces.astype(np.uint64)))
    assert (right-original).volume()<.001 and (original-right).volume()<.001
    scene=trimesh.load(root/'replacement-left.3mf')
    assert len(scene.geometry)==1
    assert np.all(scene.bounds[0]>=-.001) and np.all(scene.bounds[1]<[256,256,261])
# Probe receiver walls away from ribs: catches an accidentally unchanged socket.
for y in (28.,56.):
    for side in (-1,1):
        center=np.array([151.3,y+side*5.9,6.])
        normal=np.array([-1.,2.*side,0.])/np.sqrt(5)
        probes=[center+normal*(socket_offset-.01),center+normal*(socket_offset+.01)]
        assert parts['right-installed'].contains(probes).tolist()==[False,True]
        if expansion:
            probes=[center+normal*(expansion-.01),center+normal*(expansion+.01)]
            assert parts['left-installed'].contains(probes).tolist()==[True,False]
allowed=md.Manifold()
if interference is not None:
    baseline=root.parent/root.name.split('-compression-')[0]
    for name,actual in [('left-installed',left),('right-installed',right)]:
        m=trimesh.load_mesh(baseline/(name+'.stl'))
        original=md.Manifold(md.Mesh64(m.vertices,m.faces.astype(np.uint64)))
        assert (original-actual).volume()<.001, name
        if name=='right-installed':
            assert (actual-original).volume()<.001, 'Receiver must match same-clearance baseline'
        else:
            added=actual-original
    for y in (28.,56.):
        for side in (-1,1):
            allowed+=md.Manifold.cube([2,2,4]).translate([150.3,y+side*5.9-1,1])
            # Independently probe both sides of the requested crest position.
            center=np.array([151.3,y+side*5.9,3.])
            normal=np.array([-1.,2.*side,0.])/np.sqrt(5)
            crest=socket_offset+interference
            probes=[center+normal*(crest-.01),center+normal*(crest+.01)]
            assert parts['left-installed'].contains(probes).tolist()==[True,False]
    assert added.volume()>.1 if clearance+interference>0 else added.volume()<.001
    assert (added-allowed).volume()<.001, 'Changes outside four local ribs'
path=[(left^right.translate([0,0,float(z)])).volume() for z in np.arange(0,22.01,.25)]
unexpected=[((left^right.translate([0,0,float(z)]))-allowed).volume()
            for z in np.arange(0,22.01,.25)]
assert max(unexpected)<.001
if interference is None or interference==0:
    assert max(path)<.001
else:
    assert path[0]>.001, 'Expected compression contact is absent'
motion={name:(left^right.translate(d)).volume() for name,d in {
    'seated':[0,0,0],'small_play':[.2,0,0],'sideways_blocked':[1,0,0],
    'foreaft_blocked':[0,1,0],'stop':[0,0,-.2],'lift_release':[10,0,12]}.items()}
assert motion['lift_release']<.001, motion
if interference is None:
    assert motion['seated']<.001, motion
    if clearance==0:
        assert motion['small_play']>.1, motion
    else:
        assert motion['small_play']<.001, motion
assert min(motion[k] for k in ('sideways_blocked','foreaft_blocked','stop'))>.1, motion
# Root material and the corresponding receiver relief must both exist.
assert parts['left-installed'].contains([[147.7,33.3,2]])[0]
assert not parts['right-installed'].contains([[147.7,33.3,2]])[0]
# Extra clearance only at the entrance, not throughout the bearing face.
assert parts['right-installed'].contains([[153.6+socket_offset,28,.1],[153.6+socket_offset,28,1]]).tolist()==[False,True]
# The aperture opens at the contact edge, while the deeper rib remains intact.
radius=json.loads((root/'surface.json').read_text())['opening_radius_mm']
y=40+radius*np.cos(np.pi/6)+.1
z=(10+y/10)*21/18
assert parts['left-installed'].contains([[84.5,y,z-.05],[84.5,y,z-.4]]).tolist()==[False,True]
# Pad centers remain at Z=0; the etched border is recessed by only 0.2 mm.
for x in (30,117.5,177.5,265):
    m=parts['left-installed' if x<147.5 else 'right-installed']
    for y in (3,77):
        points=[[x,y,-1],[x+5.2,y,-1]]
        hits,ids,_=m.ray.intersects_location(points,[[0,0,1]]*2)
        heights=[min(hits[ids==i,2]) for i in range(2)]
        assert np.allclose(heights,[0,.2],atol=1e-5),(x,y,heights)

layers={}
for name in ('left','right','test-joint-left','test-joint-right','surface-pad-sample'):
    m=parts[name];previous=None;floating=[]
    for z in np.arange(.1,m.bounds[1,2],.2):
        section=m.section([0,0,1],[0,0,z])
        if section is None: continue
        shape=build_area(MultiLineString([p[:,:2] for p in section.discrete]))
        pieces=list(shape.geoms) if shape.geom_type=='MultiPolygon' else [shape]
        if previous is not None:
            for piece in pieces:
                if piece.area>.02 and piece.intersection(previous.buffer(.02)).area<.0001:
                    floating.append({'z':float(z),'area':piece.area})
        previous=shape
    layers[name]=floating
assert not any(layers.values()),layers
report={'closed_parts':list(parts),'insertion_positions':len(path),
        'compression_interference_per_flank_mm':interference,
        'max_overlap_outside_compression_ribs_mm3':max(unexpected),
        'max_insertion_overlap_mm3':max(path),'motion_overlap_mm3':motion,
        'root_and_entry_checks':'passed','aperture_bevel_check':'passed',
        'eight_pad_height_checks':'passed','floating_layer_components':layers}
(root/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
