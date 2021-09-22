import sqlite3


class DBHelper:
    def __init__(self, dbname="begreater.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS userData (user text, chains text, streakDate text)"
        useridx = "CREATE INDEX IF NOT EXISTS userIndex ON userData (user ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(useridx)
        self.conn.commit()

    def add_item(self, owner, chains, streakDate):
        stmt = "INSERT INTO userData (user, chains, streakDate) VALUES (?, ?, ?)"
        args = (owner, chains, streakDate)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def mod_streak(self, owner, streakDate):
        stmt = "UPDATE userData SET streakDate = ? WHERE user = ?"
        args = (streakDate, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def mod_chains(self, owner, chains):
        stmt = "UPDATE userData SET chains = ? WHERE user = ?"
        args = (chains, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, owner):
        stmt = "DELETE FROM userData WHERE user = ?"
        args = (owner, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_streak(self, owner):
        stmt = "SELECT streakDate FROM userData WHERE user = ?"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_chains(self, owner):
        stmt = "SELECT chains FROM userData WHERE user = ?"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]