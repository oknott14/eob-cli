# CLI Interface

## Description

The CLI interface is how users interact with the Explanation of Benefits data extraction tool.

## Functional Requirements

1. Runnable from any command line interface
2. User can specify a path to a `.pdf` file or zip file of many `.pdf`s
3. CLI tool extracts structured JSON data from provided files

### Nice to Haves

1. User can specify an output file / folder to write the JSON output to
2. User can specify verbos / non-verbose logging

## Technical Requirements

1. CLI tool can be run by calling `python extract_eob.py` from the project directory
2. The `--file` argument allows the user to specify the path to EOB files.
3. The CLI will only read `.pdf` files from the specified file location.
