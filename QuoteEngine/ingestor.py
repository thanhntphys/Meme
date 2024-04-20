"""Quote import module."""
from typing import List

from .CsvIngestor import CsvIngestor
from .DocxIngestor import DocxIngestor
from .IngestorInterface import IngestorInterface
from .PdfIngestor import PdfIngestor
from .TxtIngestor import TxtIngestor
from .model import QuoteModel, InvalidFileFormat


class Ingestor(IngestorInterface):
    """Main ingestor class supporting multiple file types.

    This class supports the dynamic registration of new ingestors to
    handle additional file types as needed.
    """

    _ingestors = set()

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if there is any registered ingestor that can handle the file type of the given path.
        
        Args:
            path (str): The file path to check.
        
        Returns:
            bool: True if there is a supported ingestor for the file, False otherwise.
        """
        return any(ingestor.can_ingest(path) for ingestor in cls._ingestors)

    @classmethod
    def _parse(cls, path: str) -> List[QuoteModel]:
        """Attempt to parse a file using the appropriate registered ingestor.
        
        Args:
            path (str): The path of the file to parse.
        
        Returns:
            List[QuoteModel]: A list of QuoteModel instances extracted from the file.
        
        Raises:
            InvalidFileFormat: If no registered ingestor can handle the file format.
        """
        for ingestor in cls._ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise InvalidFileFormat(f"No registered ingestor can handle the file format: {path}")

    @classmethod
    def register(cls, ingestor: IngestorInterface):
        """Register a new type of ingestor.
        
        Args:
            ingestor (IngestorInterface): The ingestor class to register.
        """
        cls._ingestors.add(ingestor)

    @classmethod
    def deregister(cls, ingestor: IngestorInterface):
        """Deregister an existing ingestor type.
        
        Args:
            ingestor (IngestorInterface): The ingestor class to deregister.
        """
        cls._ingestors.discard(ingestor)

    @classmethod
    def register_defaults(cls):
        """Register default ingestor types for CSV, DOCX, PDF, and TXT files."""
        default_ingestors = (CsvIngestor, DocxIngestor, PdfIngestor, TxtIngestor)
        for ingestor in default_ingestors:
            cls.register(ingestor)
