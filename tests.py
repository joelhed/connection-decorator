import connection_decorator


connector = connection_decorator.Connector("db.db")

    
@connector.connect
def get_all_persons(conn):
    cur = conn.execute("select * from person;")
    return cur.fetchall()


@connector.connect
def get_teacher_ids_for_person(conn, person_id):
    cur = conn.execute(
        "select teacher_id from student_relation where student_id=?",
        (person_id, )
    )
    return cur.fetchall()


def main():
    for person in get_all_persons():
        print(person)
        print("teachers:", get_teacher_ids_for_person(person[0]))


if __name__ == "__main__":
    main()
