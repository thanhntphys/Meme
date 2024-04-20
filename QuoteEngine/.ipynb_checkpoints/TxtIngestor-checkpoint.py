"""Txt parsing module."""
from typing import List

from .IngestorInterface import IngestorInterface
from .model import QuoteModel


class TxtIngestor(IngestorInterface):
    """Parse plain text files to extract quotes.

    This class parses files with a '.txt' extension, looking for lines that contain quotes in the
    format 'QuoteBody - QuoteAuthor'.
    """

    ext = ".txt"

    @classmethod
    def _parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a plain text file.

        Args:
            path (str): The path to the text file to parse.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances representing the parsed quotes.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            IOError: If there is an error reading the file.
            ValueError: If a line is found without the expected ' - ' separator.
        """
        quotes = []
        try:
            with open(path, "r", encoding="utf-8-sig") as file:
                for line in file:
                    if " - " in line:
                        try:
                            body, author = line.strip().split(" - ", 1)
                            quotes.append(QuoteModel(body=body, author=author))
                        except ValueError:
                            raise ValueError(f"Format error in line: {line.strip()}. Expected 'QuoteBody - QuoteAuthor'.")
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {path} does not exist.")
        except IOError as e:
            raise IOError(f"Error reading {path}: {str(e)}")

        return quotes
