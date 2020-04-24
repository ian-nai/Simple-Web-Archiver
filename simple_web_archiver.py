import tkinter as tk
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import os
import pathlib
import json
import subprocess

root = tk.Tk()

root.title('Simple Web Archiver')

canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

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


entry1 = tk.Entry (root) 

entry1.insert(0, 'Enter your URL...')
entry1.bind('<FocusIn>', on_entry_click)
entry1.bind('<FocusOut>', on_focusout)
entry1.config(fg = 'black')

canvas1.create_window(200, 140, window=entry1)

def getSquareRoot():  

    # The commented definition of 'Segments' below can be used to return base urls split by slashes, rather than by using the regex expression in the uncommented code
    url2 = entry1.get()
    
    html_page = requests.get(url2).text
    soup = BeautifulSoup(html_page, 'html.parser')
    links = []
    
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url2)
    print("Urls: ",urls)
    
    #Segments = url2.rpartition('/')
    Segments = re.findall('^(?:\w+://)?.*?(?::\d+)?(?=/|$)', url2)
    
    base_url = Segments[0]
    
    print(base_url)
    

    for link in BeautifulSoup(html_page, parse_only=SoupStrainer('a'), features="html.parser"):
       if link.has_attr('href'):
           #print(link['href'])
           links_list.append(link['href'])
       
 
    img_tags = soup.find_all('img')
    img_urls = ([img['src'] for img in img_tags])
    for x in img_urls:
        links_list.append(x)
    
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
    
    print(linkslist3)
    
    # ~~~ button stuff ~~~
    
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
                    open(d, 'wb').write(r.content)
                else:
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
                    open(d, 'wb').write(r.content)
                else:
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
                    open(d, 'wb').write(r.content)
                else:
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
                    open(d, 'wb').write(r.content)
                else:
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
                      open(d, 'wb').write(r.content)
                  else:
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
                         open(d, 'wb').write(r.content)
                     else:
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
                    open(d, 'wb').write(r.content)
                else:
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
                    open(d, 'wb').write(r.content)
                else:
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
                    open(d, 'wb').write(r.content)
                else:
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
                      open(d, 'wb').write(r.content)
                  else:
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
                         open(d, 'wb').write(r.content)
                     else:
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
                         open(d, 'wb').write(r.content)
                     else:
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

# buttons - visual setup      
var1 = tk.IntVar()
var2 = tk.IntVar()

c1 = tk.Checkbutton(root, text='Save Local Pages',variable=var1, onvalue=1, offvalue=0)
c1.select()
c1.pack()
c2 = tk.Checkbutton(root, text='Save External Pages',variable=var2, onvalue=1, offvalue=0)
c2.pack()

var3 = tk.IntVar()
var4 = tk.IntVar()

c3 = tk.Checkbutton(root, text='Save Pages as HTML',variable=var3, onvalue=1, offvalue=0)
c3.select()
c3.pack()
c4 = tk.Checkbutton(root, text='Save WARCs',variable=var4, onvalue=1, offvalue=0)
c4.pack()

    
    
button1 = tk.Button(text='Download Archive', command=getSquareRoot)
canvas1.create_window(200, 180, window=button1)

root.mainloop()
