import tkinter as tk
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import os
import pathlib
import json
import subprocess
import shutil

root = tk.Tk()

root.title('Simple Web Archiver')

canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

filename_errors = 0

def on_entry_click(event):
    if entry1.get() == 'Enter your URL...':
       entry1.delete(0, "end")
       entry1.insert(0, '') 
       entry1.config(fg = 'black')
def on_focusout(event):
    if entry1.get() == '':
        entry1.insert(0, 'Enter your URL...')
        entry1.config(fg = 'black')
        
links_list = []


label_entry1 = tk.Label(root, text= 'Save Entire Website:')
canvas1.create_window(200, 115, window=label_entry1)

label_entry2 = tk.Label(root, text= 'Save Limited Scope:')
canvas1.create_window(200, 180, window=label_entry2)

entry1 = tk.Entry (root) 

entry1.insert(0, 'https://www.example.com')
entry1.bind('<FocusIn>', on_entry_click)
entry1.bind('<FocusOut>', on_focusout)
entry1.config(fg = 'black')

canvas1.create_window(200, 140, window=entry1)

entry2 = tk.Entry (root) 

entry2.insert(0, 'https://example.com/test/')
entry2.bind('<FocusIn>', on_entry_click)
entry2.bind('<FocusOut>', on_focusout)
entry2.config(fg = 'black')

canvas1.create_window(200, 205, window=entry2)


