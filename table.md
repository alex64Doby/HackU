# Users
列名|データ型|列制約
--|--|--
user_id | CHAR(48) | PRIMARY KEY
user_name | CHAR(16) | NOT NULL
prefecture_id | INT | NOT NULL
point | INT | DEFAULT 0

# Prefectures
列名|データ型|列制約
--|--|--
prefecture_id | INT | PRIMARY KEY
prefecture_name | CHAR(16) | NOT NULL

# Connections
列名|データ型|列制約
--|--|--
connection_id | CHAR(48) | PRIMARY KEY
user_id1 | CHAR(48) | NOT NULL
user_id2 | CHAR(48) | NOT NULL
status | CHAR(48) | NOT NULL
created_by | DATETIME | DEFAULT CURRENT_TIME
updated_by | DATETIME | DEFAULT CURRENT_TIME
point | INT | NOT NULL
