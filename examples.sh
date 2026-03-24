#!/bin/bash

# Basic example
python autocover.py \
  --title "DOMINA TUS COMMITS" \
  --subtitle "METODOLOGÍA CONVENTIONAL COMMITS" \
  --footer "cuevaneander.tech/blog" \
  --output examples/example1.png

# With gradient
python autocover.py \
  --title "Python Tips & Tricks" \
  --subtitle "Improve Your Code Quality" \
  --footer "cuevaneander.tech/blog" \
  --gradient "#1a1a2e,#16213e" \
  --text-color "#0f3460" \
  --output examples/example2.png

# With custom colors
python autocover.py \
  --title "Web Development" \
  --subtitle "Modern JavaScript Framework" \
  --footer "cuevaneander.tech/blog" \
  --bg-color "#0d1117" \
  --text-color "#58a6ff" \
  --output examples/example3.png

# Horizontal gradient
python autocover.py \
  --title "Machine Learning" \
  --subtitle "Deep Learning Fundamentals" \
  --footer "cuevaneander.tech/blog" \
  --gradient "#ff6b6b,#4ecdc4" \
  --gradient-direction horizontal \
  --text-color "#ffffff" \
  --output examples/example4.png

echo "Examples generated in examples/ directory"
