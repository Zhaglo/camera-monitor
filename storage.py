import sqlite3

from contextlib import closing


def init_db():
    with closing(sqlite3.connect('checks.db')) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS checks (
                    check_id TEXT PRIMARY KEY NOT NULL,
                    status TEXT NOT NULL
                )
            """)


def create_check(check_id):
    with closing(sqlite3.connect('checks.db')) as connection:
        with connection:
            connection.execute(
                'INSERT INTO checks (check_id, status) VALUES (?, ?)',
                (check_id, 'pending')
            )


def get_check(check_id):
    with closing(sqlite3.connect('checks.db')) as connection:
        cursor = connection.execute(
            'SELECT check_id, status FROM checks WHERE check_id = ?',
            (check_id,)
        )
        return cursor.fetchone()


def update_check_status(check_id, status):
    with closing(sqlite3.connect('checks.db')) as connection:
        with connection:
            cursor = connection.execute(
                'UPDATE checks SET status = ? WHERE check_id = ?',
                (status, check_id)
            )
            return cursor.rowcount == 1


if __name__ == '__main__':
    init_db()