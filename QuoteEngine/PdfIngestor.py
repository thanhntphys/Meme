"""Pdf parsing module."""
import os
import re
import subprocess
import tempfile
from typing import List

from .IngestorInterface import IngestorInterface
from .model import QuoteModel


class PdfIngestor(IngestorInterface):
    """Parse PDF files using pdftotext via the command line.

    This class uses the external 'pdftotext' tool to convert PDF documents to plain text and then
    extracts quotes using a predefined regex pattern.
    """

    ext = ".pdf"
    quote_regex = re.compile(r'"([^"]+)" - (.+)')

    @classmethod
    def _parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a PDF file.

        Args:
            path (str): The file path of the PDF to parse.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances extracted from the PDF.

        Raises:
            FileNotFoundError: If the 'pdftotext' tool is not installed or found.
            Exception: If the 'pdftotext' tool fails to run or other IO errors occur.
        """
        _, temp_file = tempfile.mkstemp(suffix=cls.ext)
        try:
            # Attempt to convert PDF to text
            subprocess.run(["pdftotext", path, temp_file], check=True)
            with open(temp_file, "r") as file_handle:
                content = file_handle.read()
            return [
                QuoteModel(body=match.group(1), author=match.group(2))
                for match in cls.quote_regex.finditer(content)
            ]
        except subprocess.CalledProcessError:
            raise Exception(f"Failed to convert PDF file: {path}")
        finally:
            # Ensure the temporary file is removed after processing
            os.remove(temp_file)
