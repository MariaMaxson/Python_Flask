import pymysql

conn = pymysql.connect(
    host="sql12.freesqldatabase.com",
    database="sql12646561",
    user="sql12646561",
    password="HcHuEDj7Jb",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)
curser = conn.cursor()
sql_query = """CREATE TABLE BOOK(
    id integer primary key,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
)"""
curser.execute(sql_query)
conn.close()