def getLimitedScope():

    url3 = entry2.get()
    
    html_page2 = requests.get(url3).text
    soup2 = BeautifulSoup(html_page2, 'html.parser')
    links2 = []
    img_links = []
    
    
    for link in BeautifulSoup(html_page2, parse_only=SoupStrainer('a'), features="html.parser"):
       if link.has_attr('href'):
           links2.append(link['href'])
       
 
  
    
    for link in soup2.find_all('link', href=True):
         links2.append(link['href'])
    
    links3 = []
    for x in links2:
        if "http" in x:
            continue
        elif "mailto" in x:
            continue
        else:
            links3.append(x)
    
    external_links2 = []
    for x in links2:
        if "http" in x:
            external_links2.append(x)
        elif "mailto" in x:
            continue
        else:
             continue
    print('external links: ', external_links2)
               
    linkslist33 = []
    
    for x in links3:
        url44 = (url3 + str(x))
        linkslist33.append(url44)
    
    print(linkslist33)
    
    
    limited_urls = [s for s in linkslist33 if url3 in s]
    
    if (var5.get() == 1):
        img_tags = (soup2.findAll('img'))
        for im in img_tags:
            img_links.append(im['src'])
        for x in limited_urls:
            html_page3 = requests.get(x).text
            soup3 = BeautifulSoup(html_page3, 'html.parser')
            img_tags2 = (soup3.findAll('img'))
            for im in img_tags2:
                img_links.append(im['src'])
    
        
    print('URLs: ', limited_urls)
   
     # ~~~ button stuff ~~~
    
    # save images
    if (var5.get() == 1):
        for x in img_links:
            sep = '?AWSAccessKeyId'
            img_filename = x.split(sep, 1)[0]

            if img_filename.startswith('http'):
                img_a = img_filename.replace('http', '')
            if img_filename.startswith('https'):
                img_a = img_filename.replace('https', '')
                img_c = img_a.strip(':')
                img_d = img_c.replace('/','_')
            if '.jpg' in img_d:
                img_e = img_d.split("?",1)[0] 


            r = requests.get(x, stream = True)
            
            if r.status_code == 200:
                r.raw.decode_content = True
    
    
            with open(img_d,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                
    # save html of local pages        
    if (var1.get() == 1) & (var2.get() == 0):
        if (var3.get() == 1) & (var4.get() == 0) or (var3.get() == 0) & (var4.get() == 0):
            for x in limited_urls:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                        d[:255]
                    open(d, 'wb').write(r.content) 
                else:
                    if len(d) > 250:
                        d[:250]
                    open(e, 'wb').write(r.content) 
                    
        # WARC only for local files
        elif (var3.get() == 0) & (var4.get() == 1):
            for x in limited_urls:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                        d[:255]
                    open(d, 'wb').write(r.content)      
                else:
                    if len(d) > 240:
                        d[:240]
                    open(d, 'wb').write(r.content)  
                    subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])
                    
        # HTML and WARC for local files
        else:
              for x in limited_urls:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                     if len(d) > 255:
                        d[:255]
                     open(d, 'wb').write(r.content)      
                else:
                    if len(d) > 240:
                        d[:240]
                    open(d, 'wb').write(r.content)  
                    subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])
                    
    # html, external only                
    elif (var1.get() == 0) & (var2.get() == 1):
        if (var3.get() == 1) & (var4.get() == 0):
            for x in external_links2:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                     if len(d) > 255:
                        d[:255]
                     open(d, 'wb').write(r.content) 
                else:
                    if len(d) > 250:
                        d[:250]
                    open(e, 'wb').write(r.content) 
                
        # warc, external only
        if (var3.get() == 0) & (var4.get() == 1):
             for x in external_links2:
                  r = requests.get(x, allow_redirects=True)
                  if x.startswith('http'):
                      a = x.replace('http', '')
                  if x.startswith('https'):
                      a = x.replace('https', '')
                      c = a.strip(':')
                      d = c.replace('/','_')
                      e = (d + '.html')
                  if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                      '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                      '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                      '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                      '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                      '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                      '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                      '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                      '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                      if len(d) > 255:
                          d[:255]
                      open(d, 'wb').write(r.content)      
                  else:
                      if len(d) > 240:
                          d[:240]
                      open(d, 'wb').write(r.content)  
                      subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])   
                      
        if (var3.get() == 1) & (var4.get() == 1):                    
                for x in external_links2:
                     r = requests.get(x, allow_redirects=True)
                     if x.startswith('http'):
                         a = x.replace('http', '')
                     if x.startswith('https'):
                         a = x.replace('https', '')
                         c = a.strip(':')
                         d = c.replace('/','_')
                         e = (d + '.html')
                     if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                         '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                         '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                         '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                         '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                         '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.sh', '.swift', '.vb', '.ods',
                         '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                         '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                         '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                         if len(d) > 255:
                             d[:255]
                         open(d, 'wb').write(r.content) 
                     else:
                         if len(d) > 240:
                             d[:240]
                         open(e, 'wb').write(r.content)
                         subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])     
                  
    # local and external
    elif (var1.get() == 1) & (var2.get() == 1):
        # if html only
        if (var3.get() == 1) & (var4.get() == 0):
            for x in limited_urls:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content) 
                else:
                    if len(d) > 250:
                             d[:250]
                    open(e, 'wb').write(r.content)
        
            for x in external_links2:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content)
                else:
                    if len(d) > 250:
                             d[:250]
                    open(e, 'wb').write(r.content)
                
        # warc only for local and external
        if (var3.get() == 0) & (var4.get() == 1):
             for x in limited_urls:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content)
                else:
                    if len(d) > 240:
                             d[:240]
                    subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])
                
                    
             for x in external_links2:
                  r = requests.get(x, allow_redirects=True)
                  if x.startswith('http'):
                      a = x.replace('http', '')
                  if x.startswith('https'):
                      a = x.replace('https', '')
                      c = a.strip(':')
                      d = c.replace('/','_')
                      e = (d + '.html')
                  if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                      '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                      '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                      '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                      '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                      '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                      '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                      '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                      '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                      if len(d) > 255:
                             d[:255]
                      open(d, 'wb').write(r.content)
                  else:
                      if len(d) > 240:
                             d[:240]
                      subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])   
                      
        if (var3.get() == 1) & (var4.get() == 1):
                for x in limited_urls:
                     r = requests.get(x, allow_redirects=True)
                     if x.startswith('http'):
                         a = x.replace('http', '')
                     if x.startswith('https'):
                         a = x.replace('https', '')
                         c = a.strip(':')
                         d = c.replace('/','_')
                         e = (d + '.html')
                     if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                         '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                         '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                         '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                         '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                         '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                         '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                         '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                         '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                         if len(d) > 255:
                             d[:255]
                         open(d, 'wb').write(r.content)
                     else:
                        if len(d) > 240:
                             d[:240]
                        open(e, 'wb').write(r.content)
                        subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])
                
                    
                for x in external_links2:
                     r = requests.get(x, allow_redirects=True)
                     if x.startswith('http'):
                         a = x.replace('http', '')
                     if x.startswith('https'):
                         a = x.replace('https', '')
                         c = a.strip(':')
                         d = c.replace('/','_')
                         e = (d + '.html')
                     if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                         '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                         '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                         '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                         '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                         '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.sh', '.swift', '.vb', '.ods',
                         '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                         '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                         '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                         if len(d) > 255:
                             d[:255]
                         open(d, 'wb').write(r.content)
                     else:
                         if len(d) > 240:
                             d[:240]
                         open(e, 'wb').write(r.content)
                         subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])     
                         
    elif (var1.get() == 0) & (var2.get() == 0):
        print('error! please select an option')
        
    else:
        print('error! please select an option')   
        

    if (var1.get() == 0) & (var2.get() == 0):
        pass
    else: 
        label1 = tk.Label(root, text= 'Archive Saved!')
        canvas1.create_window(200, 230, window=label1)
   
  
