from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path=Path(__file__).parent / 'employee_events.db'
# print("The file path is:", db_path)


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, sql_query:str):
        
        with connect(self.db_path) as conn:
            df = pd.read_sql_query(sql_query, conn)
        return df

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, sql_query:str):
        connection = connect(self.db_path)
        cursor = connection.cursor()
        result = cursor.execute(sql_query).fetchall()
        connection.close()
        return result
    
# # A simple class that uses the mixin and supplies the db_path
# class Repo(QueryMixin):
#     def __init__(self, db_path: Path):
#         self.db_path = str(db_path)  # sqlite3.connect accepts str paths

# repo = Repo(db_path)

# # Run your query and print the result
# df = repo.query(
#     "SELECT DISTINCT manager_name FROM team;"
# )
# print(df)
 
 # Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query
