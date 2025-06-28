import mysql.connector

cn = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)

cr = cn.cursor()

cr.execute('CREATE DATABASE IF NOT EXISTS mv_managment')

sq1 = '''CREATE TABLE IF NOT EXISTS mv_managment.movie(
    mv_id INT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    activ INT NOT NULL,
    m_theater VARCHAR(30)
)engine = innodb;'''
cr.execute(sq1)

sq2 = '''CREATE TABLE IF NOT EXISTS mv_managment.booking(
    id INT PRIMARY KEY AUTO_INCREMENT,
    b_mvid INT NOT NULL,
    b_theater VARCHAR(30) NOT NULL,
    b_time INT NOT NULL,
    seat INT NOT NULL,
    FOREIGN KEY (b_mvid) REFERENCES movie(mv_id)
)engine = innodb;'''
cr.execute(sq2)

cn.close()
