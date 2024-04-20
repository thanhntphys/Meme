"""Ingestor interface module."""
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from .model import QuoteModel, InvalidFileFormat


class IngestorInterface(ABC):
    """Base interface to parse quotes from files.
    
    Attributes:
        ext (str): Supported file extension (must include leading dot).
    """

    ext: str = None

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check whether this ingestor supports the input file's extension.
        
        Args:
            path (str): Path to the file to be checked.
        
        Returns:
            bool: True if the file extension is supported, False otherwise.
        """
        return Path(path).suffix == cls.ext

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the input file if supported.
        
        Args:
            path (str): Path to the file to be parsed.
        
        Returns:
            List[QuoteModel]: List of parsed QuoteModel instances.
        
        Raises:
            InvalidFileFormat: If the file format is not supported.
        """
        if not cls.can_ingest(path):
            raise InvalidFileFormat(f"Cannot ingest file with unsupported format: {path}")
        return cls._parse(path)

    @classmethod
    def scan(cls, directory_path: str) -> List[QuoteModel]:
        """Scan a directory (including subfolders) and parse all supported files for quotes.
        
        Args:
            directory_path (str): Directory path to scan for files.
        
        Returns:
            List[QuoteModel]: List of all quotes found in the directory.
        """
        quotes = []
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                file_path = Path(root) / file_name
                if cls.can_ingest(file_path):
                    quotes.extend(cls.parse(file_path))
        return quotes

    @classmethod
    @abstractmethod
    def _parse(cls, path: str) -> List[QuoteModel]:
        """Define format-specific parsing logic.
        
        Args:
            path (str): Path to the file to be parsed.
        
        Returns:
            List[QuoteModel]: List of parsed QuoteModel instances.
        
        Raises:
            NotImplementedError: If the child class does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement the _parse method")
