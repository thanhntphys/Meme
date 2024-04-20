from collections import namedtuple

# Define a namedtuple for QuoteModel
QuoteModel = namedtuple('QuoteModel', ['body', 'author'])

def __str__(self):
    """Return the string representation."""
    return f'"{self.body}" - {self.author}'

# Attach the __str__ method to QuoteModel
QuoteModel.__str__ = __str__

class InvalidFileFormat(Exception):
    """Raised when a file with the wrong extension is passed to an ingestor."""
    pass
