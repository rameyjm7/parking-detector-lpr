#!/bin/bash
# Script to download PKLot dataset

URL="http://www.inf.ufpr.br/vri/databases/PKLot.tar.gz"
OUTPUT="PKLot.tar.gz"

# Download the file
echo "Downloading PKLot dataset..."
wget -c "$URL" -O "$OUTPUT"

if [ $? -eq 0 ]; then
    echo "Download completed successfully"
    echo "Uncompressing file...This might take some time..."
    pv $OUTPUT | tar xz
else
    echo "Download failed!"
fi
