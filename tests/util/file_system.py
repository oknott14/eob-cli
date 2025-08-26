import shutil
from pathlib import Path
from typing import List

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_zip_file(temp_dir: Path, zip_file_path: Path):
    """
    Creates a dummy directory with PDF files, zips it, and then prepares
    for extraction testing.
    """
    # Create a temporary directory for the dummy PDF files
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Create a zip archive from the temporary directory
    # shutil.make_archive zips the content and gives it a .zip extension
    shutil.make_archive(
        str(zip_file_path.absolute()).removesuffix(zip_file_path.suffix),
        "zip",
        temp_dir,
    )


def create_test_files(dir: Path, type: str = "pdf", amount: int = 3):
    dir.mkdir(parents=True, exist_ok=True)
    paths: List[Path] = []
    for i in range(amount):
        paths.append((dir / f"document_{i}.{type}"))
        paths[-1].touch(exist_ok=True)
    return paths


def cleanup_dir(path: Path):
    # Clean up the temporary directory after zipping
    shutil.rmtree(path.absolute())
    

def write_to_pdf_file(pdf_path: Path, content: str = "Test Content"):
    """
    Creates a simple PDF file at the specified path and writes content to it.

    Args:
        pdf_path (Path): The path to the PDF file to create.
    """
    try:
        # Create a new canvas (the drawing surface for the PDF)
        c = canvas.Canvas(str(pdf_path), pagesize=letter)

        # Set font and size for the text
        c.setFont("Helvetica", 12)

        # Write some text at a specific coordinate (x, y)
        c.drawString(100, 750, content)

        # Save the PDF file
        c.save()

    except Exception as e:
        print(f"An error occurred while writing to the PDF: {e}")
