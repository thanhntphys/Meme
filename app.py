"""Web app module for meme generation."""
import mimetypes
import random
import tempfile
from pathlib import Path

import requests
from flask import Flask, render_template, request

from MemeGenerator.engine import MemeEngine
from QuoteEngine.ingestor import Ingestor

app = Flask(__name__)
current_dir = Path(__file__).parent
meme_engine = MemeEngine(current_dir / "static")

def setup():
    """Load all resources and initialize meme generation assets."""
    Ingestor.register_defaults()
    quotes = Ingestor.scan(current_dir / "_data/DogQuotes")
    images = MemeEngine.find_images(current_dir / "_data/photos/dog")
    return quotes, images

quotes, images = setup()

@app.route("/")
def meme_rand():
    """Serve a randomly generated meme."""
    img = random.choice(images)
    quote = random.choice(quotes)
    meme_path = meme_engine.make_meme(img, quote.body, quote.author)
    return render_template("meme.html", path=Path(meme_path).relative_to(current_dir))

@app.route("/create", methods=["GET"])
def meme_form():
    """Render the form for users to create their own meme."""
    return render_template("meme_form.html")

@app.route("/create", methods=["POST"])
def meme_post():
    """Create and display a user-defined meme based on form input."""
    try:
        image_url = request.form.get("image_url")
        body = request.form.get("body")
        author = request.form.get("author")

        response = requests.get(image_url, allow_redirects=True)
        content_type = response.headers.get("content-type")
        extension = mimetypes.guess_extension(content_type)
        if not extension:
            return render_template("error.html", message="Unsupported content type: Please use an image URL.")

        with tempfile.NamedTemporaryFile(suffix=extension) as tmp:
            tmp.write(response.content)
            tmp.flush()  # Make sure all data is written
            meme_path = meme_engine.make_meme(tmp.name, body, author)
        return render_template("meme.html", path=Path(meme_path).relative_to(current_dir))
    except Exception as e:
        return render_template("error.html", message=str(e))


if __name__ == "__main__":
    app.run(debug=True)
