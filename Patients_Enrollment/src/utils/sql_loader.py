"""
Load a SQL query from a .sql file.
This function reads the contents of a SQL file
and returns the query as a string so it can be
executed by a database engine or cursor.

Parameters
----------
path : str
Relative or absolute path to the SQL file.
Returns
----------
SQL query string loaded from the file.
"""
def load_sql(path):
    with open(path, "r") as file:
        return file.read()