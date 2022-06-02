"""This module supplies a function decorator that gives a connection to a database."""
import functools
import sqlite3


class Connector:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
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
            self.conn = sqlite3.connect(*self.args, **self.kwargs)

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
