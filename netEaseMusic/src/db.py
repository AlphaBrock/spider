# -*- coding: utf-8 -*-
import sqlite3
from config import DB_PATH


class Database(object):

    def __init__(self):
        self.con = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.init_db()

    def __del__(self):
        self.con.close()

    def init_db(self):
        cur = self.con.cursor()
        myMusicPlayList = '''CREATE TABLE IF NOT EXISTS myMusicPlayList
    (
      id  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      musicID VARCHAR(20),
      musicName VARCHAR(40),
      singer VARCHAR(40),
      musicPicUrl VARCHAR(100),
      totalCommentCount int(20),
      hotComment VARCHAR(256),
      hotCommentLikedCount int(20),
      date TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime'))
    )'''
        cur.execute(myMusicPlayList)
        self.con.commit()

    def run_query(self, cmd, param=None):
        cur = self.con.cursor()
        if param is None:
            cur.execute(cmd)
        else:
            cur.execute(cmd, param)
        self.con.commit()
        self.con.close()

    def inser_data(self, param):
        sql_cmd = "INSERT INTO myMusicPlayList(musicID, musicName, singer, musicPicUrl, totalCommentCount, hotComment, hotCommentLikedCount) VALUES (?,?,?,?,?,?,?)"
        self.run_query(sql_cmd, param)


if __name__ == '__main__':
    Database().init_db()
