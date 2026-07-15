#!/bin/bash

echo "🔄 Step 1: Running data engine to fetch latest market trends..."
python engine.py

# Check if the engine step succeeded before moving on
if [ $? -eq 0 ]; then
    echo "🎬 Step 2: Passing fresh data to video compiler..."
    python maker.py
    echo "🎉 Process complete! Your updated daily video is ready."
else
    echo "❌ Error: Data engine failed. Skipping video generation."
    exit 1
fi
