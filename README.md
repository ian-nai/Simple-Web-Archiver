# Simple-Web-Archiver
A simple, GUI web archiving tool in Python. Pages can be downloaded as files (HTML, CSS, etc) or as WARCs. Images from the pages can also be downloaded.
<p align="center">
  <img src="https://raw.githubusercontent.com/ian-nai/Simple-Web-Archiver/master/gui_example.png?token=AFOEH7TUZUUTVDJTTMBFKNK623AE2" alt="Screenshot of the tool's GUI."/>
</p>

## Why Use This?
This tool is intended to serve as a simple self-archiving program that is accessible to users with limited technical knowledge. Using the program allows users to quickly and easily download local archives of websites without learning curve of prior technical knowlege related to web archiving. 

## Getting Started

Download the project above, then unzip the file. In your terminal, navigate to the project folder and install the requirements:

```
pip3 install -r requirements.txt
```

Then type the following to open up the GUI:

```
pip3 install simple_web_archiver.py
```

## Usage

The GUI allows you to select whether you'd like to save the website's files locally, as WARCs, or both, and whether you'd like to download files solely from the website whose address you've entered or from external sites, as well (i.e., sites linked to from the address you've entered). Only enter the base URL for the site you'd like to capture (e.g., https://www.duckduckgo.com), click "Download Archive," and the tool will retrieve all of the pages and files of the site it can find, following links to download as much of the site as possible. 

To download files from a limited scope of the website, use the second text entry box to enter your specified base URL (e.g., https://www.duckduckgo.com/test/), enter the delimiting term you'd like all URLs to share (e.g., "test" would download all links from the link above)and click "Download Limited Archive." This will only download links beginning with that prefix, or external links found on pages with that base URL.

Select "Save Images" to download images from the scope you've selected (i.e., local only or both local and eternal).
