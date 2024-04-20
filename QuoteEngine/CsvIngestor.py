"""Csv parsing module."""
from typing import List
import pandas as pd
from .IngestorInterface import IngestorInterface
from .model import QuoteModel

class CsvIngestor(IngestorInterface):
    """Parse comma separated value files using pandas.

    This class inherits from the IngestorInterface and implements the parsing of CSV files
    to create a list of QuoteModel instances.
    """
    
    ext = ".csv"

    @classmethod
    def _parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a CSV file.

        Args:
            path (str): The file path of the CSV to parse.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances created from the CSV data.
        """
        try:
            data = pd.read_csv(path)
            quotes = data.apply(lambda row: QuoteModel(body=row['body'], author=row['author']), axis=1).tolist()
            return quotes
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty")
        except KeyError as e:
            raise ValueError(f"CSV file is missing required columns: {e}")

