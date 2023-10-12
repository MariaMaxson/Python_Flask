from flask import Flask , jsonify , request 
import pymysql
app=Flask(__name__)

def db_connections():
    conn = None
    try:
        conn = pymysql.connect(
            host="sql12.freesqldatabase.com",
            database="sql12646561",
            user="sql12646561",
            password="HcHuEDj7Jb",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(e)
    return conn        

@app.route ('/books', methods=['GET','POST','DELETE'])
def books():
    conn = db_connections()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor=conn.execute("SELECT * FROM book")
        books =[
            dict(id=row['id'],author=row['author'],language=row['language'],title=row['title'])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql="""INSERT INTO book(author , language , title) VALUES(%s,%s,%s)"""
        cursor = conn.execute(sql,(new_author,new_lang,new_title))
        conn.commit()
        return f"book with id : {cursor.lastrowid} created successfully"
    if request.method == 'DELETE':
        sql = """DELETE FROM book"""
        conn.execute(sql)
        conn.commit()
        return 'All records has been deleted', 200
    
@app.route('/book/<int:id>', methods=['GET','PUT','DELETE']) 
def single_book(id):
    conn = db_connections()
    cursor=conn.cursor()
    book = None
    if request.method =='GET':
        cursor.execute("SELECT * FROM book WHERE id=?",(id,))
        rows=cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book)    
            
    if request.method =='PUT':
        sql= """UPDATE book set title=?,
                                author=?,
                                language=?
                                where id=?"""
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        update_book ={
                    'id':id,
                    'author': author,
                    'language':language,
                    'title': title
        }
        conn.execute(sql,(title,language,author, id))
        conn.commit()
        return jsonify(update_book),200     
    if request.method == 'DELETE':
        sql = """DELETE FROM book WHERE id=?"""
        conn.execute(sql,(id,))
        conn.commit()
        return "the book with id:{} has been deleted".format(id),200        

if __name__ == '__main__':
    app.run(debug=True)