#!/usr/bin/env python3

import os
import sys
import hashlib
import argparse
from functools import partial

def get_file_hash(filename, hasher=hashlib.sha256, chunk_size=4096):
    d = hasher()
    try:
        with open(filename, mode='rb') as fh:
            for buf in iter(partial(fh.read, chunk_size), b''):
                d.update(buf)
    except Exception as e:
        print(f"Error processing file {filename}: {e}", file=sys.stderr)
        return None
    return d.hexdigest()

def build_hash_tree(directory, follow_symlinks=False, use_names=False, hasher=hashlib.sha256):
    files_dict = {}
    for root, dirs, files in os.walk(directory, topdown=True, followlinks=follow_symlinks):
        for filename in files:
            path = os.path.join(root, filename)
            if not follow_symlinks and os.path.islink(path):
                continue
            rel_path = os.path.relpath(path, directory)
            if os.path.getsize(path) == 0:
                key = get_file_hash(path, hasher) + "-" + rel_path if not use_names else rel_path
            else:
                key = get_file_hash(path, hasher) if not use_names else rel_path
            if key is not None:
                files_dict[key] = path
    return files_dict

def find_missing_files(srces, dests, follow_symlinks=False, use_names=False, hasher=hashlib.sha256):
    src_tree = {directory: build_hash_tree(directory, follow_symlinks, use_names, hasher) for directory in srces}
    dest_tree = {directory: build_hash_tree(directory, follow_symlinks, use_names, hasher) for directory in dests}
    missing = []
    for src_dir, src_files in src_tree.items():
        for key, src_path in src_files.items():
            found = any(key in dest_files for dest_files in dest_tree.values())
            if not found:
                missing.append((src_path, key))
    return missing

def run():
    parser = argparse.ArgumentParser(description="Checks whether every file from the source directories exists in the destination directories.")
    parser.add_argument("src", nargs='+', help="Source directory(ies).")
    parser.add_argument("dest", nargs='+', help="Destination directory(ies).")
    parser.add_argument("--follow-symlinks", action='store_true', help="Follow symbolic links when scanning files.")
    parser.add_argument("--use-names", action='store_true', help="Use file names instead of checksums for comparison.")
    args = parser.parse_args()

    missing = find_missing_files(args.src, args.dest, args.follow_symlinks, args.use_names)
    if missing:
        print("Missing files found:")
        for path, key in missing:
            print(f"Identifier: {key}, Path: {path}")
    else:
        print("No missing files found.")

if __name__ == "__main__":
    run()


