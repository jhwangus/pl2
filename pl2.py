#! /usr/bin/python
# Filename: pl2.py

# Done: Fix the order dependency of track/annotation.   The final process should be at the end of track, not annotation.
# Done: Clean the whitespaces before and after in location and string, as well as tab and newline/crlf
# TODO: Port it to Python 3.4
# TODO: Provide a mapping list for track/location/annotation (e.g., node/audioURL/title) to adopt to different xml style

import xml.sax, sys, getopt, os.path, urllib.request, re
from random import choice

browser_agents = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.00; Windows 98)')]
player_agents = [('User-agent', 'Windows-Media-Player/11.0.5721.5145')]

class PlayListHandler(xml.sax.ContentHandler):

    def __init__ (self):
        self.isLocation, self.isAnnotation = 0, 0
        self.Location, self.Annotation = "", ""
        self.TrackOn = False
        self.cmdlist = []
   
    def startElement(self, name, attrs):
        if self.TrackOn:
            if name == "location" :
                self.isLocation = 1
                self.Location = ""
            elif name == "annotation":
                self.isAnnotation = 1
                self.Annotation = ""
        if name == "track":
            self.TrackOn = True
        return

    def endElement(self, name):
        global prefix
        if self.TrackOn:
            if name == "location":
                self.isLocation = 0
                # print self.Location
            elif name == "annotation":
                self.isAnnotation = 0
        if name == "track":
            self.Location = self.Location.strip()
            self.Annotation = self.Annotation.strip()
            ext = os.path.splitext(self.Location)[1]
            self.cmdlist.append([self.Location, prefix + self.Annotation.strip() + ext])
            self.TrackOn = False
        return

    def characters (self, ch):
        if self.isLocation == 1:
            self.Location += ch
        if self.isAnnotation == 1:
            self.Annotation += ch
        return

    def get_result(self):
        return self.cmdlist
    
def usage():
    ''' Display command usage.'''
    line = '''\

Usage        : pl2 [-f names.txt] [-h] [-s str] [-v] file 
-f names.txt : a name list to rename the songs (for m3u/asx)
-h           : this help
-s str       : file name prefix
-v           : version number
file_or_url  : URL/path of webpage or a XML/xspf/asx/m3u playlist file

This program takes an URL/path of a web page or a XML/xspf/asx/m3u
playlist file.  If it's a html web page, it scans the page for
the playlists and download them.  Then it further analyze the
playlists and download the songs.

Most of the songs from the Internet would have numerical names such as
"1336867.mp3" for easier administration at the web site, it's better to
rename them.  Since XML/XSPF usually comes with the songs' "real" names
(in <annotation> tags), so their songs would be automatically renamed
after downloaded.

m3u and asx usually do not have a fixed format for songs' names. So
this tool provides an interactive way for the users to add a name list
file (each line matches with each of the songs from the playlist) and
use it to rename.  How to get the name list?  (1) You can view the page
source of the web page (i.e., edit the html file) and there its author
usually would list the songs.  (2) Some of the m3u/asx files come with
songs' names in "comments".  You can copy them to a text file and then
edit them.

Note: asx support is not well tested due to the limited links I can find.
      Also, the Unicode/GB/BiG5 supports are just workable but not perfect.

Example:

pl2 http://bbs.wenxuecity.com/music/643349.html
pl2 http://www.simon.com/1213.xml
pl2 -s "La Tilla" 2223.xspf
pl2 -f abba.txt ABBA.m3u
pl2 -s "Chopin" -f goldencd.txt http://www.simon.com/goldencd.asx

'''
    sys.stderr.write(line)
    sys.stderr.flush()
    
def version():
    ''' Display command version.'''
    sys.stderr.write('PL2 ' + ver_str + ', by Clown\n')
    sys.stderr.write('Copyright (C)2012 Clown, All rights reserved.\n')
    sys.stderr.write('This SW is provided under the Simplified BSD License.\n')
    sys.stderr.write('For details, please read the readme file.')
    sys.stderr.flush()

