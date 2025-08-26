# Exctraction Chain

The extraction chain will handle the logic for extracting data from the provided EOB documents.

## High Level Overview

1. Validate Arguments
   1. Filepath is valid
1. Ingest Documents
   1. Extract Zip into a directory (if zip)
   1. Ingest PDF(s)
   1. Convert PDF(s) to LC documents
1. Pre-Processing
   1. Chunk Documents (probably)
   1. Remove unnecessary info
1. Data Extraction
1. Conversion to JSON (probably not)
1. Data Storage
