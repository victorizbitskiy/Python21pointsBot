import sqlite3


class DBHelp:

    def __init__(self, dbname="games.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (chat_id integer PRIMARY KEY, points_user integer NOT NULL, " \
               "points_bot integer NOT NULL)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_points(self, chat_id, points_user, points_bot):
        stmt = "UPDATE items SET points_user = points_user + (?), points_bot = points_bot + (?) WHERE chat_id = (?)"
        args = (points_user, points_bot, chat_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_item(self, chat_id, points_user, points_bot):
        stmt = "INSERT INTO items (chat_id, points_user, points_bot) VALUES (?, ?, ?)"
        args = (chat_id, points_user, points_bot)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, chat_id):
        stmt = "DELETE FROM items WHERE chat_id = (?)"
        args = (chat_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_item(self, chat_id):
        stmt = "SELECT points_user, points_bot FROM items WHERE chat_id = (?)"
        args = (chat_id,)
        t = [x for x in self.conn.execute(stmt, args)]
        return t[0][0], t[0][1]
