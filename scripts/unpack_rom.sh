#!/bin/bash
# Unpack Lain's Project OTA package into raw partition images (.img)
set -e

ZIP_FILE="${1:-Lain's-Project-Retriever(august).zip}"
OUTPUT_DIR="${2:-extracted_images}"

if [ ! -f "$ZIP_FILE" ]; then
    echo "Usage: $0 <path_to_zip> [output_directory]"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
echo "[+] Extracting OTA files from $ZIP_FILE..."
unzip -q -o "$ZIP_FILE" boot.img dtbo.img dynamic_partitions_op_list unsparse_super_empty.img \
    "*.new.dat.br" "*.transfer.list" -d "$OUTPUT_DIR"

cd "$OUTPUT_DIR"

for part in odm product system vendor; do
    if [ -f "${part}.new.dat.br" ]; then
        echo "[+] Decompressing ${part}.new.dat.br..."
        brotli -d "${part}.new.dat.br"
        
        echo "[+] Converting ${part}.new.dat to ${part}.img..."
        python3 /usr/local/bin/sdat2img.py "${part}.transfer.list" "${part}.new.dat" "${part}.img"
        
        rm -f "${part}.new.dat" "${part}.new.dat.br"
    fi
done

echo "[+] Done! Images extracted to $(pwd)"
