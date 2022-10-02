import win32clipboard as cb
import win32con
import pymysql
import time


# python3

class ClipboardHelper:

    def __init__(self):
        pass

    @staticmethod
    def get_text(last_blob):  # 读取剪切板
        cb.OpenClipboard()
        try:
            blob = cb.GetClipboardData(win32con.CF_TEXT)
        except:
            blob = last_blob
        finally:
            cb.CloseClipboard()
        return blob

    @staticmethod
    def set_text(blob):  # 写入剪切板
        cb.OpenClipboard()
        cb.EmptyClipboard()
        cb.SetClipboardData(win32con.CF_TEXT, blob)
        cb.CloseClipboard()


class MysqlHelper:

    def __init__(self, host, port, user, pw, db, table):
        self.host = host
        self.port = port
        self.user = user
        self.pw = pw
        self.db = db
        self.table = table
        self.id = -1

    def get_conn(self):  # 数据库连接
        while True:
            try:
                conn = pymysql.connect(host=self.host, port=int(self.port),
                                       user=self.user, password=self.pw,
                                       database=self.db, charset="utf8")
                return conn
            except:
                print("数据库连接失败")
                time.sleep(10)

    def get_text(self):  # 读取数据库
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('select id, copy from ' + self.table + ' order by id desc limit 1;')
            result = cur.fetchall()
            cur.close()
            conn.close()
            self.id = result[0][0]
            return result[0][1]
        except:
            print("数据库读取失败")

    def get_id(self):  # 读取数据库
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('select id from ' + self.table + ' order by id desc limit 1;')
            result = cur.fetchall()
            cur.close()
            conn.close()
            return result[0][0]
        except:
            print("数据库读取失败")

    def set_text(self, blob):  # 写入数据库
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('insert into ' + self.table + ' (copy) values (%s);', blob)
            cur.execute('select id from ' + self.table + ' order by id desc limit 1;')
            result = cur.fetchall()
            cur.close()
            conn.commit()
            conn.close()
            self.id = result[0][0]
        except:
            print("数据库写入失败")

    def init_table(self):
        conn = self.get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                'CREATE TABLE  ' +
                self.table +
                ' (id bigint(20) NOT NULL AUTO_INCREMENT,copy longblob,PRIMARY KEY (id)) ' +
                'ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;')
        except:
            print("检测到数据库 " + self.db + "." + self.table)
        else:
            print("数据库创建成功 " + self.db + "." + self.table)
        cur.close()
        conn.commit()
        conn.close()

    def is_changed(self):
        db_id = self.get_id()
        if self.id == -1:
            self.id = db_id
            result = False
        else:
            if self.id != db_id:
                result = True
            else:
                result = False
        return result
