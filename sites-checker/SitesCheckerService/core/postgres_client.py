
from os import sys, path
import logging
import psycopg2
import psycopg2.extras

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

logger = logging.getLogger('SitesCheckerService')
RETRY_DELAY_IN_SECONDS = 5


class PostgresClient:

    def __init__(self, dsn=None):
        if dsn:
            self.dsn = dsn
        else:
            raise TypeError('check error : missing dsn and no parameters')
        try:
            self.conn = psycopg2.connect(dsn=self.dsn)
        except psycopg2.ProgrammingError as ex:
            raise ex


    def prepare(self, query, data):
        cursor = self.conn.cursor()
        return cursor.mogrify(query, data)

    def select(self, query):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        for result in cursor.fetchall():
            yield result
        cursor.close()


    def insert_list_of_dictionaries(self, data, tablename, cols):
        '''Insert Python list of dictionaries into PSQL database'''
        with self.conn.cursor() as cursor:
            cursor.copy_from(data, tablename, cols)
            self.conn.commit()


    def delete_rows(self, sql=None):
        if not sql:
            return
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except psycopg2.DatabaseError as ex:
            raise ex
        else:
            self.conn.commit()
        finally:
            cursor.close()


    def empty_table(self, table):
        sql ='TRUNCATE {0} RESTART IDENTITY; ALTER SEQUENCE {0}_id_seq RESTART WITH 1;'.format(table)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except psycopg2.DatabaseError as ex:
            raise ex
        else:
            self.conn.commit()
        finally:
            cursor.close()


    def insert(self, sql):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(sql)
            for result in cursor.fetchall():
                yield result
        except psycopg2.DatabaseError as ex:
            raise ex
        else:
            self.conn.commit()
        finally:
            cursor.close()


    def insert_no_msg(self, sql):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(sql)
        except psycopg2.DatabaseError as ex:
            raise ex
        else:
            self.conn.commit()
        finally:
            cursor.close()
