# Simple-Web-Archiver
[![Screenshot of the tool's GUI.](https://raw.githubusercontent.com/ian-nai/Simple-Web-Archiver/master/gui_screenshot.png)


A simple, GUI web archiving tool in Python.


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

The GUI allows you to select whether you'd like to save the website's files locally, as WARCs, or both, and whether you'd like to download files solely from the website whose address you've entered or from external sites, as well (i.e., sites linked to from the address you've entered). Only enter the base URL for the site you'd like to capture (e.g., https://www.duckduckgo.com), and the tool will retrieve all of the pages and files of the site it can find, following links to download as much of the site as possible. 
