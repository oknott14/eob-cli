# File Reader

## Description

The File Reader will read files from the file system and convert them into LangChain documents.

## Functional Requirements

1. Reads one or more files based on a single file path.
2. Validates that the filepath points to a `.pdf` file or zip file of many `.pdf`s.
3. Reads the file(s) and converts the results to usable documents.
4. Files can be located anywhere in the file system.

## Technical Requirements

1. File(s) are read and stored as an array of Langchain Documents.
2. Zips are extracted and read as multiple files.

## Design

The File Reader will be a class that accepts a file path, validates it, and reads the PDF files from the path.
