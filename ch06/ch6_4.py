# 參閱6-23頁

from pytubefix import YouTube, exceptions
url = 'https://swf.com.tw/'

try:
    yt = YouTube(url)
except exceptions.PytubeFixError as e:
    print(f"\nPytube 發生錯誤：{e}")
except Exception as e:
    print(f"\n執行過程中發生未預期的錯誤：{e}")