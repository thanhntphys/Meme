"""Docx parsing module."""
import re
from typing import List

import docx
from docx import Document
from docx.opc.exceptions import PackageNotFoundError

from .IngestorInterface import IngestorInterface
from .model import QuoteModel, InvalidFileFormat


class DocxIngestor(IngestorInterface):
    """Parse Microsoft Word (.docx) file format using `python-docx`.
    
    This class implements the parsing of .docx files to extract text
    that matches the expected quote format: "quote text" - author.
    """

    ext = ".docx"
    quote_regex = re.compile(r'"([^"]+)" - (.+)')

    @classmethod
    def _parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a .docx file located at the specified path.
        
        Args:
            path (str): The file path of the .docx to parse.
        
        Returns:
            List[QuoteModel]: A list of QuoteModel instances extracted from the .docx.
        
        Raises:
            InvalidFileFormat: If the file is not accessible or corrupt, or if no quotes are found.
        """
        try:
            doc = Document(path)
        except PackageNotFoundError:
            raise InvalidFileFormat(f"The file at {path} could not be opened. It may be corrupt or not a .docx file.")

        quotes = [
            QuoteModel(body=m.group(1), author=m.group(2))
            for paragraph in doc.paragraphs
            for m in cls.quote_regex.finditer(paragraph.text)
        ]

        if not quotes:
            raise InvalidFileFormat(f"No quotes found in the .docx file at {path}. Please ensure the quotes are properly formatted.")

        return quotes

