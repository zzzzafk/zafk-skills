# Page Capabilities — Deep Reference

## Color Page

### Node Types

| Node | Shortcut | Behavior |
|------|----------|----------|
| Serial | Alt+S | Chains left-to-right; order matters — each output feeds the next |
| Parallel | Alt+P | Multiple branches from same source → Parallel Mixer (averages equally) |
| Layer | Alt+L | Layer Mixer with composite modes; bottom input = highest priority |
| Splitter/Combiner | Alt+Y | Separates R/G/B into independent streams, recombines |
| Outside | Alt+O | Auto-generated inverted matte from parent qualifier/power window |
| Key Mixer | — | Combines alpha channels from multiple sources |
| Shared Node | Right-click | Propagates across every clip where attached (project or timeline level) |

### Ideal Node Tree Template

```
[Input CST]     ← Camera space to DWG/DI (or auto with RCM)
    ↓
[NR]            ← Temporal + Spatial NR (before corrections)
    ↓
[Primary]       ← Lift/Gamma/Gain: exposure, WB, contrast
    ↓
[Secondaries]   ← Parallel branch: skin // sky // object isolation
    ↓
[Creative]      ← LUT node (Key Output Gain = LUT intensity) or Color Warper
    ↓
[Texture]       ← Film grain, halation (60-80% opacity on layer node)
    ↓
[Output CST]    ← DWG/DI to Rec.709 / P3 / PQ (or auto with RCM)
```

### Color Science Modes

| Mode | When to Use |
|------|-------------|
| DaVinci YRGB | Manual color management; no auto transforms |
| YRGB Color Managed (RCM) | Recommended for most projects; automatic input/output transforms |
| ACEScct | Academy standard; log tone curve; preferred over ACEScc |
| ACEScc | Pure log ACES; older pipeline compatibility |
| ACES 2.0 | New in Resolve 20; OCIO 2.4.2-based |

### Recommended Color Spaces

| Stage | Recommended |
|-------|-------------|
| Timeline / Working | DaVinci Wide Gamut + DaVinci Intermediate |
| Output (SDR) | Rec.709 Gamma 2.4 |
| Output (HDR) | Rec.2020 ST.2084 or Rec.2100 HLG |
| DCI | P3-D65 |

### Curves Available

- **Custom (YRGB)** — Master + per-channel curves with Log/Lin toggle
- **Hue vs Hue** — Remap any hue range to a different hue
- **Hue vs Saturation** — Boost/reduce saturation per hue range
- **Hue vs Luminance** — Brighten/darken a specific hue range
- **Luminance vs Saturation** — Saturation control by exposure zone
- **Saturation vs Saturation** — Saturation by existing saturation
- **YSFX** — Y-channel spatial effects curves
- **Soft Clip** — Adjustable knee for highlight/shadow rolloff

### Qualifier Tool Parameters

| Control | Function |
|---------|----------|
| Hue Center/Width/Softness | HSL key range |
| Luminance Min/Max/Softness | Luma key range |
| Saturation Low/High | Saturation range |
| 3D Qualifier | Spatial 3D color sampling |
| Denoise | Pre-key noise reduction |
| Clean Black/White | Matte cleanup |
| Blur Radius | Matte softening |
| In/Out Ratio | Feather bias |
| Shrink/Grow | Morphological expand/contract |

### Scopes

| Scope | Use for |
|-------|---------|
| Waveform | Exposure, black/white levels, luma distribution |
| Parade (RGB) | Color balance, cast identification per zone |
| Vectorscope | Hue/saturation; skin tone at ~10 o'clock; color accuracy |
| Histogram | Shadow/midtone/highlight density |
| CIE Chromaticity | Gamut boundary check (Rec.709/P3/Rec.2020) |

---

## Fusion Page

### Node Categories

**2D Compositing (most common):**
- `Merge` — Composite FG over BG via alpha (all blend modes)
- `Transform` — 2D position/rotation/scale
- `Crop`, `Scale`, `Resize` — geometric adjustments
- `ColorCorrector`, `BrightnessContrast`, `HueCurves` — color in comp
- `Blur`, `UnsharpMask`, `Defocus`, `GlowFusion` — effects
- `Text+` — advanced character generator (see below)
- `Background` — solid color or gradient generator
- `FastNoise`, `Plasma`, `Texture` — procedural generators

**Masking & Roto:**
- `Polygon` — Bézier with per-point feathering
- `BSpline` — Smooth tension-based curves
- `Rectangle`, `Ellipse` — Simple shape masks
- `Bitmap` — Convert luma/alpha channel to mask
- `Paint` — Vector strokes (Clone, Erase, Wire Removal, Smear)
- `Magic Mask` — AI person/object isolation with tracking

**Tracking:**
- `Tracker` — Point tracker (contrast or AI)
- `PlanarTracker` — Flat surface track → `PlanarTransform`
- `CameraTracker` — 3D camera solve (Studio)

**Particles:**
- `pEmitter` — Particle source (Point/Line/Plane/Cube/Sphere/Bitmap regions)
- `pRender` — Renders particles to 2D
- `pTurbulence`, `pDirectionalForce`, `pBounce`, `pFriction` — forces
- `pSpawn` — Spawn child particles
- `pCustom` / `pCustomForce` — Lua expression-based custom forces

**3D Pipeline:**
- `MediaIn3D` → `Merge3D` → `Camera3D` + `DomeLight3D` → `Renderer3D`
- `Shape3D` — primitives (cube, sphere, cone, torus, plane)
- `Text3D` — extruded/beveled 3D text
- `FBXMesh3D` — import .fbx / .obj / .abc
- `ImagePlane3D` — 2D image in 3D space
- `Replicate3D` — instance geometry

