# -*- coding: utf-8 -*-
import hashlib

import requests
import random
import json
import base64
import time

from pprint import pprint
import config
import encrypted
import db


class Request(object):
    """
    封装个类用于做request请求
    """
    def __init__(self, method, url, body, headers):
        self.method = method
        self.url = url
        self.body = body
        self.headers = headers

    def post_url(self):
        try:
            body = json.dumps(self.body).encode('utf-8')
            params, encSecKey = encrypted.obtain_params_and_seckey(body)
            payload = {
                'params': params,
                'encSecKey': encSecKey
            }
            response = requests.request("{}".format(self.method), self.url, headers=self.headers, data=payload)
            return response
        except Exception as e:
            config.logger1.exception("Request 提交请求出现异常，抛出如下错误:{}".format(e))


def write_sql():
    pass


def random_ip():
    a = random.randint(1, 255)
    b = random.randint(1, 255)
    c = random.randint(1, 255)
    d = random.randint(1, 255)
    return str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)


def login(type, username, passwd):
    url = ''
    md_create = hashlib.md5()
    md_create.update(passwd.encode('utf-8'))  # 计算密码的md5
    if type is "cellphone":
        url = "https://music.163.com/weapi/login/cellphone"
    elif type is "email":
        url = "https://music.163.com/weapi/w/login"
    method = "POST"
    headers = {
        'User-Agent': '{}'.format(random.choice(config.UserAgent)),
        'X-Forwarded-For': random_ip()
    }
    body = {
        "username": "{}".format(username),
        "password": "{}".format(md_create.hexdigest()),
        "rememberLogin": "true"
    }
    response = Request(method, url, body, headers).post_url()
    try:
        if response.status_code == 200:
            text = json.loads(response.text)
            account_id = text['account'].get('id')
            config.logger1.info("login 登录成功，获取用户id为:{}".format(account_id))
            return account_id
        else:
            config.logger1.warning("login 提交登录失败，返回结果为:{}".format(response.text))
    except Exception as e:
        config.logger1.exception("login 处理返回结果数据异常，抛出信息:{}".format(e))


def search_music(musicid):
    url = "https://music.163.com/weapi/cloudsearch/get/web"
    method = "POST"
    headers = {
        'User-Agent': '{}'.format(random.choice(config.UserAgent)),
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Forwarded-For': random_ip()
    }
    body = {
        "hlpretag": "",
        "hlposttag": "",
        "s": "{}".format(musicid),
        "type": "1",
        "offset": "0",
        "total": "true",
        "limit": "30"
    }
    response = Request(method, url, body, headers).post_url()
    try:
        if response.status_code == 200:
            text = json.loads(response.text)
            # trackIds = text['playlist'].get('trackIds')
            if len(text['result']) != 0:
                songs = text['result'].get('songs')
                musicName = songs[0].get('name')
                singer = songs[0].get('ar')[0].get('name')
                config.logger1.info("search_music 搜索到歌曲信息，音乐名:{}，音乐ID:{}，歌手:{}".format(musicName, musicid, singer))
                return musicName, singer
            else:
                config.logger1.info("search_music 搜索无该歌曲，音乐ID:{}，跳过!".format(musicid))
                return None, None
        else:
            config.logger1.warning("search_music 未搜索到歌单信息，返回结果为:{}".format(response.text))
    except Exception as e:
        config.logger1.exception("search_music 处理返回结果数据异常，抛出信息:{}".format(e))


def get_playlist_detail():
    url = "https://music.163.com/weapi/v6/playlist/detail"
    method = "POST"
    headers = {
        'User-Agent': '{}'.format(random.choice(config.UserAgent)),
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Forwarded-For': random_ip()
    }
    body = {"id": "4431711", "offset": "0", "total": "true", "limit": "1000", "n": "1000"}
    response = Request(method, url, body, headers).post_url()
    try:
        if response.status_code == 200:
            text = json.loads(response.text)
            trackIds = text['playlist'].get('trackIds')
            musicInfo = []
            for item in trackIds:
                musicID = item.get('id')
                config.logger1.info(
                    "get_playlist_detail 获取到歌曲信息，音乐ID:{}".format(musicID))
                musicName, singer = search_music(musicID)
                time.sleep(2)
                musicInfo.append([musicID, musicName, singer])
            return musicInfo
        else:
            config.logger1.warning("get_playlist_detail 未获取到歌单信息，返回结果为:{}".format(response.text))
    except Exception as e:
        config.logger1.exception("get_playlist_detail 处理返回结果数据异常，抛出信息:{}".format(e))


def get_song_detail(musicInfo):
    for musics in musicInfo:
        musicID = musics[0]
        musicName = musics[1]
        singer = musics[2]
        url = "https://music.163.com/weapi/comment/resource/comments/get"
        method = "POST"
        headers = {
            'User-Agent': '{}'.format(random.choice(config.UserAgent)),
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Forwarded-For': random_ip()
        }
        body = {
            "rid": "R_SO_4_{}".format(musicID),
            "threadId": "R_SO_4_{}".format(musicID),
            "pageNo": "1",
            "pageSize": "20",
            "cursor": "-1",
            "offset": "0",
            "orderType": "1"
        }
        response = Request(method, url, body, headers).post_url()
        try:
            if response.status_code == 200:
                text = json.loads(response.text)
                hotComments = text['data'].get('hotComments')
                totalCount = text['data'].get('totalCount')
                for item in hotComments:
                    content = item.get('content')
                    likedCount = item.get('likedCount')
                    config.logger1.info(
                        "get_song_detail 获取到歌曲信息，音乐ID:{}，音乐名:{}，歌手:{}，评论数:{}，单条评论点赞数:{}，评论:{}".format(musicID,
                                                                                                      musicName, singer,
                                                                                                      totalCount,
                                                                                                      likedCount,
                                                                                                      content))
                time.sleep(2)
            else:
                config.logger1.warning("get_song_detail 未获取到歌曲信息，返回结果为:{}".format(response.text))
        except Exception as e:
            config.logger1.exception("get_song_detail 处理返回结果数据异常，抛出信息:{}".format(e))


if __name__ == '__main__':
    # username = "qq528327016@126.com"
    # passwd = "chenfei537527"
    # loginType = "email"
    # account_id = login(loginType, username, passwd)
    # get_play_list(account_id)
    musicInfo = get_playlist_detail()
    get_song_detail(musicInfo)
