License
=======

Copyright (c) 2012, Clown@Crazys.net, All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.


Usage
=====

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


Installation
============

1. Unzip the package.
2. Make sure folder "pl2" is added into the DOS PATH environment variable.


Change History
==============

v. 1.0
1. First quick installment.

v. 2.0
1. Added support for starting from html or playlist file from net or local.
2. Added support for xspf/m3u/asx.
3. Added support for adding namelist for m3u/asx playlist
4. Added license statement.


简体说明
========

1. 这个工具提供从网页扫瞄 playlist 并自动下载的功能。流程几乎全部自动化。
   由於网页/playlist都会下载，就算中途有些疑难杂症，也很容易诊断解决。

2. 安装程序：

   a. unzip the package.
   b. Make sure folder "pl2" is added into the DOS PATH environment variable.

3. 最简单的方式：
   
   a. 直接使用网页地址：    pl2 http://bbs.wenxuecity.com/music/643349.html
   b. 使用已经下载的网页：  pl2 643349.html

4. 如果网页有些问题，可以用 view->Page Source 或直接用编辑器打开，然後找到
   playlist，剪贴给工具执行：

   a. 使用playlist地址：    pl2 http://www.simon.com/1213.xml
   b. 使用playlist档：      pl2 1213.xml

5. 有时候xml档encoding不正确，例如宣称是 utf-8 但有时却存成 utf-16。建议使
   用 ConvertZ 这个软件的"档案"功能转换。xml/xspf 最好是存成 utf-8。

6. m3u/asx 通常没有附上歌名，所以要另外解决。一个方法是从网页上或HTML档中剪贴
   取得，存至一个文字档（例如：abba.txt）并编辑，让每行一条歌名，这将对应到
   m3u/asx playlist 档中的每条歌。执行时用 "-f" 提供这个 namelist。

   pl2 -f abba.txt http://www.simon.com/ABBA_19861211.m3u

7. 如果没有使用 -f，工具下载 m3u/asx 後会提问是否要继续，以及是否要提供
   namelist。这时可以回答 "N" 暂时中止结束。然後用编辑器打开 m3u/asx 检查，
   有时候会有歌名在它们的 comment lines 中，这样就可以将它们剪贴产生 namelist
   档。然後再重新开始，用 -f 或者半路补档。

   pl2 http://space.wenxuecity.com/media/1252101412.m3u
   Retrieve URL ...
   Downloading 1252101412.m3u (880 bytes) ...
   1252101412.m3u: 0.86/0.86 kb (100%)
   Found M3U playlist ...
   The player list 1252101412.m3u is a m3u/asx file.
   You did not provide a name list to rename songs.
   Do you want to add a name list?  (Y/N) n
   Do you want to proceed to download the songs without a name list?  (Y/N) n

   1252101412.m3u 内容是：

   //01 Butterfly Concerto
   http://space.wenxuecity.com/media/1251423294.mp3
   //02 The Heart Asks The Pleasure First
   http://space.wenxuecity.com/media/1251424288.mp3
   //03 To The Children
   http://space.wenxuecity.com/media/1251423517.mp3
   //04 Through Her Eyes
   http://space.wenxuecity.com/media/1251425117.mp3
   //05 Grandmother's Heart
   http://space.wenxuecity.com/media/1251423751.mp3
   //06 Waterfall
   http://space.wenxuecity.com/media/1251424589.mp3
   //07 Children's Dawn Blessing
   http://space.wenxuecity.com/media/1251424000.mp3
   //08 First Spring
   http://space.wenxuecity.com/media/1251424832.mp3
   //09 Parnie's Song
   http://space.wenxuecity.com/media/1251424714.mp3
   //10 Tomorrow's Child
   http://space.wenxuecity.com/media/1251425249.mp3
   //11 Words
   http://space.wenxuecity.com/media/1251425379.mp3
   //12 Cristofori's Dream
   http://space.wenxuecity.com/media/1251423406.mp3

   编辑成new_list.txt

   01 Butterfly Concerto
   02 The Heart Asks The Pleasure First
   03 To The Children
   04 Through Her Eyes
   05 Grandmother's Heart
   06 Waterfall
   07 Children's Dawn Blessing
   08 First Spring
   09 Parnie's Song
   10 Tomorrow's Child
   11 Words
   12 Cristofori's Dream

   然後再执行一次：

   pl2 -f new_list.txt 1252101412.m3u

   注意：这时候的名字字体显示不尽完善，主要是因为显示 utf-8 的关系。
         抱歉，一时没有好的解决。但是存档名或更换档名没有问题。

