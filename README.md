Meme Generator Project
======================
Welcome to the Meme Generator! This tool lets you create humorous memes by pairing randomly chosen quotes with images from a curated collection. Perfect for social media sharing, presentations, or just having a bit of fun, this project combines a simple web interface with a powerful command-line application for versatility and ease of use.

## Features
- Generate memes automatically or customize them with your own text and images.
- Easy to use web interface for on-the-fly meme creation.
- Command line tool for batch processing or automation tasks.

## How to build
o build the project, you will first need to have
Python installed. This was developed against Python
version `3.8.5`. You will also need `pip` and,
optionally, `virtualenv`.

All the commands in the below listings will be
assumed to be running in the same directory where
you found this `README`, unless otherwise specified.
I will also assume you are developing under Linux (I
used Ubuntu).

* Set up a virtual environment (optional - recommended)
```sh
$ python -m venv env
$ source  venv/bin/activate
```
* Lint code and docstrings
```sh
$ pip install flake8 flake8-docstrings
$ flake8
```
* Download dependencies and run tests
```sh
$ pip install -r requirements.txt
$ pytest
```
## How to run
* Generate a meme on the command line
```sh
$ python3 ./meme.py
```
this will return the path to a generated meme image.