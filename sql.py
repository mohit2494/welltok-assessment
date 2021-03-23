create_channels_sql = '''CREATE TABLE IF NOT EXISTS channels
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name text UNIQUE NOT NULL,
                code text UNIQUE NOT NULL,  
                created TIMESTAMP, 
                updated TIMESTAMP, 
                deleted INTEGER
                )'''

create_range_sql = '''CREATE TABLE IF NOT EXISTS range
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                begin INTEGER, 
                ending INTEGER,
                created TIMESTAMP,
                updated TIMESTAMP,
                deleted INTEGER
                )'''

create_base_fee_sql = '''CREATE TABLE IF NOT EXISTS base_fee
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                channel_id INTEGER, 
                price FLOAT,
                created TIMESTAMP,
                updated TIMESTAMP,
                deleted INTEGER,
                FOREIGN KEY(channel_id) REFERENCES channels(id)
                )'''

create_trans_fee_sql = '''CREATE TABLE IF NOT EXISTS trans_fee
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                channel_id INTEGER,
                range_id INTEGER,
                price FLOAT,
                created TIMESTAMP,
                updated TIMESTAMP,
                deleted INTEGER,
                FOREIGN KEY(channel_id) REFERENCES channels(id),
                FOREIGN KEY(range_id) REFERENCES range(id)
                )'''