8. 本工具用 Python 撰写，已经用 py2exe 编译成DOS 执行档 pl2.exe，不
   必另外安装 Python。另外提供源码 pl2.py 供其它作业系统如 Linux 使
   用（需用 Python v2.6 或以上）。


繁體說明
========

1. 這個工具提供從網頁掃瞄 playlist 並自動下載的功能。流程幾乎全部自動化。
   由於網頁/playlist都會下載，就算中途有些疑難雜症，也很容易診斷解決。

2. 安裝程序：

   a. unzip the package.
   b. Make sure folder "pl2" is added into the DOS PATH environment variable.

3. 最簡單的方式：
   
   a. 直接使用網頁地址：    pl2 http://bbs.wenxuecity.com/music/643349.html
   b. 使用已經下載的網頁：  pl2 643349.html

4. 如果網頁有些問題，可以用 view->Page Source 或直接用編輯器打開，然後找到
   playlist，剪貼給工具執行：

   a. 使用playlist地址：    pl2 http://www.simon.com/1213.xml
   b. 使用playlist檔：      pl2 1213.xml

5. 有時候xml檔encoding不正確，例如宣稱是 utf-8 但有時卻存成 utf-16。建議使
   用 ConvertZ 這個軟件的"檔案"功能轉換。xml/xspf 最好是存成 utf-8。

6. m3u/asx 通常沒有附上歌名，所以要另外解決。一個方法是從網頁上或HTML檔中剪貼
   取得，存至一個文字檔（例如：abba.txt）並編輯，讓每行一條歌名，這將對應到
   m3u/asx playlist 檔中的每條歌。執行時用 "-f" 提供這個 namelist。

   pl2 -f abba.txt http://www.simon.com/ABBA_19861211.m3u

7. 如果沒有使用 -f，工具下載 m3u/asx 後會提問是否要繼續，以及是否要提供
   namelist。這時可以回答 "N" 暫時中止結束。然後用編輯器打開 m3u/asx 檢查，
   有時候會有歌名在它們的 comment lines 中，這樣就可以將它們剪貼產生 namelist
   檔。然後再重新開始，用 -f 或者半路補檔。

   pl2 http://space.wenxuecity.com/media/1252101412.m3u
   Retrieve URL ...
   Downloading 1252101412.m3u (880 bytes) ...
   1252101412.m3u: 0.86/0.86 kb (100%)
   Found M3U playlist ...
   The player list 1252101412.m3u is a m3u/asx file.
   You did not provide a name list to rename songs.
   Do you want to add a name list?  (Y/N) n
   Do you want to proceed to download the songs without a name list?  (Y/N) n

   1252101412.m3u 內容是：

   //01 Butterfly Concerto
   http://space.wenxuecity.com/media/1251423294.mp3
   //02 The Heart Asks The Pleasure First
   http://space.wenxuecity.com/media/1251424288.mp3
   //03 To The Children
   http://space.wenxuecity.com/media/1251423517.mp3
   //04 Through Her Eyes
   http://space.wenxuecity.com/media/1251425117.mp3
   //05 Grandmother's Heart
   http://space.wenxuecity.com/media/1251423751.mp3
   //06 Waterfall
   http://space.wenxuecity.com/media/1251424589.mp3
   //07 Children's Dawn Blessing
   http://space.wenxuecity.com/media/1251424000.mp3
   //08 First Spring
   http://space.wenxuecity.com/media/1251424832.mp3
   //09 Parnie's Song
   http://space.wenxuecity.com/media/1251424714.mp3
   //10 Tomorrow's Child
   http://space.wenxuecity.com/media/1251425249.mp3
   //11 Words
   http://space.wenxuecity.com/media/1251425379.mp3
   //12 Cristofori's Dream
   http://space.wenxuecity.com/media/1251423406.mp3

   編輯成new_list.txt

   01 Butterfly Concerto
   02 The Heart Asks The Pleasure First
   03 To The Children
   04 Through Her Eyes
   05 Grandmother's Heart
   06 Waterfall
   07 Children's Dawn Blessing
   08 First Spring
   09 Parnie's Song
   10 Tomorrow's Child
   11 Words
   12 Cristofori's Dream

   然後再執行一次：

   pl2 -f new_list.txt 1252101412.m3u

   注意：這時候的名字字體顯示不盡完善，主要是因為顯示 utf-8 的關係。
         抱歉，一時沒有好的解決。但是存檔名或更換檔名沒有問題。

8. 本工具用 Python 撰寫，已經用 py2exe 編譯成DOS 執行檔 pl2.exe，不
   必另外安裝 Python。另外提供源碼 pl2.py 供其它作業系統如 Linux 使
   用（需用 Python v2.6 或以上）。

