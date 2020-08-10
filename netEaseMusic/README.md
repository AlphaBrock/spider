# 网易云音乐API接口
1. 获取我的歌单
    可获取歌曲id
    ```
    POST https://music.163.com/weapi/v6/playlist/detail
    ```
   body
   ```
    {
        "id":"4431711",
        "offset":"0",
        "total":"true",
        "limit":"1000"
    }
   ```
2. 获取我的歌单列表
    可获取歌单id
   ```
   POST https://music.163.com/weapi/user/playlist
   ```
   body
   ```
    {
        "offset": "0",
        "limit": "1001",
        "uid": "3392707"
    }
    ```
3. 获取歌曲评论
   可获取歌曲评论数以及热门评论
   ```
   POST https://music.163.com/weapi/comment/resource/comments/get
   ```
    body  
   ```
    {
        "rid":"R_SO_4_1330348068",
        "threadId":"R_SO_4_1330348068",
        "pageNo":"1",
        "pageSize":"20",
        "cursor":"-1",
        "offset":"0",
        "orderType":"1"
    }
   ```
4. 获取热门歌单
   ```
   GET https://music.163.com/discover/playlist
   ```
5. 获取指定歌单列表
   ```
    GET https://music.163.com/playlist?id=2932915124
   ```
6. 登录接口
   邮箱登录
   ```
   https://music.163.com/weapi/w/login
   ```
   body
   ```
   {
    "username":"qq528327016@0126.com",
    "password":"29339b099ad11c630407f63c1bba880e",
    "rememberLogin":"true"
   }
   ```