#!/bin/sh

while IFS=$'\n' read -r pkg
do
    echo installing [$pkg]
    pip install "$pkg"
done < requirements.txt
