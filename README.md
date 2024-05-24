# CopyVerifier

`CopyVerifier` is a Python tool designed to ensure that files copied or mirrored between directories are complete and unaltered. This tool uses SHA-256 checksums or file names to verify that all files in a source directory exist in a target directory without changes.

## Features

- **Checksum Verification:** Uses SHA-256 hashes to verify files.
- **Name-Based Comparison:** Optionally compare files based on their names.
- **Empty File Handling:** Unique identification for empty files to ensure they are tracked correctly.
- **Cross-Platform:** Works on any system that supports Python.
- **Open Source:** Freely usable and modifiable under the MIT License.

## Getting Started

### Prerequisites

- Python 3.2 or higher

### Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/CopyVerifier.git
cd CopyVerifier
```

### Usage

Run the script from the command line:
```bash
python copyverifier.py --src [source directory] --dest [destination directory] [options]
```

Options:

* `--follow-symlinks: Follow symbolic links.`
* `--use-names: Compare files based on their names instead of checksums.`


### Contributing

Contributions are welcome!

### License

This project is licensed under the MIT License - see the LICENSE file for details.
