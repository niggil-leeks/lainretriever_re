# Lain's Project (Retriever)

Technical dump and breakdown of Lain's Project (Retriever), an Android 16 (One UI 8 / API 36) port for Samsung Galaxy S20 FE (r8q, SM-G780G/SM-G781B).

### Quick notes
- Target: Galaxy S20 FE (`r8q`, Snapdragon 865 `kona`).
- Port Base: Galaxy A73 5G (`a73xq`, `SM-A736B`) Android 16 QSSI.
- Why A73 base: Uses optical in-display fingerprint (`optical_display_phone`) matching S20 FE, instead of ultrasonic sensors from S-series flagships.
- Kernel: `4.19.325-ryzen-shine` compiled with Clang 22.
- Shims: Pixel 4 (`coral`) USB HAL 1.3 adapted for Qualcomm `a600000.ssusb` sysfs.
- Partitions: Resizes `qti_dynamic_partitions` in super (system ~6.3GB, vendor ~1.7GB, product ~1.1GB, odm ~54MB).

### Contents
- `boot/`: boot.img, dtbo.img, extracted kernel, ramdisk with fstab, cmdline.
- `build_props/`: build.prop from system, vendor, product, odm, etc.
- `config/`: dynamic_partitions_op_list, updater-script, metadata.
- `vendor/`: init scripts, VINTF manifests, ueventd.
- `product/`: RRO overlay APKs.
- `odm/`: sepolicy and sha256 mappings.
- `scripts/`: unpack scripts for OTA payload and boot.img.
