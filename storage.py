import sqlite3

from contextlib import closing


def init_db():
    with closing(sqlite3.connect('checks.db')) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS checks (
                    check_id TEXT PRIMARY KEY NOT NULL,
                    status TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    result_json TEXT
                )
            """)


def create_check(check_id, request_json):
    with closing(sqlite3.connect('checks.db')) as connection:
        with connection:
            connection.execute(
                'INSERT INTO checks (check_id, status, request_json) VALUES (?, ?, ?)',
                (check_id, 'pending', request_json)
            )


def get_check(check_id):
    with closing(sqlite3.connect('checks.db')) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(
            'SELECT check_id, status, request_json, result_json FROM checks WHERE check_id = ?',
            (check_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row is not None else None


def update_check_status(check_id, status):
    with closing(sqlite3.connect('checks.db')) as connection:
        with connection:
            cursor = connection.execute(
                'UPDATE checks SET status = ? WHERE check_id = ?',
                (status, check_id)
            )
            return cursor.rowcount == 1


def complete_check(check_id, result_json):
    with closing(sqlite3.connect('checks.db')) as connection:
        with connection:
            cursor = connection.execute(
                'UPDATE checks SET status = ?, result_json = ? WHERE check_id = ?',
                ('completed', result_json, check_id)
            )
            return cursor.rowcount == 1


if __name__ == '__main__':
    init_db()