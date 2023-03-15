"""This module supplies a function decorator that gives a connection to a database."""
import functools
import sqlite3


def create_sqlite_connection(*args, **kwargs):
    return sqlite3.connect(*args, **kwargs)


class Connector:

    def __init__(self, *args, connection_factory=create_sqlite_connection, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.connection_factory = connection_factory
        self.conn = None

    def connect(self, f):
        """This decorator supplies a database connection as the first argument.

        This also manages the connection transaction, rolls back if an exception occurs,
        commits otherwise, and closes the connection in the end.
        """

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if self.conn is not None:
                print("Using existing connection...")
                return f(self.conn, *args, **kwargs)

            print("Connecting...")
            self.conn = self.connection_factory(*self.args, **self.kwargs)

            try:
                return_value = f(self.conn, *args, **kwargs)
            except Exception:
                self.conn.rollback()
                raise
            else:
                self.conn.commit()
            finally:
                self.conn.close()
                self.conn = None

            return return_value

        return wrapped
