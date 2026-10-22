#!/usr/bin/env python3
"""Package PC translated game files into PvZ-Fusion-4.0.5-English-PC.zip."""

import os
import sys
import time
import zipfile
from pathlib import Path


def package_pc_zip(pc_dir: Path, output_zip: Path) -> None:
    start = time.time()
    print(f"Creating {output_zip} from {pc_dir}...")
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    temp_zip = output_zip.with_suffix(".tmp.zip")

    count = 0
    total_uncompressed = 0
    with zipfile.ZipFile(temp_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for root, dirs, files in os.walk(pc_dir):
            for file in sorted(files):
                if file.endswith(".orig") or file.endswith(".tmp") or file.endswith(".bak"):
                    continue
                file_path = Path(root) / file
                arcname = file_path.relative_to(pc_dir).as_posix()
                z.write(file_path, arcname)
                total_uncompressed += file_path.stat().st_size
                count += 1
                print(f"  + {arcname} ({file_path.stat().st_size / (1024*1024):.2f} MB)")

    if temp_zip.exists():
        temp_zip.replace(output_zip)

    compressed_size = output_zip.stat().st_size
    duration = time.time() - start
    print(f"\nCreated {output_zip.name} with {count} files in {duration:.1f}s.")
    print(f"Uncompressed: {total_uncompressed / (1024*1024):.2f} MB -> Compressed: {compressed_size / (1024*1024):.2f} MB")


if __name__ == "__main__":
    pc_folder = Path("build/PC_PVZ-Fusion-4.0.5")
    zip_dest = Path("build/PvZ-Fusion-4.0.5-English-PC.zip")
    package_pc_zip(pc_folder, zip_dest)
