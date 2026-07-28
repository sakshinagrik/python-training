import sqllite3
def init_db();
    conn = sqlite3.connect('instance coacing.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTs students
    (id INTIGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT ,
    course TEXT,
    address TEXT,
    admission_date DATE)''')
    conn.commit()
    conn.close()
 init_db()