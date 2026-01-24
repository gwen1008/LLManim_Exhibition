#!/bin/bash
# Quick audio test script
echo "2+3" | .venv/bin/python main.py 2>&1 | tee /tmp/audio_test.log