**Resolve 20 New:**
- Deep Image Compositing (OpenEXR multi-layer)
- Vector Warping toolset
- Cryptomatte support
- PSD layer import as individual nodes
- Magic Mask v2 with paint brush refinement

### Text+ Node Key Parameters

| Tab | Key Parameters |
|-----|----------------|
| Text | Styled Text, Font, Color, Size (rel. to width), Tracking, Line Spacing, Write On, OpenType features |
| Shading | 8 elements, each: Fill Type (Solid/Gradient/Image), appearance (Fill/Outline), Opacity, Softness, Glow |
| Layout | Mode: Point / Frame / Circle / Path; Position on Path 0–1+ |
| Transform | Position, Rotation, Size relative to composition |
| Image | Background/foreground compositing with pre-multiplied alpha |
| Advanced | Anti-alias quality, sub-pixel rendering |

Text on path: Set Layout Mode → Path, then draw a spline. Animate `Position on Path` parameter for write-on effects.

---

## Fairlight Audio Page

### Track Types

| Type | Channels | Use |
|------|----------|-----|
| Mono | 1 | Single mic, VO, sound design |
| Stereo | 2 | Music, ambience, stereo pairs |
| 5.1 | 6 | Surround submix |
| 7.1 | 8 | Cinema surround |
| 7.1.4 (Atmos) | 12 | Dolby Atmos (Studio) |
| Adaptive | 1–24 | Multi-format with user-defined mapping |

### FlexBus Routing

Every track can output to up to 20 sets of busses (3 busses per set = 60 destinations). Cascading is supported up to 6 layers deep. Standard routing: `Track → Submix Bus → Main Mix Bus → Output`.

### FairlightFX Plugins (Built-in)

| Plugin | Use |
|--------|-----|
| Dialogue Processor | All-in-one: de-rumble, de-esser, de-pop, compressor, expander, exciter |
| Dialogue Leveler | Auto-level speech (Resolve 20) |
| Noise Reduction | Spectral noise floor learn + remove |
| Voice Isolation | AI speech/noise separation (Studio, Neural Engine) |
| Voice Convert | Change speaker voice with model (Resolve 20, Studio) |
| De-Esser | High-frequency sibilance control |
| De-Hummer | 50/60Hz hum removal |
| Multiband Compressor | 4-band compressor with crossover points |
| Reverb | Algorithmic reverb with pre-delay, room size, damping |
| Foley Sampler | MIDI-triggered Foley SFX (Studio) |
| Vocal Channel | Comprehensive vocal chain in single plugin |

### Loudness Standards

| Standard | Target LUFS | True Peak | Platform |
|----------|-------------|-----------|----------|
| EBU R128 | −23 LUFS | −1 dBTP | EU broadcast |
| ATSC A/85 | −24 LKFS | −2 dBTP | US broadcast |
| YouTube | −14 LUFS | −1 dBTP | Online |
| Apple Podcasts | −16 LUFS | −1 dBTP | Podcast |
| Spotify | −14 LUFS | −1 dBTP | Music streaming |
| Netflix | −27 LUFS | −2 dBTP | Streaming (drama) |

---

## Deliver Page — Codec Matrix

| Container | Codecs | Alpha | Notes |
|-----------|--------|-------|-------|
| MP4 | H.264, H.265 | No | Web delivery |
| QuickTime | ProRes 422 Proxy/LT/422/HQ, ProRes 4444, ProRes 4444 XQ, DNxHD, DNxHR, H.264, H.265, Cineform | ProRes 4444/XQ only | Broadcast/archival |
| MXF OP-Atom | DNxHD, DNxHR, JPEG2000, XDCAM | No | Avid compatibility |
| MXF OP1A | XAVC, DNxHR | No | Broadcast ingest |
| EXR | RGB Half, RGB Float, DWAA, DWAB | Yes | VFX, HDR |
| DPX | Various | No | Film/archive |
| TIFF | 8/16-bit | Yes | Image sequences |
| DCP | JPEG 2000 | No | Digital cinema |

### Render Settings Key Parameters

| Setting | Values |
|---------|--------|
| `FormatWidth` / `FormatHeight` | e.g., 1920/1080, 3840/2160, 4096/2160 |
| `FrameRate` | 23.976, 24, 25, 29.97, 30, 48, 50, 59.94, 60 |
| `VideoQuality` | 0=Automatic, higher = better |
| `ExportVideo` / `ExportAudio` | true/false |
| `AudioBitDepth` | 16, 24, 32 |
| `AudioSampleRate` | 44100, 48000, 96000 |
| `SeparateAudioTrack` | true/false |
| `UseNetworkOptimization` | true (for streaming delivery) |
| `EnableSubtitleRendering` | true = burn-in subtitles |
| `SubtitleStyle` | Burn-in or Embedded |

### Export Types for `timeline → export`

| ExportType String | Format |
|-------------------|--------|
| `EXPORT_AAF` | Avid AAF |
| `EXPORT_DRT` | DaVinci Resolve Timeline |
| `EXPORT_EDL` | CMX EDL |
| `EXPORT_FCP_7_XML` | Final Cut Pro 7 XML |
| `EXPORT_FCPXML_1_9` | Final Cut Pro X XML |
| `EXPORT_HDRCMX` | HDR CMX |
| `EXPORT_TEXT_CSV` | CSV |
| `EXPORT_TEXT_TABBED` | Tab-delimited text |
| `EXPORT_YOUTUBE_CHAPTERS` | YouTube chapter markers |
| `EXPORT_OTIO` | OpenTimelineIO |
