# Rule 60 V3 Honeycomb Wrist Rest — No Extra Hardware

A code-generated two-piece wrist rest by [minpeter](https://github.com/minpeter).
Integral sliding dovetails connect the halves without screws, magnets or
separate connectors. Optional adhesive anti-slip pads are not included.

[View on MakerWorld](https://makerworld.com/en/models/3490864-rule-60-v3-honeycomb-wrist-rest#profileId-3986872)

Also in this repository: an experimental [HHKB top case with the wrist rest
built in](#hhkb-top-case-with-integrated-wrist-rest-experimental).

![Dovetail joint detail; overview predates the small compression ribs](images/joint-underside.png)

## Download and print

**Current version: tight fit.** The owner printed the male joint coupon and
confirmed a very tight, fully seated fit with the existing receiver. The full
replacement body is being printed; full-body strength and long-term retention
have not been validated.

| File | Use |
| --- | --- |
| [Full wrist rest — 3MF](models/rule60-v9-honeycomb-body.3mf) | Both current halves on one plate |
| [Left / male — STL](models/left.stl) | Replacement male half |
| [Right / female — STL](models/right.stl) | Receiver half |
| [Both halves — STL](models/rule60-one-plate.stl) | Combined print plate |
| [Male-only replacement — 3MF](models/rule60-tight-fit-left.3mf) | Reuse an existing v9 receiver |
| [Male-only fit coupon — 3MF](models/rule60-tight-fit-test-left.3mf) | Test against your existing receiver first |
| [Two-joint fit test — 3MF](models/rule60-v9-joint-test.3mf) | Print both sides of the joint test |
| [Surface and pad sample — 3MF](models/rule60-v9-surface-pad-test.3mf) | Surface feel, adhesion and pad placement |

Existing `rule60-v9-*` download paths are retained, but the body and joint-test
files now contain the tight-fit revision. Older geometry remains in Git history.
The surface sample is unchanged.

Repository 3MFs contain **geometry only**, not printer settings or G-code.
Keep the supplied orientation: the sloping wrist-contact surface faces the
build plate. Re-slice for your printer, nozzle, filament and plate. MakerWorld
also provides a Bambu Studio print profile with the updated geometry.

Body: **295 × 80 × 21 mm**. Eight optional **10 × 4 × 1 mm** adhesive pads
give approximately **22 mm** installed height. The body has 2.4 mm honeycomb
ribs, a 2.2 mm skin and 0.2 mm aperture-edge relief, without X ribs or weight
inserts. Dimensions follow the owner's measured Rule 60 V3 front edge;
compatibility with other keyboard cases is not guaranteed.

## Fit and assembly

The male mating faces are expanded **0.20 mm** to close the original nominal
gap, with four rounded compression ribs adding **0.10 mm per flank** locally.
The v9 receiver interface is unchanged. This is **friction retention, not a
latch**: printing variation, wear and PETG creep can change the holding force.

Place the left half on a flat surface. Align the right half above both tongues,
then lower it evenly into place. Do not force the halves together horizontally
or hammer them. Test the coupon in the same material and settings first; a
successful fit should seat fully without cracking or damaging either half.

Already have a v9 receiver? Print only the male coupon, then the replacement
left half. **Do not combine the enlarged male with the smaller sockets from
the experimental `--clearance 0` revision.** Support both halves when carrying.

Attach equally thick pads inside all eight marked outlines, without covering
the bottom-open sockets. The outlines are not recessed pad pockets.

![Underside and pad locations](images/pad-sites.png)

## Slicing

The updated MakerWorld profile preserves the owner's **X2D / 0.4 mm nozzle,
Bambu PETG Translucent, 0.20 mm layers, 3 walls, 15% infill and no supports**.
Its estimate is approximately **4.1 hours / 72 g**, not a measured completed
print time. Select your own printer, filament and build plate before slicing.

Inspect first-layer adhesion, dovetail overhangs, compression ribs and pad
ledges in the layer preview. The CLI slice completed but reported ZFiller and
reserved-tool-command diagnostics; their impact remains unresolved. A
successful CLI exit does not prove every toolpath is correct. Do not enable
supports inside the mating sockets without checking removal access.

## Reproduce and continue designing

Install [uv](https://docs.astral.sh/uv/), clone the repository, then run:

```sh
uv sync --locked
# Original receiver and no-rib comparison baselines for verification:
uv run build.py 2.4
uv run build.py 2.4 --male-expansion 0.20
# Current published fit:
uv run build.py 2.4 --male-expansion 0.20 --compression 0.10
uv run verify.py rib-2.4-male-expanded-0.20-compression-0.10
uv run export.py
```

`build.py` constructs the geometry in code and reads no external STL or 3MF.
Outputs are in the ignored `rib-2.4-male-expanded-0.20-compression-0.10/`
directory. `rule60-one-plate.3mf`, `replacement-left.3mf`,
`replacement-test-left.3mf` and `test-joint-plate.3mf` correspond to the
downloads above. STL exports use millimetres.

`export.py` refreshes `models/` and the verification evidence. Published STLs
are binary: export removes triangles that collapse at float32 precision, then
checks closed meshes, component counts, dimensions and volume after reload.
This avoids degenerate faces when MakerWorld converts ASCII STL downloads.

The default command without fit options intentionally reproduces the original
looser v9. `--male-expansion 0.20` without `--compression` provides a no-rib
control. Other supported compression values are `0` and `0.05`; fit changes
require a new coupon test. Do not globally scale a part to adjust the joint.

For optional CAD renders, install Blender separately:

```sh
blender -b --python render.py -- rib-2.4-male-expanded-0.20-compression-0.10
```

`uv.lock` pins geometry/check dependencies. Blender and Bambu Studio are
external applications. Private printer configuration, raw logs and caches
are not included; save your own slicer project for repeatable printing.

## Verification and limitations

[Current verification](evidence/verification.json) checks closed connected
meshes, dimensions, plate bounds, 89 insertion positions, intentional contact
confined to the compression ribs, an unchanged receiver, root and entry
geometry, aperture relief, pad heights and layer-section connectivity.
[Current dimensions](evidence/dimensions.json) record the fit parameters.

These checks do not simulate deformation, insertion force, wear, creep or
full-body stiffness. The owner's coupon test confirms fit for their print,
not a universal tolerance guarantee. CAD images are illustrations, not proof
of physical strength or transparent PETG appearance. The overview images
predate the small compression ribs. Automated visual review of the latest
renders was unavailable due to an image-upload quota.

[Historical rib comparison](evidence/rib-comparison.json) covers the original
v9 candidates, not the current tight-fit slicing estimate.

## HHKB top case with integrated wrist rest (experimental)

A replacement Rule 60 V3 **HHKB** top case with the honeycomb wrist rest built
in. It reuses the stock bottom case, PC gasket plate, 12 silicone gasket caps
and four ball-catch strike plates. The case outline and Z levels follow the
owner's caliper measurements of the stock top case; the gasket-cap and
ball-catch pockets follow photo metrology of the same part.

![Exploded view of the two top-case halves](images/topcase-exploded.png)

**Status: not yet test-fitted as a full print.** An earlier corner coupon
confirmed joint positions, ball-catch engagement and screw-hole size; the
outline and Z levels were re-measured after that test.

| File | Use |
| --- | --- |
| [Left half — 3MF](models/rule60-hhkb-topcase-left.3mf) | 206 × 197 mm print, ~75 g |
| [Right half — 3MF](models/rule60-hhkb-topcase-right.3mf) | 149 × 197 mm print, ~65 g |
| [Fit coupons — 3MF](models/rule60-hhkb-topcase-fit-coupons.3mf) | Front-left corner, front joints and back seam |
| [CAD — STEP](models/rule60-hhkb-topcase.step) | Both halves, for remixing |

Assembled: **298.1 × 198.3 mm**, 20.01 mm case height. The halves split at the
centre through the wrist rest and front bezel, joined by three sliding
dovetails with compression ribs. The back bezel continues on the left half to
the back-right ball-catch strike, whose stock plate bridges the back seam with
one M2 screw in each half; a wedge key aligns that seam. Every joint side face
is line-to-line (0 mm); the dovetail landings and the faces under each 45°
print ramp keep a 0.20 mm vertical glue line. Use epoxy or gel cyanoacrylate.
Strike-plate screws must not exceed **5.0 mm under the head** (1.45 mm plate +
3.55 mm pilot).

### Printing

Print each half on its own plate in the supplied orientation, top face on the
plate, without supports or brim. The owner's settings: X2D / 0.4 mm nozzle,
Bambu PETG Translucent, 0.20 mm Standard, 3 walls, 15% infill, textured PEI,
default 0.15 mm elephant-foot compensation. The textured plate forms the
visible top surface.

These 3MFs include a Bambu Studio / Orca **height-range modifier: 0.10 mm
layers from Z 5.4 to 10.0 mm**. At 0.20 mm the 6.30 mm gasket-cap floor
prints at 6.4 and the 9.69 mm bottom-case seat at 9.6, pinching the caps
0.19 mm more; with the range they print at 6.3 and 9.7. Confirm the range in
the object list after opening. Bambu Studio CLI estimates: left 4 h 14 min,
right 3 h 46 min, coupons 1 h 48 min. The CLI slice reported ZFiller
diagnostics.

### Reproduce

The build drives the SolidCraft v0.22.0 headless CLI
(`~/.local/bin/solidcraft-cli`), which is not included. The checks need the
`6095(gas)` plate outline from `rule60-v3.dwg` in
[minjunkim0205/Hobby-CustomKeyboard](https://github.com/minjunkim0205/Hobby-CustomKeyboard/tree/ecf3575e9fb844d32f57b42ce6f7f23f30294396/keyboards/housings/Rule60),
converted to JSON with [`@mlightcad/libredwg-web`](https://www.npmjs.com/package/@mlightcad/libredwg-web);
the drawing is not redistributed here.

```sh
uv run build_topcase_draft.py
RULE60_DWG_JSON=/path/to/rule60-v3.json uv run verify_topcase.py
blender -b -P render_topcase_draft.py   # optional renders
uv run export_topcase.py
```

Outputs go to the ignored `topcase-draft/`; `export_topcase.py` copies the
downloads, STEP, [report](evidence/topcase-report.json),
[verification](evidence/topcase-verification.json) and renders.

### Verification and limitations

The verification checks closed single-shell exports, a 91-step insertion
path with contact only on the compression ribs, 0 mm side faces and 0.20 mm
glue lines, the back-seam strike screws, layer islands and flat overhangs, and
virtual stock parts: the DWG plate through 0.25 mm upward flex, 12 caps,
four strikes, 60 HHKB keycaps through full travel and the stock bottom-case
pocket. The same checks also pass on both halves rebuilt at the printed layer
heights, with the strikes seated on their 5.6 mm printed floor.

Not covered: the stock bottom case was not measured (its pocket copies the
stock top case); the front ball-catch strikes are centred in the available
band, not measured; cap size is photo-derived and the front caps clear their
pocket wall by only 0.08 mm; the stock plate is assumed to match the DWG.
Clearance to the plate (0.30 mm per side) and keycaps (0.32 mm) tolerates up
to about 0.2% print shrinkage.

## License and design history

Copyright 2026 minpeter. The authored source, model exports, documentation and
renders are released under **[CC BY 4.0](LICENSE)**. Attribute this project,
link to the license and identify your changes. Commercial use is permitted.
Third-party tools retain their own licenses. No affiliation with keyboard or
printer manufacturers is implied. The Rule 60 V3 is designed by INKC STUDIO;
the top case is an independent re-creation from measurements of the owner's
stock part and is not an official file.

Early experiments took inspiration from [Shanhj's palm rest](https://makerworld.com/en/models/1326999).
The final v9 generator constructs its geometry in code and embeds neither
that model's mesh nor the Bunny/Dunny connector used in earlier experiments.
This history is acknowledged without claiming the original creator authored
or licensed the v9 generator. The owner's CC BY release does not grant rights
in anyone else's work or constitute a legal determination of independence.
