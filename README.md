# Rule 60 V3 Honeycomb Wrist Rest — No Extra Hardware

A code-generated two-piece wrist rest by [minpeter](https://github.com/minpeter).
The halves slide together using integral dovetails: no screws, magnets or
separate connectors. Optional adhesive anti-slip pads are not included.

[View on MakerWorld](https://makerworld.com/en/models/3490864-rule-60-v3-honeycomb-wrist-rest#profileId-3986872)

![V9 dovetail joint detail](images/joint-underside.png)

## Download and print

- [Full wrist rest, both halves](models/rule60-v9-honeycomb-body.3mf)
- [Two-joint fit test](models/rule60-v9-joint-test.3mf)
- [Surface and pad sample](models/rule60-v9-surface-pad-test.3mf)

These are **model-only 3MFs**, not Bambu Studio projects containing the actual
print settings. Open them in your slicer and keep the supplied orientation:
the sloping wrist-contact surface faces the build plate. Re-slice for your
printer, nozzle, material and plate. No ready-to-print G-code is supplied.

Body: **295 × 80 × 21 mm** maximum height. Eight optional **10 × 4 × 1 mm**
adhesive pads give approximately **22 mm** installed height. The selected v9
has 2.4 mm honeycomb ribs, a 2.2 mm skin and 0.2 mm aperture-edge relief.
There are no X ribs or weight inserts. Compatibility with other cases is not
guaranteed; dimensions came from the owner's measured Rule 60 V3 front edge.

### Starting settings, not a validated universal preset

| Setting | Comparison configuration |
| --- | --- |
| Printer / nozzle | Bambu Lab X2D / 0.4 mm |
| Material | Generic PETG; prefer your actual manufacturer's profile |
| Layers / first layer | 0.20 mm / 0.20 mm |
| Walls / infill | 4 / 15% grid |
| Top / bottom shells | 5 / 3 |
| Supports / ironing | Off / off |
| Plate | Textured PEI |
| Comparison temperatures | Nozzle 255°C / bed 70°C |

The CLI estimated **3 h 5 min / 74.1 g** for the body, **39 min / 11.3 g**
for the joint test and **24 min / 3.7 g** for the surface sample. The owner's
actual Bambu Studio setup estimated **4 h 4 min** for the body. These are
different estimates, not measured completed print times. The actual saved
Bambu Studio project is not included in this repository.

## Assembly

Place the left half on a flat surface. Align the right half above both tongues
and lower it into place. Do not force the halves together horizontally.
Lift the right half to release; there is no vertical latch. Clearance is
0.20 mm per mating face, so zero play is not promised.

**Use both halves from v9. Do not mix with earlier versions.** The roots and
matching sockets changed. Broader roots shorten the straight retaining flanks
from 6 to 4.4 mm; this is a tradeoff, not proof of greater pull-apart strength.
Attach equally thick pads inside the eight marked outlines; do not cover the
bottom-open sockets. The marked areas are not recessed below the body base.

![Underside and pad locations](images/pad-sites.png)

## Continue designing

Install [uv](https://docs.astral.sh/uv/), clone this repository, then run:

```sh
uv sync --locked
uv run build.py 2.4
uv run verify.py rib-2.4
```

`build.py` is the geometry source of truth. It reads no external STL or 3MF.
It writes generated parts, plates, inspection meshes and metadata to the
ignored `rib-2.4/` directory. The other compared rib widths are `1.91`, `2.1`
and `2.25`; edit the script to explore other dimensions. Arbitrary changes
may require changing fit checks and revalidating the physical design.

For optional CAD renders, install Blender separately, then run:

```sh
blender -b --python render.py
```

`uv.lock` pins the geometry/check dependencies. Blender and Bambu Studio are
external applications. The original workstation-specific CLI slicing helper,
private machine paths, raw logs and caches are deliberately not included.
Use the settings above and save your own Bambu Studio project for repeatable
printing. The repository is a reproducible geometry source, not a backup of
the owner's complete printer environment.

## Evidence and limitations

[Verification](evidence/verification.json) covers closed connected meshes,
dimensions, bed bounds, 89 assembly positions, blocking/release movements,
root/receiver relief, entrance flare, aperture bevel, eight pad heights and
layer-section connectivity. It does **not** prove overhang quality, stiffness,
durability, fit, bed adhesion or comfort. Neither small test validates the
full-size unsupported span.

[Rib comparison](evidence/rib-comparison.json) records the Bambu Studio
2.8.2.61 CLI estimates. The selected 2.4 mm rib takes about nine seconds more
and 5.4 g more than the fastest v9 candidate, with less gap infill. Compared
with the earlier no-X body, v9 costs about 6 min 36 s and 6.7 g more.

Body and surface sample had zero ZFiller errors; the joint test retained one.
Reserved-tool-command and headless-display errors also appeared in the CLI.
Their impact remains unresolved: inspect GUI layer previews before printing.
The owner started a full print; its final outcome has not yet been recorded.
Renders show CAD geometry, not transparent PETG optics or physical proof.
Automated-agent visual inspection was unavailable due to image upload quota.

## License and design history

Copyright 2026 minpeter. The authored source, model exports, documentation and
renders are released under **[CC BY 4.0](LICENSE)**. Attribute this project,
link to the license and identify your changes. Commercial use is permitted.
Third-party tools retain their own licenses. No affiliation with keyboard or
printer manufacturers is implied.

Early experiments took inspiration from [Shanhj's palm rest](https://makerworld.com/en/models/1326999).
The final v9 generator constructs its geometry in code and embeds neither
that model's mesh nor the Bunny/Dunny connector used in earlier experiments.
This history is acknowledged without claiming the original creator authored
or licensed the v9 generator. The owner's CC BY release does not grant rights
in anyone else's work or constitute a legal determination of independence.
