# autoCover - Usage Examples

## Basic Examples

### Simple Cover with Solid Background

```bash
python -m autocover.cli \
  --title "My Blog Post" \
  --subtitle "A detailed guide" \
  --footer "myblog.com" \
  --output cover.png
```

### Cover with Gradient Background

```bash
python -m autocover.cli \
  --title "Python Tips" \
  --subtitle "Advanced Techniques" \
  --gradient "#1a1a2e,#16213e" \
  --text-color "#0f3460" \
  --output gradient_cover.png
```

## Advanced Examples with Text Boxes

### Cover with Rounded Boxes (Like Target Design)

```bash
python -m autocover.cli \
  --title "NOMADA DIGITAL" \
  --subtitle "LLEVA TU HOME A TODAS PARTES" \
  --footer "https://cuevaneander.tech/blog" \
  --background assets/backgrounds/your_bg.png \
  --logo assets/logos/your_logo.png \
  --logo-position bottom-left \
  --text-color "#ff7f00" \
  --box \
  --box-fill "#00000080" \
  --box-border "#ff7f00" \
  --box-border-width 4 \
  --box-padding 30 \
  --box-radius 25 \
  --output stylish_cover.png
```

### Understanding Box Parameters

- `--box`: Enable text boxes (required to activate box features)
- `--box-fill`: Background color with alpha (transparency)
  - Format: `#RRGGBBAA` where AA is alpha (00=transparent, FF=opaque)
  - Example: `#00000080` = black with 50% transparency
  - Example: `#ffffff40` = white with 25% transparency
- `--box-border`: Border color (hex format)
- `--box-border-width`: Border thickness in pixels
- `--box-padding`: Space between text and box edge
- `--box-radius`: Corner roundness (higher = more rounded)

## Logo Positioning

```bash
# Logo in bottom-left
--logo assets/logos/logo.png --logo-position bottom-left

# Logo in top-right (default)
--logo assets/logos/logo.png --logo-position top-right

# Logo in top-left
--logo assets/logos/logo.png --logo-position top-left

# Logo in bottom-right
--logo assets/logos/logo.png --logo-position bottom-right
```

## Custom Fonts

```bash
python -m autocover.cli \
  --title "Typography Matters" \
  --font assets/fonts/GeistMono-Medium.ttf \
  --font-size-title 90 \
  --output custom_font.png
```

## Background Images with Overlay

```bash
python -m autocover.cli \
  --title "Beautiful Backgrounds" \
  --background assets/backgrounds/photo.jpg \
  --overlay 0.6 \
  --overlay-color "#000000" \
  --text-color "#ffffff" \
  --output bg_overlay.png
```

The `--overlay` parameter adds a semi-transparent layer over the background:
- `0.0` = completely transparent (no overlay)
- `0.5` = 50% opacity
- `1.0` = completely opaque (solid color)

## Creating Your Own Defaults

Create a shell alias in your `~/.bashrc` or `~/.zshrc`:

```bash
alias blogcover='python -m autocover.cli \
  --background ~/autoCover/assets/backgrounds/default_bg.png \
  --logo ~/autoCover/assets/logos/my_logo.png \
  --logo-position bottom-left \
  --text-color "#ff7f00" \
  --box \
  --box-fill "#00000080" \
  --box-border "#ff7f00" \
  --box-border-width 4 \
  --footer "myblog.com"'
```

Then use it simply:

```bash
blogcover --title "My New Post" --subtitle "Post description"
```

## Color Formats

### RGB (Opaque)
- `#RRGGBB` format
- Example: `#ff7f00` = orange
- Example: `#ffffff` = white
- Example: `#000000` = black

### RGBA (With Transparency)
- `#RRGGBBAA` format (only for --box-fill)
- Example: `#00000080` = black, 50% transparent
- Example: `#ff7f0040` = orange, 25% transparent
- Example: `#ffffffCC` = white, 80% opaque

To convert opacity percentage to hex:
- 100% = FF
- 75% = BF
- 50% = 80
- 25% = 40
- 10% = 1A