def isURL(url):
    # print url[:7]
    if url[:7].upper() == 'HTTP://':
        return True
    else:
        return False

def isHTML(fname):
    ext = os.path.splitext(fname)[1].upper()
    if ext == ".HTML" or ext == ".HTM":
        return True
    else:
        return False

def file2str(fname, exit = True):
    try:
        fl = open(fname, "r")
    except Exception as e:
        print ("Error opening %s: %s" % (fname, e))
        if exit:
            sys.exit(3)
        else:
            return ""
    content = fl.read()
    fl.close()
    return content    

def file2list(fname, exit = True):
    try:
        fl = open(fname, "r")
    except Exception as e:
        print ("Error opening %s: %s" % (fname, e))
        if exit:
            sys.exit(3)
        else:
            return []
    tlist = fl.readlines()
    fl.close()
    content = []
    for t in tlist:
        content.append(t.rstrip())
    return content    

def get_playlist(fname):
    # scan html to get the playlist file(s)
    p = re.compile('file=.*?\.xml|url=.*?\.xspf|http.*?.asx|http.*?.m3u', re.IGNORECASE  | re.MULTILINE)
    content = file2str(fname)
    xli = []
    for line in p.findall(content):
        url = line[line.find('=')+1:]
        print ("Retrieve playlist ...")
        fn = download_url(url)
        xli.append(fn)
    return list(set(xli))

def download_url(url, role='b'):
    filename = ""
    proxies = {}
    length = None
    try:
        filename = url.split("/")[-1]
        outfile = open(filename, "wb")
        # opener = urllib2.build_opener()
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        # if role == 'p':
        #    opener.addheaders = player_agents
        # else:
        #    opener.addheaders = browser_agents
        # instream = opener.open(url)
        # length = instream.info().getheader("Content-Length")
        length = response.getheader("Content-Length")
        if not length or length == 0 or length == '0':
            length = "?"
        print ("Downloading %s (%s bytes) ..." % (filename, length))
        if length != "?":
            length = float(length)
        # bytesRead = 0.0
        # count = 0
        # for line in instream:
        #    bytesRead += len(line)
        #    count += 1
        #    if length != "?" and count % 10 == 0:
        #        print ("%s: %.02f/%.02f kb (%d%%)" % (filename, bytesRead / 1024.0, length / 1024.0,
        #            100*bytesRead / length), "\r",)
        #    outfile.write(line)
        # instream.close()
        body = response.read()
        outfile.write(response)
        outfile.close()
        bytesRead = body.len()
        if length != "?":
            print ("%s: %.02f/%.02f kb (%d%%)" % (filename, bytesRead / 1024.0, length / 1024.0,
                100*bytesRead / length))
        return filename
    except Exception as e:
        print ("\nError downloading %s: %s" % (url, e))
        return ""

def download_all(flist):
    for url, final_name in flist:
        name = download_url(url, 'p')
        if final_name != "":
            print (name, '->', final_name.encode("utf-8"))
            if os.path.exists(final_name):
                os.remove(final_name)
            os.rename(name, final_name)

def handle_xml(fname):
    # For xml and xspf
    try:
        fl = open(fname, "r")
    except Exception as e:
        print ("Error opening %s: %s" % (fname, e))
        sys.exit(3)
    MyHandler = PlayListHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(MyHandler)
    try:
        parser.parse(fl)
    except Exception as e:
        print ("Error opening %s: %s" % (fname, e))
        fl.close()
        sys.exit(3)
    fl.close()
    flist = MyHandler.get_result()
    download_all(flist)

def strip_m3u_asx(fname):
    content = file2str(fname, False)
    p = re.compile('((http|mms).*?.(mp3|wma|asf))', re.IGNORECASE  | re.MULTILINE)
    alist = []
    for t in p.findall(content):
        alist.append(t[0])
    return alist

