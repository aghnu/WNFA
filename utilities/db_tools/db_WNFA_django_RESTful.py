import sqlite3 as sql
import sys, os
import math

def store_img_data(name, data, path):
    with open(path + '/' + name + 'jpg', 'wb') as bf:
        bf.write(data)

def main():
    # connect
    dbPath = os.path.abspath(os.path.split(__file__)[0] + "/" + sys.argv[1])
    imgPath = os.path.abspath(os.path.split(__file__)[0] + "/" + sys.argv[2])
    con = sql.connect(dbPath)
    cur = con.cursor()

    print(imgPath)
    print(dbPath)

    # extract
    row_count = 8
    cur.execute('SELECT COUNT(*) FROM WNFA_text_to_art_art;')
    num_rows = cur.fetchall()[0][0]
    for row in range(math.ceil(num_rows/row_count)):
        cur.execute('SELECT id,data FROM WNFA_text_to_art_art LIMIT ? OFFSET ?;', (row_count, row * row_count))
        for record in cur.fetchall():
            id = record[0]
            data = record[1]
            name = str(id)
            store_img_data(name, data, imgPath)
            
    con.close()
main()