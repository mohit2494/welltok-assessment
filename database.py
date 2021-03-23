import os
from setup import Setup
import sqlite3
import logging
import datetime
import heapq
import sql
logger = logging.getLogger(__name__)

class DBHelper(object):
    DATABASE_NAME = "campaign.db"
    RECORD_VISIBLE = 0
    RECORD_HIDDEN = 1
    TABLE_NAMES = ["channels", "range", "base_fee", "trans_fee"]
    init_failed = False

    def __init__(self, config_file=None):
        try:
            self.con = sqlite3.connect(self.DATABASE_NAME)
            self.con.isolation_level = None
            self.setup_object = Setup(config_file=config_file)
        except Exception as e:
            log.debug(e)
            init_failed = True

    def reload(self):
        path = "./"+self.DATABASE_NAME
        if os.path.exists(path):
            os.remove(path)
        self.con = sqlite3.connect(self.DATABASE_NAME)
        self.create_and_insert()

    def create_tables(self):
        logger.debug('starting to create tables')
        try:
            cur = self.con.cursor()
            cur.execute('begin')
            for table in self.TABLE_NAMES:
                cur.execute(getattr(sql, 'create_'+str(table)+'_sql'))
                logger.debug('Table '+table+' created')
        except Exception as e:
            self.con.rollback()
            logger.debug(
                'Error creating tables'+str(e))
            raise Exception(
                'Internal Error. Please contact welltok tools Team: welltoktools@gmail.com')
        self.con.commit()

    def insert_into_tables(self):
        validated_data = self.setup_object.read_config()
        try:
            cur = self.con.cursor()
            cur.execute('begin')
            for tablename in self.TABLE_NAMES:
                method = getattr(self, 'insert_'+tablename)
                method(data=validated_data[tablename], cur=cur)
        except Exception as e:
            self.con.rollback()
            logger.debug(
                'Error inserting data into tables. Please validate config.json.'+str(e))
            raise Exception(
                'Error in inserting data from config.json. Please validate or contact welltok tools Team: welltoktools@gmail.com')
        self.con.commit()

    def create_and_insert(self):    
        self.create_tables()
        self.insert_into_tables()

    def insert_channels(self, data=None, cur=None):
        for id, val in data.items():
            name = val['name']
            code = val['code']
            self.insert_into_channels_table(cur, int(id), name, code)

    def insert_range(self, data=None, cur=None):
        for id, val in data.items():
            start, end = val['from'], val['to']
            self.insert_into_range_table(cur, id, start, end)

    def insert_trans_fee(self, data=None, cur=None):
        for id, val in data.items():
            range_id = int(val['range_id'])
            channel_id = int(val['channel_id'])
            price = float(val['price'])
            self.insert_into_transfee_table(
                cur, id, range_id, channel_id, price)

    def insert_base_fee(self, data=None, cur=None):
        for id, val in data.items():
            channel_id = int(val['channel_id'])
            price = float(val['price'])
            self.insert_into_basefee_table(cur, id, channel_id, price)

    def insert_into_channels_table(self, cur, id, name, code):
        now = datetime.datetime.now()
        cur.execute(
            "insert into channels(id, name, code, created, updated, deleted) values (?, ?, ?, ?, ?, ?)",
            (id, name, code, now, now, self.RECORD_VISIBLE))

    def insert_into_basefee_table(self, cur, id, channel_id, price):
        now = datetime.datetime.now()
        cur.execute(
            "insert into base_fee(id, channel_id, price, created, updated, deleted) values (?, ?, ?, ?, ?, ?)",
            (id, channel_id, price, now, now, self.RECORD_VISIBLE))

    def insert_into_range_table(self, cur, id, start, end):
        now = datetime.datetime.now()
        cur.execute(
            "insert into range(id, begin, ending, created, updated, deleted) values (?, ?, ?, ?, ?, ?)",
            (id, start, end, now, now, self.RECORD_VISIBLE))

    def insert_into_transfee_table(self, cur, id, range_id, channel_id, price):
        now = datetime.datetime.now()
        cur.execute(
            "insert into trans_fee(id, channel_id, range_id, price, created, updated, deleted) values (?, ?, ?, ?, ?, ?, ?)",
            (id, channel_id, range_id, price, now, now, self.RECORD_VISIBLE))

    def get_channel_id_by_code(self, code):
        if not code:
            return None
        cur = self.con.cursor()
        cur.execute("select id from channels where code=?",
                    (code,))
        row = cur.fetchone()
        return row[0] if row else None

    def get_all_ranges(self):
        cur = self.con.cursor()
        cur.execute("select id,begin,ending from range")
        row = cur.fetchall()
        return row if row else None

    def get_range_id(self, audience_size):
        cur = self.con.cursor()
        cur.execute("select id from range where ? >= begin and ? <=ending",
                    (audience_size, audience_size,))
        row = cur.fetchone()
        if not row:
            raise Exception('Audience size out of range')
        return row[0]

    def get_base_fee(self, channel_id=None):
        if not channel_id:
            return None
        cur = self.con.cursor()
        cur.execute(
            "select price from base_fee where channel_id=?", (channel_id,))
        row = cur.fetchone()
        return row[0] if row else None

    def get_trans_fee(self, range_id=None, channel_id=None):
        if not (range_id and channel_id):
            return None
        cur = self.con.cursor()
        cur.execute(
            "select price from trans_fee where channel_id=? and range_id=?", (channel_id, range_id,))
        row = cur.fetchone()
        return row[0] if row else None

    def get_channel_name(self, channel_id=None):
        if not channel_id:
            return None
        cur = self.con.cursor()
        cur.execute("select name from channels where id=?", (channel_id,))
        row = cur.fetchone()
        return str(row[0]) if row else None

    def is_data_present(self, tablename):
        if not tablename or tablename.strip() == "":
            return False
        try:
            cur = self.con.cursor()
            cur.execute("select * from "+tablename.strip().lower())
            rows = cur.fetchall()
            return len(rows) > 0
        except Exception as e:
            logger.debug(e)
            return False

    def check_tables_exist(self):
        return all([self.is_data_present(tablename) for tablename in self.TABLE_NAMES])
