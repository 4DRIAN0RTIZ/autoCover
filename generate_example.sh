#!/bin/bash

# Example script matching the target design style
# Make sure you have:
# - Background image in assets/backgrounds/
# - Logo in assets/logos/

python autocover.py \
  --title "Morph.nvim" \
  --subtitle "React-like renderer para Neovim" \
  --footer "https://cuevaneander.tech/blog" \
  --font assets/fonts/Prehistoric-Caveman.ttf \
  --background assets/backgrounds/bg.png \
  --logo assets/backgrounds/logo.png \
  --logo-position bottom-left \
  --logo-size 280 \
  --text-color "#e38228" \
  --box \
  --box-fill "#00000080" \
  --box-border "#e38528" \
  --box-border-width 4 \
  --box-padding 30 \
  --box-radius 55 \
  --output morph-nvim-react-like-renderer-para-neovim.webp

echo "Cover generated successfully"
