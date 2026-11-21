#!/usr/bin/env python3
"""
Unpack Android boot.img (Header Version 2)
Extracts kernel, ramdisk, and prints cmdline/kernel parameters.
"""
import struct
import os
import sys

def unpack_boot(img_path, out_dir="boot_extracted"):
    os.makedirs(out_dir, exist_ok=True)
    with open(img_path, "rb") as f:
        hdr = f.read(4096)
        if hdr[:8] != b'ANDROID!':
            print("Error: Invalid Android boot image magic")
            sys.exit(1)

        (kernel_size, kernel_addr, ramdisk_size, ramdisk_addr,
         second_size, second_addr, tags_addr, page_size,
         header_version, os_version) = struct.unpack("<10I", hdr[8:48])

        cmdline = hdr[64:576].decode("latin1", errors="replace").strip("\x00")
        dtb_size = struct.unpack("<I", hdr[1640:1644])[0] if header_version >= 2 else 0

        print(f"Header Version : {header_version}")
        print(f"Kernel Size    : {kernel_size} bytes")
        print(f"Ramdisk Size   : {ramdisk_size} bytes")
        print(f"DTB Size       : {dtb_size} bytes")
        print(f"Page Size      : {page_size} bytes")
        print(f"Kernel Cmdline : {cmdline}")

        def n_pages(sz, psz=page_size):
            return (sz + psz - 1) // psz

        f.seek(page_size)
        kernel_data = f.read(kernel_size)
        with open(os.path.join(out_dir, "kernel.gz"), "wb") as kf:
            kf.write(kernel_data)

        ramdisk_offset = page_size + n_pages(kernel_size, page_size) * page_size
        f.seek(ramdisk_offset)
        ramdisk_data = f.read(ramdisk_size)
        with open(os.path.join(out_dir, "ramdisk.cpio.gz"), "wb") as rf:
            rf.write(ramdisk_data)

        with open(os.path.join(out_dir, "cmdline.txt"), "w") as cf:
            cf.write(cmdline + "\n")

    print(f"[+] Boot image unpacked to {out_dir}/")

if __name__ == "__main__":
    img = sys.argv[1] if len(sys.argv) > 1 else "boot.img"
    out = sys.argv[2] if len(sys.argv) > 2 else "boot_extracted"
    unpack_boot(img, out)
