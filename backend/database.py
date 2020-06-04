import sqlite3
from functools import wraps

from typing import Callable, Dict, Tuple


def _where_stmt(tblname, params: Dict, join_params: Tuple = ()):
    named_params_string = " AND ".join(
        ["{}.{key}=:{key}".format(tblname, key=k) for k in params if k not in join_params]
    )

    if not named_params_string:
        return ""

    return "WHERE {}".format(named_params_string)


class DB:
    def _join_with_mapper(f):
        @wraps(f)
        def wrapper(
            self,
            tblname: str,
            search_params: Dict,
            mappertbl: str = None,
            mappertbl_keys: Tuple = (),
        ) -> Callable:
            where_stmt = _where_stmt(tblname, search_params, mappertbl_keys)
            stmt = "SELECT * FROM {} {};".format(tblname, where_stmt)

            if mappertbl is not None:
                stmt = (
                    (
                        "SELECT {maintbl}.* from {maintbl} "
                        "INNER JOIN {jointbl} ON {jointbl}.{} = :{} "
                        "WHERE {maintbl}.id == {jointbl}.{} {where_stmt};"
                    )
                ).format(
                    # *args
                    *mappertbl_keys,
                    # **kwargs
                    maintbl=tblname,
                    jointbl=mappertbl,
                    where_stmt=where_stmt.replace("WHERE ", "AND "),
                )

            return f(self, stmt, search_params)

        return wrapper

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conn = sqlite3.connect(app.config["DATABASE_URL"], check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()

    def insert(self, tblname: str, data: Dict) -> bool:
        columns = ", ".join(data.keys())
        placeholders = f":{columns.replace(', ', ', :')}"
        stmt = "INSERT INTO {} ({}) VALUES ({})".format(tblname, columns, placeholders)

        try:
            return self.cursor.execute(stmt, data).lastrowid
        except (sqlite3.IntegrityError, sqlite3.ProgrammingError, sqlite3.OperationalError):
            # sqlite3.IntegrityError - unique constraint failed
            # sqlite3.ProgrammingError - params are not maching table column
            # sqlite3.OperationalError - columns and values are not matching
            # TODO: log error message
            self.conn.rollback()

        return 0

    def update(self, tblname, item_id: int, data: Dict):
        placeholders = ", ".join(["{key}=:{key}".format(key=k) for k in data])
        stmt = "UPDATE {} SET {} WHERE id=:id".format(tblname, placeholders)
        try:
            return self.cursor.execute(stmt, {**data, "id": item_id}).lastrowid
        except (sqlite3.IntegrityError, sqlite3.ProgrammingError, sqlite3.OperationalError):
            # TODO: log error message
            self.conn.rollback()

    def delete(self, tblname: str, id: int = None):
        # NOTE: if id is empty it will remove all items in table
        # NOTE: SQL does on delete cascade, but it should be considered carefully
        #       because once deleted it's hard to restore if at all
        stmt = "DELETE FROM {} {}".format(tblname, ("WHERE id=?" if id is not None else ""))
        return self.cursor.execute(stmt, (id,)).rowcount

    @_join_with_mapper
    def filter_by(self, stmt: str, search_params: Dict) -> sqlite3.Cursor:
        # TODO: Add order_by in order to be consistent
        return self.cursor.execute(stmt, search_params)
