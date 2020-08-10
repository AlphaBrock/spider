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
