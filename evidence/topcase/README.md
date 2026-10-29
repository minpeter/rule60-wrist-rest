# HHKB top case — measurements and evidence

Source data behind [`build_topcase_draft.py`](../../build_topcase_draft.py) and the
checks behind the published files. All measurements were taken by the owner
on the stock Rule 60 V3 HHKB top case with a digital vernier caliper
(±0.01 mm display; hand-measurement error of a few hundredths is expected).

`Z_p` is the print-frame height: 0 at the top face (on the build plate),
increasing toward the skirt lip.

## Caliper measurements

| Quantity | Value (mm) | Source | Used as |
| --- | --- | --- | --- |
| Top-case height, top face to skirt lip | 20.01 | [IMG_0333](photos/IMG_0333.jpg) | `SKIRT_H`, `JUNC_H` |
| Bottom-case seat floor (pocketed 10.32 deep from the lip) | 9.69 | [IMG_0334](photos/IMG_0334.jpg) | `Z_FLOOR` |
| Silicone-cap seat level | 6.30 | owner, message 2026-10-28 | `Z_GASKET`, `Z_RELIEF` |
| Ball-catch strike pocket floor | 5.55 | [IMG_0337](photos/IMG_0337.jpg) | `Z_STRIKE` |
| Top-face bezel, left/right sides | 5.65 | owner, message 2026-10-29 | `BEZEL_SIDE` |
| Top-face bezel, back | 10.90 | owner, message 2026-10-29 | `BEZEL_BACK` |
| Top-face bezel, front (outside the HHKB blockers) | 11.02 | owner, message 2026-10-29 | `BEZEL_FRONT` |
| HHKB blocker, from the outer edge | H 30 × W 34.34 | owner, message 2026-10-29 | H checked (30.02); W follows the plate layout |
| Skirt wall, front | 2.80 | owner, message 2026-10-29 | `FRONT_WALL` |
| Skirt wall, sides and back | 2.85 | owner, message 2026-10-29 | `SKIRT_WALL` |
| Short-side underside steps from the outer edge (wall / 9.69 ledge / 6.30 strip) | 2.85 / 4.90 / 5.66 | owner, message 2026-10-29 | `RIM_SEAT_W` = 2.05; checked by `short_side_steps_2p85_4p90_5p66` |
| Previous wrist-rest print length (same printer, PETG, settings; design 295.0) | 295.0 | owner, message 2026-10-29 | shrinkage check |

Readings not used in v6.2:

| Photo | Reading | Note |
| --- | --- | --- |
| [IMG_0335](photos/IMG_0335.jpg) | 7.98 | Level around the gasket area. The owner later asked for the cap pockets and plate relief to be cut straight to the 6.30 level. |
| [IMG_0336](photos/IMG_0336.jpg) | 6.05 | Location not recorded. |
| [IMG_0340](photos/IMG_0340.jpg) | 10.12 | Location not recorded. |
| [IMG_0341](photos/IMG_0341.jpg) | 6.17 | Location not recorded. |

## Photo-derived values

| Quantity | Value | Method |
| --- | --- | --- |
| Strike positions (plate frame) | BL 89.85, BR 196.70, FL 90.22, FR 196.28 | Homography of [IMG_0201](photos/IMG_0201.jpg) on the 8 top-mount holes of the DWG `6095(top)` plate, RMS 0.13 mm ([ball-catch-analysis.json](analysis/ball-catch-analysis.json)) |
| Strike plate | ~20.5 × 6.55 mm, M2 at 13.0 mm pitch, tongue 3.55 × ~5.7 mm | Same analysis plus two-view silhouette fit of IMG_0218 / IMG_0222 |
| Strike pocket "mushroom" end reliefs | 7.25 wide, 4.1 lobe 4.55 past the plate end, end wall 2.15 past, R0.85 shoulder | Two-view ray-cast silhouette fit, IMG_0218 + IMG_0222 (13 mm-eq. ultra-wide, f = 1485 px) ([fit](analysis/strike-pocket-fit-v4.3.png)) |
| Back strike distance from the inner back wall | BL 4.15, BR 4.30 | Same fit; kept when the measured outline moved the wall |
| Front strike distance from the inner front wall | 4.26 | **Not measured**: centred between the front wall and the plate edge |
| Silicone gasket cap | 8.3 × 5.5 × 4.5 free; 8.2 × 4.0 compressed footprint | Rectified underside photo, 28 px/mm ([annotated](analysis/underside-photo-annotated.jpg)) |

