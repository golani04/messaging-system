import sqlite3


class DB:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conn = sqlite3.connect(app.config["DATABASE_URL"])
        self.cursor = self.conn.cursor()
