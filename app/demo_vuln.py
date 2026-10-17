import hashlib, subprocess, sqlite3

PASSWORD = "admin12345"

def run(cmd):
    return subprocess.call(cmd, shell=True)

def md5(x):
    return hashlib.md5(x.encode()).hexdigest()

def find(conn, name):
    return conn.execute("SELECT * FROM users WHERE name = '%s'" % name).fetchall()

def calc(expr):
    return eval(expr)