The plate outline and tab positions come from the `6095(gas)` drawing in
`rule60-v3.dwg` of [minjunkim0205/Hobby-CustomKeyboard @ ecf3575](https://github.com/minjunkim0205/Hobby-CustomKeyboard/tree/ecf3575e9fb844d32f57b42ce6f7f23f30294396/keyboards/housings/Rule60)
(file hashes in [dwg-source-manifest.json](analysis/dwg-source-manifest.json)).
The drawing is not redistributed.

## Photos

Resized to 1600 px; all EXIF metadata, including location, removed.

| Photos | Content |
| --- | --- |
| [0201](photos/IMG_0201.jpg), [0202](photos/IMG_0202.jpg) | Stock top-case underside with the keyboard, flat on the desk (strike/hole calibration) |
| [0215](photos/IMG_0215.jpg), [0216](photos/IMG_0216.jpg), [0217](photos/IMG_0217.jpg), [0218](photos/IMG_0218.jpg), [0220](photos/IMG_0220.jpg), [0222](photos/IMG_0222.jpg) | Strike pockets and back wall at an angle (two-view fit). 0215, 0216, 0218, 0220 and 0222 arrived incomplete; the flat grey areas are missing image data. |
| [0313](photos/IMG_0313.jpg)–[0317](photos/IMG_0317.jpg) | v4.6 printed corner coupon (white) fitted to the stock case: strike plate in its pocket, bottom-case nesting from the side |
| [0318](photos/IMG_0318.jpg), [0319](photos/IMG_0319.jpg) | Same coupon on the assembled keyboard |
| [0333](photos/IMG_0333.jpg)–[0337](photos/IMG_0337.jpg), [0340](photos/IMG_0340.jpg), [0341](photos/IMG_0341.jpg) | Caliper readings (table above) |

The v4.6 coupon test (owner, 2026-10-28) confirmed joint positions, ball-catch
engagement and screw-hole size. The outline and Z levels were re-measured
afterwards, so that result does not carry over to v6.2 unchanged.

## Analysis artefacts

| File | Content |
| --- | --- |
| [underside-photo-annotated.jpg](analysis/underside-photo-annotated.jpg) | Rectified stock underside with gasket caps, strikes and holes marked |
| [outline-overlay-v4.png](analysis/outline-overlay-v4.png) | v4 model outline over the rectified photo (superseded outline; shows the method) |
| [strike-pocket-fit-v4.3.png](analysis/strike-pocket-fit-v4.3.png) | Two-view strike-pocket silhouette fit |
| [measurement-guide.png](analysis/measurement-guide.png) / [.svg](analysis/measurement-guide.svg) | Guide sent to the owner for what to measure |
| [ball-catch-analysis.json](analysis/ball-catch-analysis.json) | Strike/catch positions and hardware size estimates |
| [dwg-source-manifest.json](analysis/dwg-source-manifest.json) | Source URLs and SHA-256 of the downloaded Rule60 drawings |

## Checks (v6.2)

| File | Content |
| --- | --- |
| [../topcase-verification.json](../topcase-verification.json) | `verify_topcase.py` output on the exported halves |
| [../topcase-report.json](../topcase-report.json) | Build report: Z stack, pocket outlines, back seam, dovetails |
| [checks/as-printed-check.json](checks/as-printed-check.json) | Same checks on both halves rebuilt at the printed layer heights, printed floor heights from the sliced G-code, plan clearances to the stock parts, slicer estimates |
| [checks/seams-v6.2.png](checks/seams-v6.2.png) | Split line, back-seam plan at the BR strike, and sections through the 3 dovetails and the wedge key |
| [checks/underside-levels-v6.2.png](checks/underside-levels-v6.2.png) | Underside height map with the front-left corner enlarged |

`as-printed-check.json` and the two check images were produced during the
design session, not by `build_topcase_draft.py`; regenerate them by hand if the
geometry changes.