def getFullSite():  

    # The commented code below can be edited to return base urls split by slashes, rather than by using the regex expression in the uncommented code
    
    url2 = entry1.get()
    
    html_page = requests.get(url2).text
    soup = BeautifulSoup(html_page, 'html.parser')
    links = []
    img_links = []
    
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url2)
    print("Urls: ", urls)
    
    #Segments = url2.rpartition('/')
    
    Segments = re.findall('^(?:\w+://)?.*?(?::\d+)?(?=/|$)', url2)
    #base_url = Segments[0]
    base_url = Segments[0]
    print(base_url)


    for link in BeautifulSoup(html_page, parse_only=SoupStrainer('a'), features="html.parser"):
       if link.has_attr('href'):
           #print(link['href'])
           links_list.append(link['href'])
       
 
    
    for link in soup.find_all('link', href=True):
         links_list.append(link['href'])
    
    links_list2 = []
    for x in links_list:
        if "http" in x:
            continue
        elif "mailto" in x:
            continue
        else:
            links_list2.append(x)
    
    external_links = []
    for x in links_list:
        if "http" in x:
            external_links.append(x)
        elif "mailto" in x:
            continue
        else:
             continue
    print('external links: ', external_links)
               
    linkslist3 = []
    
    for x in links_list2:
        url4 = (base_url + str(x))
        linkslist3.append(url4)
    
    if (var5.get() == 1):
        img_tags = (soup.findAll('img'))
        for im in img_tags:
            img_links.append(im['src'])
        for x in linkslist3:
            html_page3 = requests.get(x).text
            soup3 = BeautifulSoup(html_page3, 'html.parser')
            img_tags2 = (soup3.findAll('img'))
            for im in img_tags2:
                img_links.append(im['src'])
   
     # ~~~ button stuff ~~~
     
    # save images
    if (var5.get() == 1):
        for x in img_links:
            sep = '?AWSAccessKeyId'
            img_filename = x.split(sep, 1)[0]

            if img_filename.startswith('http'):
                img_a = img_filename.replace('http', '')
            if img_filename.startswith('https'):
                img_a = img_filename.replace('https', '')
                img_c = img_a.strip(':')
                img_d = img_c.replace('/','_')
            if '.jpg' in img_d:
                img_e = img_d.split("?",1)[0] 


            r = requests.get(x, stream = True)
            
            if r.status_code == 200:
                r.raw.decode_content = True
    
    
            with open(img_d,'wb') as f:
                shutil.copyfileobj(r.raw, f)
 
    
    # save html of local pages
    if (var1.get() == 1) & (var2.get() == 0):
        if (var3.get() == 1) & (var4.get() == 0) or (var3.get() == 0) & (var4.get() == 0):
            for x in linkslist3:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content)
                else:
                    if len(d) > 250:
                             d[:250]
                    open(e, 'wb').write(r.content)
                    
        # WARC only for local files
        elif (var3.get() == 0) & (var4.get() == 1):
            for x in linkslist3:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content)
                else:
                    if len(d) > 240:
                             d[:240]
                    subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])
                    
        # HTML and WARC for local files
        else:
              for x in linkslist3:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content)
                else:
                    if len(d) > 240:
                             d[:240]
                    open(e, 'wb').write(r.content)
                    subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])
                    
    # html, external only                
    elif (var1.get() == 0) & (var2.get() == 1):
        if (var3.get() == 1) & (var4.get() == 0):
            for x in external_links:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content)
                else:
                    if len(d) > 250:
                             d[:250]
                    open(e, 'wb').write(r.content)
                
        # warc, external only
        if (var3.get() == 0) & (var4.get() == 1):
             for x in external_links:
                  r = requests.get(x, allow_redirects=True)
                  if x.startswith('http'):
                      a = x.replace('http', '')
                  if x.startswith('https'):
                      a = x.replace('https', '')
                      c = a.strip(':')
                      d = c.replace('/','_')
                      e = (d + '.html')
                  if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                      '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                      '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                      '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                      '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                      '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                      '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                      '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                      '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                      if len(d) > 255:
                             d[:255]
                      open(d, 'wb').write(r.content)
                  else:
                      if len(d) > 240:
                             d[:240]
                      subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])   
                      
        if (var3.get() == 1) & (var4.get() == 1):                    
                for x in external_links:
                     r = requests.get(x, allow_redirects=True)
                     if x.startswith('http'):
                         a = x.replace('http', '')
                     if x.startswith('https'):
                         a = x.replace('https', '')
                         c = a.strip(':')
                         d = c.replace('/','_')
                         e = (d + '.html')
                     if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                         '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                         '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                         '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                         '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                         '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.sh', '.swift', '.vb', '.ods',
                         '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                         '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                         '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                         if len(d) > 255:
                             d[:255]
                         open(d, 'wb').write(r.content)
                     else:
                         if len(d) > 240:
                             d[:240]
                         open(e, 'wb').write(r.content)
                         subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])     
                  
    # local and external
    elif (var1.get() == 1) & (var2.get() == 1):
        # if html only
        if (var3.get() == 1) & (var4.get() == 0):
            for x in linkslist3:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content)
                else:
                    if len(d) > 250:
                             d[:250]
                    open(e, 'wb').write(r.content)
        
            for x in external_links:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                    e = (d + '.html')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content)
                else:
                    if len(d) > 250:
                             d[:250]
                    open(e, 'wb').write(r.content)
                
        # warc only for local and external
        if (var3.get() == 0) & (var4.get() == 1):
             for x in linkslist3:
                r = requests.get(x, allow_redirects=True)
                if x.startswith('http'):
                    a = x.replace('http', '')
                if x.startswith('https'):
                    a = x.replace('https', '')
                    c = a.strip(':')
                    d = c.replace('/','_')
                if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                    '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                    '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                    '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                    '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                    '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                    '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                    '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                    '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                    if len(d) > 255:
                             d[:255]
                    open(d, 'wb').write(r.content)
                else:
                    if len(d) > 240:
                             d[:240]
                    subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])
                
                    
             for x in external_links:
                  r = requests.get(x, allow_redirects=True)
                  if x.startswith('http'):
                      a = x.replace('http', '')
                  if x.startswith('https'):
                      a = x.replace('https', '')
                      c = a.strip(':')
                      d = c.replace('/','_')
                      e = (d + '.html')
                  if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                      '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                      '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                      '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                      '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                      '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                      '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                      '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                      '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                      if len(d) > 255:
                             d[:255]
                      open(d, 'wb').write(r.content)
                  else:
                      if len(d) > 240:
                             d[:240]
                      subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])   
                      
        if (var3.get() == 1) & (var4.get() == 1):
                for x in linkslist3:
                     r = requests.get(x, allow_redirects=True)
                     if x.startswith('http'):
                         a = x.replace('http', '')
                     if x.startswith('https'):
                         a = x.replace('https', '')
                         c = a.strip(':')
                         d = c.replace('/','_')
                         e = (d + '.html')
                     if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                         '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                         '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                         '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                         '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                         '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb', '.ods',
                         '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                         '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                         '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                         if len(d) > 255:
                             d[:255]
                         open(d, 'wb').write(r.content)
                     else:
                        if len(d) > 240:
                             d[:240]
                        open(e, 'wb').write(r.content)
                        subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])
                
                    
                for x in external_links:
                     r = requests.get(x, allow_redirects=True)
                     if x.startswith('http'):
                         a = x.replace('http', '')
                     if x.startswith('https'):
                         a = x.replace('https', '')
                         c = a.strip(':')
                         d = c.replace('/','_')
                         e = (d + '.html')
                     if x.endswith(('.aif', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.7z', 
                         '.pkg', '.rar', '.tar.gz', '.zip', '.bin', '.dmg', '.iso', '.csv', '.dat', '.db', '.log',
                         '.sql', '.tar', '.xml', '.bat', '.bin', '.exe', '.jar', '.py', '.otf', '.ttf', '.ai', '.bmp',
                         '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx',
                         '.cer', '.css', '.js', '.jsp', '.part', '.php', '.rss', '.key', '.odp', '.pps',
                         '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.sh', '.swift', '.vb', '.ods',
                         '.xls', '.xls', '.xlsm', '.xlsx', '.bak', '.cfg', '.dmp', '.drv', '.ini', '.tmp', '.3g2', '3gp', '.avi',
                         '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx',
                         '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd')):
                         if len(d) > 255:
                             d[:255]
                         open(d, 'wb').write(r.content)
                     else:
                         if len(d) > 240:
                             d[:240]
                         open(e, 'wb').write(r.content)
                         subprocess.run(['sudo', 'wget', x, ('--warc-file=' + d)])     
                         
    elif (var1.get() == 0) & (var2.get() == 0):
        print('error! please select an option')
        
    else:
        print('error! please select an option')   
        

    if (var1.get() == 0) & (var2.get() == 0):
        pass
    else: 
        label1 = tk.Label(root, text= 'Archive Saved!')
        canvas1.create_window(200, 230, window=label1)

        
var1 = tk.IntVar()
var2 = tk.IntVar()

c1 = tk.Checkbutton(root, text='Save Local Pages',variable=var1, onvalue=1, offvalue=0)
c1.select()
c1.pack()
c2 = tk.Checkbutton(root, text='Save External Pages',variable=var2, onvalue=1, offvalue=0)
c2.pack()

#warc buttons
var3 = tk.IntVar()
var4 = tk.IntVar()

c3 = tk.Checkbutton(root, text='Save Pages as HTML',variable=var3, onvalue=1, offvalue=0)
c3.select()
c3.pack()
c4 = tk.Checkbutton(root, text='Save WARCs',variable=var4, onvalue=1, offvalue=0)
c4.pack()

var5 = tk.IntVar()
c5 = tk.Checkbutton(root, text='Save Images',variable=var5, onvalue=1, offvalue=0)
c5.pack()
    
    
button1 = tk.Button(text='Download Archive', command=getFullSite)
canvas1.create_window(200, 245, window=button1)

button2 = tk.Button(text='Download Limited Archive', command=getLimitedScope)
canvas1.create_window(200, 270, window=button2)

root.mainloop()
