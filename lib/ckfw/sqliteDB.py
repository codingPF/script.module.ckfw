# -*- coding: utf-8 -*-
"""
The local SQlite database module
SPDX-License-Identifier: MIT
"""

# pylint: disable=too-many-lines,line-too-long
import time
import sqlite3
from . import utils as pyUtils


class SqliteDB(object):
    """
    The local SQlite database class

    """

    def __init__(self, pAddon, databaseFilename):
        self.addon = pAddon
        self.logger = self.addon.createLogger('SqliteDB')
        self.databaseFilename = databaseFilename
        self.logger.debug('DB File {}', self.databaseFilename)
        self.conn = None

    def reset(self):
        try:
            self.exit()
        except Exception as err:
            pass
        rt = pyUtils.file_remove(self.databaseFilename)
        self.conn = None
        self.logger.debug('DB Reset {}', rt)

    def getConnection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.databaseFilename, timeout=60)
            self.conn.execute('pragma synchronous=off')
            self.conn.execute('pragma journal_mode=off')
            self.conn.execute('pragma page_size=65536')
            self.conn.execute('pragma encoding="UTF-8"')
        return self.conn

    def exit(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def execute(self, aStmt, aParams=None):
        """ execute a single sql stmt and return the resultset """
        start = time.time()
        self.logger.debug('query: {} params {}', aStmt, aParams)
        cursor = self.getConnection().cursor()
        if aParams is None:
            cursor.execute(aStmt)
        else:
            cursor.execute(aStmt, aParams)
        rs = cursor.fetchall()
        cursor.close()
        self.logger.debug('execute: {} rows in {} sec', len(rs), time.time() - start)
        return rs

    def executeUpdate(self, aStmt, aParams):
        """ execute a single update stmt and commit """
        cursor = self.getConnection().cursor()
        if aParams is None:
            cursor.execute(aStmt)
        else:
            cursor.execute(aStmt, aParams)
        rs = cursor.rowcount
        self.logger.debug(" rowcount executeUpdate {}" , rs)
        cursor.close()
        self.getConnection().commit()
        return rs

'''
    def isInitialized(self):
        rt = False
        try:
            sql = 'select 0 from audiofile where 1=0'
            rs = self.execute(sql, None)
            rt = True
        except Exception as err:
            pass
        return rt

    def create(self):
        self.execute("""
            CREATE TABLE audiofile (
            broadcastId INT, episodeId INT NOT NULL PRIMARY KEY, episodeTitle VARCHAR(256),
            episodeDuration INT, episodeAired INT, episodeDescription VARCHAR(256), 
            episodeUrl VARCHAR(256), episodeImage VARCHAR(256), created INT)"""
                     , None)

    def setLastLoadEpisode(self, pBroadcast):
        sql = "update audiofile set created = ? where broadcastId = ?"
        rs = self.executeUpdate(sql, (int(time.time()), pBroadcast))
        return rs

    def deleteCategory(self):
        deleteStmt = "DELETE FROM category"
        return self.executeUpdate(deleteStmt, None)

    def addCategory(self, pKey, pParams):
        rs = 0
        deleteStmt = 'SELECT 1 FROM category WHERE broadcastId = ?'
        if len(self.execute(deleteStmt, (pKey,))) == 0:
            sql = "INSERT INTO category values (?,?,?,?,?,?,?,?,?,?,?)"
            rs = self.executeUpdate(sql, pParams)
        return rs
'''
