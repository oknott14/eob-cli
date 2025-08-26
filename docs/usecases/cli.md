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

## Design

The user can access the application from two places: `extract_eob.py` and `main.py`.

The `extract_eob.py` file will satisfy the basic functionality of passing only a file path and returning the extracted JSON data from EOB files. Alternatively, `main.py` will be the access point for the compiled application and will support a more robust feature set (see the nice to have requirements).

The CLI will use the python package [Typer](https://typer.tiangolo.com/) to easily create a reactive CLI with type hints, autocompletion, and more.

### Commands

#### Extracting EOB Data

To extract EOB data, run `python extract_eob.py --file {file_path_to_eob(s)}`.
