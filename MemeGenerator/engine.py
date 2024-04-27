"""Meme generator engine module."""
import os
import random
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from QuoteEngine.model import QuoteModel
from typing import List

class MemeEngine:
    """Meme generator engine that creates memes by superimposing quotes onto images."""

    text_margin = 10  # margin to prevent text sticking too close to the borders
    default_font = "./_data/fonts/FreeSans.ttf"
    default_font_size = 20

    def __init__(self, root: Path):
        """Initialize the meme generator engine with a directory to store output.
        
        Args:
            root (Path): The root directory where generated memes will be stored.
        """
        self.root = root
        os.makedirs(root, exist_ok=True)

    def _write_quote(self, img: Image, quote: QuoteModel, font_name: str, font_size: int):
        """Draw a quote on the image using the provided font settings.
        
        Args:
            img (Image): The image to draw the quote on.
            quote (QuoteModel): The quote model containing the text and author.
            font_name (str): The path to the font file.
            font_size (int): The size of the font.
        """
        quote_str = f'"{quote.body}" - {quote.author}'
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_name, font_size)
        bbox = draw.textbbox((0,0), quote_str, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = random.randint(self.text_margin, max(self.text_margin, img.width - text_width - self.text_margin))
        text_y = random.randint(self.text_margin, max(self.text_margin, img.height - text_height - self.text_margin))

        draw.text((text_x, text_y), quote_str, font=font, fill='white')

    def make_meme(self, img_path: Path, text: str, author: str, width: int = 500,
                  font_name: str = default_font, font_size: int = default_font_size) -> str:
        """Generate a meme from an image and a quote and save it to the root directory.
        
        Args:
            img_path (Path): Path to the source image.
            text (str): The quote text.
            author (str): The quote author.
            width (int): Desired width of the meme image.
            font_name (str): Font file to use for the quote text.
            font_size (int): Size of the quote text.
        
        Returns:
            str: The file path of the generated meme.
        
        Raises:
            ValueError: If the image file cannot be opened or processed.
        """
        try:
            with Image.open(img_path) as img:
                ratio = img.height / img.width
                new_height = int(ratio * width)
                resized = img.resize((width, new_height))
                self._write_quote(resized, QuoteModel(text, author), font_name, font_size)
                meme_path = tempfile.mktemp(dir=self.root, prefix="meme-", suffix=".jpg")
                resized.save(meme_path)
                return meme_path
        except FileNotFoundError:
            raise ValueError(f"The image file {img_path} does not exist.")
        except UnidentifiedImageError:
            raise ValueError("The provided file is not a valid image.")

    @staticmethod
    def find_images(path: Path, img_ext: str = ".jpg") -> List[Path]:
        """Recursively find and return paths to images within a directory matching the specified extension.
        
        Args:
            path (Path): Directory path to search for images.
            img_ext (str): Image file extension to look for.
        
        Returns:
            List[Path]: A list of paths to images that match the specified extension.
        """
        img_ext = img_ext.lower()
        return [Path(root) / file for root, _, files in os.walk(path) for file in files if file.lower().endswith(img_ext)]
