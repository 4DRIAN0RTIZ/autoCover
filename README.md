# autoCover

Generate blog cover images (OG images) from the command line.

**Features:** solid/gradient/image backgrounds · text boxes with rounded borders · logo placement · custom fonts · WebP/PNG output

## Requirements

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/) >= 10.0.0

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python autocover.py --title "TITLE" --subtitle "Subtitle" --footer "myblog.com" --output cover.webp
```

### Solid background

```bash
python autocover.py \
  --title "DOMINA TUS COMMITS" \
  --subtitle "METODOLOGÍA CONVENTIONAL COMMITS" \
  --footer "myblog.com" \
  --output cover.png
```

### Gradient background

```bash
python autocover.py \
  --title "Mi Título" \
  --subtitle "Mi Subtítulo" \
  --footer "myblog.com" \
  --gradient "#111111,#ff7f00" \
  --gradient-direction vertical \
  --text-color "#ffffff" \
  --output cover.png
```

### Background image + overlay

```bash
python autocover.py \
  --title "Mi Título" \
  --background assets/backgrounds/bg.png \
  --overlay 0.6 \
  --output cover.png
```

### Full example with boxes and logo

```bash
python autocover.py \
  --title "NOMADA DIGITAL" \
  --subtitle "LLEVA TU HOME A TODAS PARTES" \
  --footer "myblog.com" \
  --background assets/backgrounds/bg.png \
  --logo assets/logos/logo.png \
  --logo-position bottom-left \
  --font assets/fonts/MyFont.ttf \
  --text-color "#ff7f00" \
  --box \
  --box-fill "#00000080" \
  --box-border "#ff7f00" \
  --box-border-width 4 \
  --box-radius 55 \
  --output cover.webp
```

## Options

### Text

| Option | Default | Description |
|---|---|---|
| `--title` | — | Main title (top) |
| `--subtitle` | — | Subtitle (center) |
| `--footer` | — | Footer text (bottom) |
| `--text-color` | `#ff7f00` | Text color (hex) |
| `--font` | system font | Path to TTF/OTF font file |
| `--font-size-title` | auto | Title font size |
| `--font-size-subtitle` | auto | Subtitle font size |
| `--font-size-footer` | auto | Footer font size |
| `--title-max-lines` | `1` | Max lines before wrapping title |
| `--subtitle-max-lines` | `3` | Max lines before wrapping subtitle |
| `--no-shadow` | off | Disable text shadow |

### Background

| Option | Default | Description |
|---|---|---|
| `--bg-color` | `#111111` | Solid background color (hex) |
| `--gradient` | — | Gradient `start,end` (e.g. `"#111111,#ff7f00"`) |
| `--gradient-direction` | `vertical` | `vertical` or `horizontal` |
| `--background` | — | Path to background image |
| `--overlay` | — | Overlay opacity `0.0–1.0` (requires `--background`) |
| `--overlay-color` | `#000000` | Overlay color (hex) |

### Text boxes

| Option | Default | Description |
|---|---|---|
| `--box` | off | Enable rounded text boxes |
| `--box-fill` | — | Box background color with alpha (`#RRGGBBAA`) |
| `--box-border` | `#ff7f00` | Box border color (hex) |
| `--box-border-width` | `3` | Border width in pixels |
| `--box-padding` | `30` | Padding in pixels |
| `--box-radius` | `20` | Corner radius in pixels |

### Logo

| Option | Default | Description |
|---|---|---|
| `--logo` | — | Path to logo image |
| `--logo-size` | `100` | Logo size in pixels |
| `--logo-position` | `top-right` | `top-right`, `top-left`, `bottom-right`, `bottom-left` |

### Output

| Option | Default | Description |
|---|---|---|
| `--output`, `-o` | `cover.png` | Output path (`.png`, `.webp`, `.jpg`) |
| `--width` | `1280` | Image width in pixels |
| `--height` | `720` | Image height in pixels |

## Assets structure

```
assets/
├── backgrounds/   # Background images
├── fonts/         # TTF/OTF font files
├── logos/         # Logo images
└── overlays/      # Overlay textures (optional)
```

## Color format

- Opaque: `#RRGGBB` — e.g. `#ff7f00`
- With alpha (only `--box-fill`): `#RRGGBBAA` — e.g. `#00000080` (50% transparent black)

Alpha reference: `FF`=100% · `BF`=75% · `80`=50% · `40`=25%

## More examples

See [`USAGE_EXAMPLES.md`](USAGE_EXAMPLES.md).
