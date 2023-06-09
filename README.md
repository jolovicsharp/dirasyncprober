# DirAsyncProber

DirAsyncProber is an asynchronous directory busting tool inspired by the popular "gobuster dir" command. It allows for fast and efficient enumeration of directories on web applications by leveraging the power of asynchronous programming in Python.

## Features

- Asynchronous directory busting for improved speed and efficiency.
- Customizable HTTP method, headers, cookies, and timeout options.
- Ability to search for specific status codes and file extensions.
- Expanded mode for printing full URLs for maximum detail.
- Follows redirects to avoid dead ends during enumeration.
- Optional TLS certificate verification for flexible usage.
- Provides content length information for discovered directories.
- Supports multi-threading with a configurable concurrency limit.

## Installation

As DirAsyncProber is not currently available on PyPI, you can manually install it by following these steps:

1. Clone this repository from GitHub
2. Navigate to the project directory : `cd dirasyncprober`
3. Install the required dependencies using pip : `pip install -r requirements.txt`

## Usage

`python3 dirasyncprober.py -u https://example.com -w wordlist.txt`

## Screenshot

![ApplicationScreenshot](screenshot.png)
