from mysql.connector import MySQLConnection


class Easql(MySQLConnection):

    def query(self, stmt, *args, update=False, dictionary=True, **kwargs):
        """Opens connection, performs query, and closes connection.

        Args:
            stmt (str): The mysql statement.
            update (bool, optional): Should I commit? Defaults to False.
            dictionary (bool, optional): Do I want dictionary results? Defaults to True.
        """
        if not self.is_connected():
            self.reconnect()
        with self.cursor(dictionary=dictionary) as cursor:
            cursor.execute(stmt, args, kwargs)
            if update:
                self.commit()
            data = cursor.fetchall()
        self.disconnect()
        return data

    def procedure(self, proc: str, *args, update=False, dictionary=True, **kwargs):
        """Opens connection, performs procedure, and closes connection.

        Args:
            proc (str): The procedure.
            update (bool, optional): Should I commit? Defaults to False.
            dictionary (bool, optional): Do I want dictionary results? Defaults to True.
        """
        if not self.is_connected():
            self.reconnect()
        with self.cursor(dictionary=dictionary) as cursor:
            cursor.callproc(proc, args, **kwargs)
            if update:
                self.commit()
            data = list(cursor.stored_results())
            if dictionary:
                for i, item in enumerate(data):
                    data[i] = item.fetchall()
        self.disconnect()
        return data

    def update(self, query, *args, **kwargs):
        self.query(query, *args, update=True, **kwargs)
