"""Command line meme generator module."""
import argparse
import random
import tempfile
from pathlib import Path

from MemeGenerator.engine import MemeEngine
from QuoteEngine.ingestor import Ingestor
from QuoteEngine.model import QuoteModel

def generate_meme(path: Path = None, body: str = None, author: str = None) -> str:
    """Generate a meme given a path and a quote.
    
    Args:
        path (Path): The path to the image file.
        body (str): Quote text for the meme.
        author (str): Author of the quote.

    Returns:
        str: The path to the generated meme.

    Raises:
        ValueError: If body is provided but author is missing.
    """
    if path is None:
        imgs = MemeEngine.find_images(Path(__file__).parent / "_data/photos/dog/")
        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        Ingestor.register_defaults()
        quotes = Ingestor.scan(Path(__file__).parent / "_data/DogQuotes")
        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError("Author required if body is specified")
        quote = QuoteModel(body, author)

    meme_engine = MemeEngine(tempfile.mkdtemp(prefix="memes-"))
    meme_path = meme_engine.make_meme(img, quote.body, quote.author)
    return meme_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a meme.")
    parser.add_argument("--path", type=Path, help="Path to an image to use.")
    parser.add_argument("--body", help="Quote text for the meme.")
    parser.add_argument("--author", help="Author of the quote.")
    args = parser.parse_args()

    try:
        meme_path = generate_meme(args.path, args.body, args.author)
        print(f"Meme created at: {meme_path}")
    except Exception as e:
        print(f"Error: {e}")
