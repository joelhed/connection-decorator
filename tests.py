import connection_decorator


connector = connection_decorator.Connector(":memory:")


@connector.connect
def create_test_table(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, value TEXT);")


@connector.connect
def add_test_item(conn, item):
    conn.execute("INSERT INTO test (value) VALUES (?)", (str(item), ))


@connector.connect
def get_all_test_items(conn):
    cur = conn.execute("SELECT * FROM test")
    return cur.fetchall()


@connector.connect
def test_database(conn):
    create_test_table()
    for item in ("thing one", "thing two"):
        add_test_item(item)

    conn.commit()

    print(get_all_test_items())


def main():
    test_database()


if __name__ == "__main__":
    main()
