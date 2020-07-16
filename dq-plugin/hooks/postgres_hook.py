from airflow.hooks import PostgresHook
from contextlib import closing


def run_returning(hook, sql, parameters=None):
    with closing(hook.get_conn()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute(sql, parameters)
            res = cur.fetchone()

        conn.commit()

    return res

setattr(PostgresHook, 'run_returning', run_returning)