def handle_m3u_asx(fname, names=[]):
    alist = strip_m3u_asx(fname)
    n = iter(names)
    flist = []
    for t in alist: 
        flist.append([t, next(n, "")])
    # print flist
    download_all(flist)

def get_name_list(fname):
    alist = strip_m3u_asx(fname)
    while True:
        answer = raw_input("Input a name list file (Enter to skip): ").rstrip()
        if answer == "":
            break
        nlist = file2list(answer, False)
        n = iter(nlist)
        namelist = []
        for f in alist:
            nf = next(n, "")
            if nf != "":
                nf += os.path.splitext(f)[1]
            print (f, '->', nf.encode("utf-8"))
            namelist.append(nf)
        answer = raw_input("Is this name list good to use? (Y/N) ")
        if answer[0].upper() == "Y":
            return namelist           
    return []

def confirm_name_list(fname, names):
    alist = strip_m3u_asx(fname)
    while True:
        nlist = file2list(names, False)
        n = iter(nlist)
        namelist = []
        for f in alist:
            nf = next(n, "")
            if nf != "":
                nf += os.path.splitext(f)[1]
            print (f, '->', nf.encode("UTF-16"))
            namelist.append(nf)
        answer = raw_input("Is this name list good to use? (Y/N) ")
        if answer[0].upper() == "Y":
            return namelist           
        names = raw_input("Input a name list file (Enter to skip): ").rstrip()
        if names == "":
            break
    return []

def main(argv):
    global ver_str, prefix, fname, names
    ver_str = "Ver. 1.0"
    prefix = ''
    names = ''
    # getopt
    try:                                
        opts, args = getopt.getopt(argv, "f:hvs:", ["url=", "httpproxy=", "ftpproxy=", "gopherproxy=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    # print opts
    for opt, optarg in opts:
        if opt == '-f':
            names = optarg
        elif opt == '-h':
            usage()                     
            sys.exit()
        elif opt == '-v':
            version()
            sys.exit()
        elif opt == '-s':
            prefix = optarg
    if len(args) == 1:
        url = args[0]
    else:
        usage()
        sys.exit()
    # Check if fname is an url. If so, download it.
    if isURL(url):
        print ("Retrieve URL ...")
        fname = download_url(url)
    else:
        fname = url
    # print fname
    # Check if the file is an html.  If so, scan and download xml/xspf/m3u/asx
    if isHTML(fname):
        playlist = get_playlist(fname)
    else:
        playlist = [fname]
    # Handle each playlist
    for fname in playlist:
        ext = os.path.splitext(fname)[1].upper()
        if ext == ".XML" or ext == ".XSPF":
            print ("Found XML playlist ...")
            handle_xml(fname)
            print ("Enjoy the music!")
        elif ext == ".M3U" or ext == ".ASX":
            if ext == ".M3U":
                print ("Found M3U playlist ...")
            else:
                print ("Found ASX playlist ...")
            if names == "":
                print ("The player list " + fname + " is a m3u/asx file.")
                print ("You did not provide a name list to rename songs.")
                answer = raw_input("Do you want to add a name list?  (Y/N) ")
                new_names = []
                if answer[0].upper() == "Y":
                    new_names = get_name_list(fname)
                else:
                    new_names = []
                if len(new_names) == 0:
                    answer = raw_input("Do you want to proceed to download the songs without a name list?  (Y/N) ")
                    if answer[0].upper() != "Y":
                        continue
                handle_m3u_asx(fname, new_names) 
                print ("Enjoy the music!")
            else:
                new_names = confirm_name_list(fname, names)
                # print new_names
                if len(new_names) == 0:
                    answer = raw_input("Do you want to proceed to download the songs without a name list?  (Y/N) ")
                    if answer[0].upper() != "Y":
                        continue
                handle_m3u_asx(fname, new_names)
                print ("Enjoy the music!")
        else:
            print ("Error: " + fname + " has an unknown file extension.")

if __name__ == "__main__":
    main(sys.argv[1:])
