# CLI

The CLI defines two command line functions that assist in processing EOB files: `process-eob` and `zip`.

## Process EOB Command

The `process-eob` command is a function within the CLI that extracts data from Explanation of Benefits (EOB) documents. It is designed to process either a single PDF file or a .zip archive containing multiple EOB PDFs, converting the extracted information into JSON format.

### Usage

To run this command, run one of the following commands from the project directory in your terminal:

1. `python main.py process-eob --file <path_to_file> [OPTIONS]`
2. `python extract_eob.py --file <path_to_file> [OPTIONS]`

_Note_: If you are using _UV_ as a package manager, you can also use `uv run <python_file_name> --file <<path_to_file>`

### Arguments and Options

**file (-f)**

This is a required argument that specifies the path to the EOB document(s). It accepts either a single PDF file or a .zip file containing multiple PDF documents.

_Syntax_: --file or -f

_Type_: str (string)

_Description_: The absolute file path to the EOB PDF or a .zip archive.

**output_dir (-o)**

This is an optional argument that specifies a directory to save the output JSON files. If not provided, the files will be saved in the same directory as the input file.

_Syntax_: --output or -o

_Type_: Optional[str] (optional string)

_Description_: The output directory for the extracted JSON files.

**overwrite (-ov)**

This is a flag that, when specified, allows the command to overwrite existing output files in the output_dir. This option is ignored if an output_dir is not provided.

_Syntax_: --overwrite or -ov

_Type_: bool (boolean)

_Description_: Whether to overwrite existing files in the output directory.

**temperature (-t)**

This is an optional argument that controls the randomness of the Language Model (LLM) used for data extraction. A lower value (closer to 0) makes the output more deterministic and focused, while a higher value (closer to 1) results in more creative or varied output. The default value is 0.4.

_Syntax_: --temperature or -t

_Type_: float (floating-point number)

_Description_: The temperature setting for the LLM.

**unzipTo (-z)**

This is an optional argument that specifies a directory to unzip the contents of a provided .zip file. If not provided, the files will be unzipped to a temporary directory.

_Syntax_: --unzipTo or -z

_Type_: Optional[str] (optional string)

_Description_: The directory to extract the contents of a .zip file.

### Examples

Processing a single PDF and saving to a specified output directory:

`python main.py process-eob --file /path/to/my_eob.pdf --output /path/to/json_files`

Processing a .zip file and allowing output files to be overwritten:

`python main.py process-eob -f /path/to/my_eobs.zip -o /path/to/output_dir -ov`

Processing a .zip file with a custom temperature and specifying the unzip location:

`python main.py process-eob --file /path/to/my_eobs.zip --unzipTo /temp/unzip_location --temperature 0.8`

## Zip

The zip command creates a compressed .zip archive of a specified directory.

### Usage

To run this command, you will use the following structure in your terminal:

`python main.py zip <source> <dest>`

### Arguments and Options

**source**

This is a required argument that specifies the directory to be zipped.

_Syntax_: source

_Type_: str (string)

_Description_: The absolute path to the directory you wish to compress.

**dest**

This is a required argument that specifies the location where the .zip file will be created.

_Syntax_: dest

_Type_: str (string)

_Description_: The absolute path to the directory where the output .zip file will be saved.

### Examples

Compressing a directory and saving the .zip file to another directory:

`python main.py zip /path/to/my_documents /path/to/my_archives`
