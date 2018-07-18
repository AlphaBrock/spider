# 老司机爬虫程序（仅支持Python3）

> Emmm，老司机座驾，爬取1024的那啥图片，你们都懂的
>
> 建议在海外VPS上执行，本地挂全局代理
>
> 本文最后更新于<u>**2018-2-05-18:50**</u>
>
> ==***++大佬们注意身体，小心营养跟不上++***==

**UpdateNew：** 新增pornhub爬虫

**UpdateNew：** 新增mm131爬虫

**UpdateNew：** 91Porn新增文件去重

**New：** *新增91Porn爬虫*

### 目录

- [环境需求](#环境需求)
- [python3安装](#python3安装)
- [所需库安装](#所需库安装)
- [1024食用教程](#1024食用教程)
- [91porn食用教程](#91porn食用教程)
- [mm131食用教程](#mm131食用教程)
- [pornhub食用教程](#pornhub食用教程)

## 环境需求
> Win配置 Python3环境运行即可，不麻烦，这里主要讲 Linux环境
- Python>=3 and requests库
- Ubuntu 16.04 (Xenial) or 14.04 (Trusty)
- CentOS 6 (x86_64) with Updates

- Debian 8 (Jessie)

## python3安装
> 由于Ubuntu自带了python2 and 3，这里就不再赘述

####  Centos安装Python3.6.4

- 获取源码包

  ```shell
  wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
  ```

- 解压安装

  ```shell
  tar -zxvf Python-3.6.4.tgz
  mv Python-3.6.4 /usr/local
  cd /usr/local/Python-3.6.4
  ./configure
  make
  make install
  ```

- 软链接

  ```shell
  ln -s /usr/local/bin/python3.6 /usr/bin/python3
  ```

- 查看版本

  ```shell
  python3 -V
  ```

## 所需库安装

- pip安装

  **Debian (Wheezy and newer) and Ubuntu (Trusty Tahr and newer)**

  ```
  sudo apt-get install python3-pip
  ```

   **CentOS**

  ```
  sudo yum install python34-setuptools
  sudo easy_install pip
  ```

- 安装request

  ```
  pip3 install requests
  ```
> 以下库供pornhub食用，如果你是不打算食用pornhub爬虫以下俩库无需安装

- 安装lxml
  ```shell
  pip3 install lxml
  ```
- 安装bs4

  ```shell
  pip3 install bs4
  ```


## 1024食用教程

> 源码分为单线程和多线程，具体使用那个大佬们自行定夺

![1024](https://i.imgur.com/QikIi2H.png)

![1024_2](https://i.imgur.com/FBZsEgu.png)

- 创建存放目录

  ```
  mkdir pic
  cd pic
  ```

- 单线程

  ```python
  import requests
  import threading
  import re
  import os
  def download_pic(url,dir,filename):
      headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'https://t66y.com'}
      req=requests.get(url=url,headers=headers)
      if req.status_code==200:
          with open(str(dir)+'/'+str(filename)+'.jpg','wb') as f:
              f.write(req.content)
  flag=1
  while flag<=270:
      base_url='https://t66y.com/'
      page_url='https://t66y.com/thread0806.php?fid=8&search=&page='+str(flag)
      get=requests.get(page_url)
      article_url=re.findall(r'<h3><a href="(.*)" target="_blank" id="">(?!<.*>).*</a></h3>',str(get.content,'gbk',errors='ignore'))
      for url in article_url:
          getpage=requests.get(str(base_url)+str(url))
          tittle=re.findall(r'<h4>(.*)</h4>',str(getpage.content,'gbk',errors='ignore'))
          file=tittle[0]
          if  os.path.exists(file)==False:
              os.makedirs(file)
              img_url=re.findall(r'<input src=\'(.*?)\'',str(getpage.content,'gbk',errors='ignore'))
              filename=0
              print('开始下载：'+file)
              for download_url in img_url:
                  print('下载第'+str(filename+1)+'张图片中~~~')
                  download_pic(download_url,file,filename)
                  print('下载完成')
                  filename=filename+1
              print('下载完成，共'+str(filename)+'张图片')
          else:
              print('文件夹已存在，跳过')
      print('第'+str(flag)+'页下载完成')
      flag=flag+1
      
  ```

- 多线程

  ```python
  import requests
  import threading
  import re
  import os
  class myThread (threading.Thread):   #继承父类threading.Thread
      def __init__(self, url, dir, filename):
          threading.Thread.__init__(self)
          self.threadID = filename
          self.url = url
          self.dir = dir
          self.filename=filename
      def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
          download_pic(self.url,self.dir,self.filename)
  def download_pic(url,dir,filename):
      headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'https://t66y.com'}
      req=requests.get(url=url,headers=headers)
      if req.status_code==200:
          with open(str(dir)+'/'+str(filename)+'.jpg','wb') as f:
              f.write(req.content)
  try:
      flag=1
      while flag<=270:
          base_url='https://t66y.com/'
          page_url='https://t66y.com/thread0806.php?fid=8&search=&page='+str(flag)
          get=requests.get(page_url)
          article_url=re.findall(r'<h3><a href="(.*)" target="_blank" id="">(?!<.*>).*</a></h3>',str(get.content,'gbk',errors='ignore'))
          for url in article_url:
              threads=[]
              tittle=['default']
              getpage=requests.get(str(base_url)+str(url))
              tittle=re.findall(r'<h4>(.*)</h4>',str(getpage.content,'gbk',errors='ignore'))
              file=tittle[0]
              if  os.path.exists(file)==False:
                  os.makedirs(file)
                  img_url=re.findall(r'<input src=\'(.*?)\'',str(getpage.content,'gbk',errors='ignore'))
                  filename=1
                  print('开始下载：'+file)
                  for download_url in img_url:
                      thread=myThread(download_url,file,filename)
                      thread.start()
                      threads.append(thread)
                      filename=filename+1
                  for t in threads:
                      t.join()
                  print('下载完成，共'+str(filename)+'张图片')
              else:
                  print('文件夹已存在，跳过')
          print('第'+str(flag)+'页下载完成')
          flag=flag+1
  except:
      print('程序错误，退出')
  ```

  ```
  python3 1024_spider*.py
  ```

#### 错误提示

若出现以下提示，无视即可

```python
During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.5/threading.py", line 914, in _bootstrap_inner
    self.run()
  File "1024_spider_th.py", line 13, in run
    download_pic(self.url,self.dir,self.filename)
  File "1024_spider_th.py", line 16, in download_pic
    req=requests.get(url=url,headers=headers)
  File "/usr/lib/python3/dist-packages/requests/api.py", line 67, in get
    return request('get', url, params=params, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/api.py", line 53, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 468, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 576, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/adapters.py", line 437, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPConnectionPool(host='eroticgirls.ru', port=80): Max retries exceeded with url: /photo_x/7424/10.jpg (Caused by NewConnectionError('<requests.packages.urllib3.connection.HTTPConnection object at 0x7fc35c2f00f0>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution',))
```

## 91porn食用教程

![91porn](https://i.imgur.com/ilTFFXR.png)

```python
import requests
import os,re,time,random
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False
def format_str(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str+i
    return content_str
def download_mp4(url,dir):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://91porn.com'}
    req=requests.get(url=url)
    filename=str(dir)+'/1.mp4'
    with open(filename,'wb') as f:
        f.write(req.content)
def download_img(url,dir):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://91porn.com'}
    req=requests.get(url=url)
    with open(str(dir)+'/thumb.png','wb') as f:
        f.write(req.content)
def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))
flag=1
while flag<=100:
    tittle=[]
    base_url='http://91porn.com/view_video.php?viewkey='
    page_url='http://91porn.com/v.php?category=rf&viewtype=basic&page='+str(flag)
    get_page=requests.get(url=page_url)
    viewkey=re.findall(r'<a target=blank href="http://91porn.com/view_video.php\?viewkey=(.*)&page=.*&viewtype=basic&category=rf">\n                    <img ',str(get_page.content,'utf-8',errors='ignore'))
    for key in viewkey:
        headers={'Accept-Language':'zh-CN,zh;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36','X-Forwarded-For':random_ip(),'referer':page_url,'Content-Type': 'multipart/form-data; session_language=cn_CN'}
        video_url=[]
        img_url=[]
        base_req=requests.get(url=base_url+key,headers=headers)
        video_url=re.findall(r'<source src="(.*?)" type=\'video/mp4\'>',str(base_req.content,'utf-8',errors='ignore'))
        tittle=re.findall(r'<div id="viewvideo-title">(.*?)</div>',str(base_req.content,'utf-8',errors='ignore'),re.S)
        img_url=re.findall(r'poster="(.*?)"',str(base_req.content,'utf-8',errors='ignore'))
        t=tittle[0]
        tittle[0]=format_str(t)
        t=tittle[0]
        if os.path.exists(str(t))==False:
            os.makedirs(str(t))
            print('开始下载:'+str(t))
            download_img(str(img_url[0]),str(t))
            download_mp4(str(video_url[0]),str(t))
            print('下载完成')
        else:
            print('已存在文件夹,跳过')
            time.sleep(2)
    flag=flag+1
    print('此页已下载完成，下一页是'+str(flag))
```
**New**
```python

```

## mm131食用教程

```python
import requests
import re
import os
def download_pic(b,dir):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://www.mm131.com'}
    a=1
    while True:
        url='http://img1.mm131.me/pic/'+str(b)+'/'+str(a)+'.jpg'
        req=requests.get(url=url,headers=headers)
        if req.status_code==200:
            with open(str(dir)+'/'+str(a)+'.jpg','wb') as f:
                f.write(req.content)
                a=a+1
        else:
            break
flag=1
while True:
    if flag==1:
        get=requests.get('http://www.mm131.com/xinggan/')
        b=re.findall(r'<dd><a target="_blank" href="http://www.mm131.com/xinggan/([0-9]*).html"><img src=',get.text)
        for a in b:
            getpage=requests.get('http://www.mm131.com/xinggan/'+str(a)+'.html')
            tittle=re.findall(r'<h5>(.*)</h5>',str(getpage.content,'gb2312',errors='ignore'))
            for t in tittle:
                if os.path.exists(t)==False:
                    os.makedirs(t)
                    print('开始下载：'+t)
                    download_pic(a,t)
                    print('下载完成')
                else:
                    print('文件夹已存在，跳过')
        flag=flag+1
        print('这一页的任务已经完成了')
    else:
        get=requests.get('http://www.mm131.com/xinggan/list_6_'+str(flag)+'.html')
        if get.status_code==200:
            b=re.findall(r'<dd><a target="_blank" href="http://www.mm131.com/xinggan/([0-9]*).html"><img src=',get.text)
            for a in b:
                getpage=requests.get('http://www.mm131.com/xinggan/'+str(a)+'.html')
                tittle=re.findall(r'<h5>(.*)</h5>',str(getpage.content,'gb2312',errors='ignore'))
                for t in tittle:
                    if os.path.exists(t)==False:
                        os.makedirs(t)
                        print('开始下载：'+t)
                        download_pic(a,t)
                        print('下载完成')
                    else:
                        print('文件夹已存在，跳过')
            flag=flag+1
            print('这一页的任务已经完成了')
        else:
            break
```

## pornhub食用教程
- 如何使用

```
python3 ***.py [分类] [清晰度]
```
下面给出一个例子

```
python3 ***.py 111 720
```
其中的`111`是如何获取的呢，在打开pornhub的一个分类时，例如这个[https://www.pornhub.com/video?c=111](https://www.pornhub.com/video?c=111)，这样就一目了然了，`https://www.pornhub.com/video?c=[分类]`

==**注意：** 最高可以下载720P 1080P是不能下载==

- 配合多线程下载器使用

> 建议使用FDM，下载地址：[https://www.freedownloadmanager.org/](https://www.freedownloadmanager.org/)

为了更好的利用带宽满速下载，建议使用以下爬虫，脚本会将获取的直链写入`url.txt`文件中，届时导入下载器即可
    
```python
from bs4 import BeautifulSoup as bs
import requests,re,os,urllib,sys
cat=sys.argv[1]
flag=1
url_content=[]
find=[]
find_tittle=[]
quality=sys.argv[2]
#默认只下载100页，如需更多请把下面的数值改成你想要的数值
while flag<=100:
    pornhub_url='https://www.pornhub.com/'
    c_page=pornhub_url+'video?c='+str(cat)
    base_page=c_page+'&page='+str(flag)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':base_page}
    get_base=requests.get(base_page,headers=headers)
    url_soup=bs(get_base.content,'lxml')
    for a_content in url_soup.select('.search-video-thumbs.videos li.videoBox'):
        a_content.a['class']='img js-pop'
        url_content=re.findall(r' href="/(.*?)" title',str(a_content.a))
        url=pornhub_url+url_content[0]
        headers_1={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':url}
        reqpage=requests.get(url,headers=headers_1)
        rfind='"quality":"'+str(quality)+'","videoUrl":"(.*?)"'
        find=re.findall(rfind,str(reqpage.content,'utf-8',errors='ignore'))
        find_tittle=re.findall(r'<span class="inlineFree">(.*?)</span>',str(reqpage.content,'utf-8',errors='ignore'))
        try:
            download_url=find[0].replace('\\','')
            with open('url.txt','a') as f:
                f.write(download_url)
                f.write('\n')
            print('已存在url.txt文件')
        except IndexError:
            print('没有此清晰度')
            pass
    flag+=1
```
- 直接下载

如果你是挂机下载那么就用这个吧
```python
from bs4 import BeautifulSoup as bs
import requests,re,os,urllib,sys
def download_mp4(url,dir,headers):
    req=requests.get(url=url,headers=headers)
    filename=str(dir)+'/1.mp4'
    with open(filename,'wb') as f:
        f.write(req.content)
cat=sys.argv[1]
flag=1
url_content=[]
find=[]
find_tittle=[]
quality=sys.argv[2]
#默认只下载100页，如需更多请把下面的数值改成你想要的数值
while flag<=100:
    pornhub_url='https://www.pornhub.com/'
    c_page=pornhub_url+'video?c='+str(cat)
    base_page=c_page+'&page='+str(flag)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':base_page}
    get_base=requests.get(base_page,headers=headers)
    url_soup=bs(get_base.content,'lxml')
    for a_content in url_soup.select('.search-video-thumbs.videos li.videoBox'):
        a_content.a['class']='img js-pop'
        url_content=re.findall(r' href="/(.*?)" title',str(a_content.a))
        url=pornhub_url+url_content[0]
        headers_1={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':url}
        reqpage=requests.get(url,headers=headers_1)
        rfind='"quality":"'+str(quality)+'","videoUrl":"(.*?)"'
        find=re.findall(rfind,str(reqpage.content,'utf-8',errors='ignore'))
        find_tittle=re.findall(r'<span class="inlineFree">(.*?)</span>',str(reqpage.content,'utf-8',errors='ignore'))
        try:
            if os.path.exists(str(find_tittle[0]))==False:
                download_url=find[0].replace('\\','')
                os.makedirs(str(find_tittle[0]))
                print('开始下载：'+str(find_tittle[0]))
                print('下载URL：'+download_url)
                download_mp4(str(download_url),str(find_tittle[0]),headers_1)
                print('下载完成')
            else:
                print('跳过，文件存在')
        except IndexError:
            print('没有此清晰度')
            pass
    flag+=1
```


