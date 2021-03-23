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
    cur.execute("select price from trans_fee where channel_id=? and range_id=?",(channel_id, range_id,))
    row = cur.fetchone()
    return row[0] if row else None

def get_channel_name(self, channel_id=None):
    if not channel_id:
        return None
    cur = self.con.cursor()
    cur.execute("select name from channels where id=?",(channel_id,))
    row = cur.fetchone()
    return str(row[0]) if row else None

def is_data_present(self, tablename):
        if not tablename or tablename.strip()=="":
            return False
        try:
            cur = self.con.cursor()
            cur.execute("select * from "+tablename.strip().lower())
            rows = cur.fetchall()
            return len(rows)>0
        except Exception as e:
            return False