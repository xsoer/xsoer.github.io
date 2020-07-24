#!/usr/bin/env python
# -*- coding: utf8 -*-

import pymysql
from DBUtils.PooledDB import PooledDB
from contextlib import closing


class DB:
    def __init__(self, host, user, pwd, db, port=3306):
        self.pool = PooledDB(pymysql,
                            mincached=3,
                            maxcached=10,
                            host=host,
                            port=port,
                            user=user,
                            password=pwd,
                            db=db,
                            charset='utf8')

    def __get_conn(self):
        return self.pool.connection()

    def select_one(self, sql, params=None, db=None):
        conn = self.__get_conn()
        cur = conn.cursor()
        cur.execute(sql, params)
        results = cur.fetchone()
        return results

    # 查
    def select_all(self, sql, params=None, db=None):
        with closing(self.__get_conn()) as conn, closing(conn.cursor()) as cur:
            cur.execute(sql, params)
            results = cur.fetchall()
            return results

    def select_dict(self, sql, params=None, db=None):
        with closing(self.__get_conn()) as conn, closing(conn.cursor(pymysql.cursors.DictCursor)) as cur:
            cur.execute(sql, params)
            results = cur.fetchall()
            return results

    # 增删改
    def execute(self, sql, params=None, db=None):
        with closing(self.__get_conn()) as conn, closing(conn.cursor()) as cur:
            cur.execute(sql, params)
            conn.commit()

    # 自增，返回id
    def insert_one(self, sql, params=None, db=None):
        with closing(self.__get_conn()) as conn, closing(conn.cursor()) as cur:
            cur.execute(sql, params)
            id_ = conn.insert_id()
            conn.commit()
            return id_

    # datas里的多个数据，字段要一致，没有的补None
    def insert_many(self, table, datas):
        if not datas:
            return None
        key_list = datas[0].keys()
        params = []
        for data in datas:
            param = []
            for key in key_list:
                param.append(data[key])
            params.append(param)
        cols = "`" + "`,`".join(key_list) + "`"
        vals1 = "(" + ",".join(["%s"] * len(key_list)) + ")"
        sql = "insert into %s (%s) values %s" % (table, cols, vals1)
        self._insert_many(sql, params)

    def insert_data(self, table, dict_d):
        (cols, vals, params) = self._get_column_and_param(dict_d)
        sql = "insert into %s (%s) values (%s)" % (table, cols, vals)
        return self.insert_one(sql, params)

    def update_data(self, table, dict_d, where_case):
        col_list = []
        params = []
        for k in dict_d:
            if dict_d[k] is not None:
                col_list.append("`" + k + "`=%s")
                params.append(dict_d[k])
        cols = ",".join(col_list)
        sql = "update %s set %s where %s" % (table, cols, where_case)
        self.execute(sql, params)

    # 取数据字段及数据集，方便插入或更新操作；输入dict的key值需与数据库字段对应，date类型数据转成str
    def _get_column_and_param(self, dict_d):
        col_list = []
        params = []
        for k in dict_d:
            if dict_d[k] is not None:
                col_list.append("`" + k + "`")
                params.append(dict_d[k])
        cols = ",".join(col_list)
        vals = ",".join(["%s"] * len(col_list))
        return (cols, vals, params)

    def _insert_many(self, sql, params=None, db=None):
        with closing(self.__get_conn()) as conn, closing(conn.cursor()) as cur:
            cur.executemany(sql, params)
            conn.commit()
