"""
This module retrieves the details of an object from a database and displays them 
in a formatted table. The function 'object_details' takes an integer ID parameter 
and displays the object's details with the matching ID using SQL queries to 
extract data from the 'lux.sqlite' database.

The table.py module is imported to format and display the results in a readable way.

The following constants are defined at the beginning of the module:
NAT_IND: the index of the nationality in the database
CLS_IND: the index of the classification in the database
INFO_IND1: the index of the first information field in the database
INFO_IND2: the index of the second information field in the database
COL_NUM: the number of columns in the database table

The 'print_output' helper function takes two parameters, a string and a table, 
and prints them to standard output.

Exceptions are handled using a try-except block, with any caught exceptions printed to standard 
error and the script exiting with a non-zero status.
"""
from sys import stderr
import sys
from contextlib import closing
from sqlite3 import connect
from table import Table

# INITIALIZE CONSTANT
NAT_IND = 3
CLS_IND = 5
INFO_IND1 = 6
INFO_IND2 = 7
COL_NUM = 8

FORMAT_FLAG = ["w", "w", "p", "w"]
FORMAT_SEP = ","
LABEL = ["Label"]
PRODUCED_BY =  ["Part", "Name", "Nationalities", "Timespan"]
CLASSIFIERS = ["Classifiers"]
INFORMATION = ["Type", "Name"]
DATABASE = 'file:lux.sqlite?mode=ro'

# ----------------------------------------------------
def replace_null(list1):
    """ This function takes a 2D list as a parameter, 
        and replaces the null element with empty for each element in the 2D list """
    for i, row in enumerate(list1):
        for j, element in enumerate(row):
            if element is None:
                list1[i][j] = ""

# print helper
def print_output(query, header, cursor, is_agent = False):
    """ This function is a customize print function.
        If the flag is_agent is on, print the table with specific format"""
    cursor.execute(query)
    row = cursor.fetchone()
    list1 = []
    while row is not None:
        row = list(row)
        list1.append(row)
        row = cursor.fetchone()
    replace_null(list1)
    if is_agent :
        table = Table(header, list1, format_str = FORMAT_FLAG, preformat_sep = FORMAT_SEP)
    else:
        table = Table(header, list1)
    print(table)
    print()

# ----------------------------------------------------

def object_details(temp_id):
    """
    Retrieves and prints the details of an object with the given ID from art gallery database.
    
    Arguments:
    - temp_id: An integer representing the ID of the object to retrieve information for.
    
    Returns:
    - Details of the object to the console.
    
    
    Raises an exception and exits the program if there is an error connecting to or querying 
    the database.
    """
    database_url = DATABASE
    try:
        with connect(database_url, isolation_level=None,
        uri=True) as connection:

            with closing(connection.cursor()) as cursor:
                # Create a SQL query
                stmt_str = f"""
                            SELECT label FROM objects
                            WHERE objects.id = {temp_id}"""
                # label
                print_output(stmt_str, LABEL, cursor)
                # produce by
                stmt_str = f"""
                            SELECT part,
                                name,
                                group_concat(DISTINCT descriptor) AS descriptor,
                                CASE WHEN end_date > date("now") THEN strftime('%Y', begin_date) || "-" 
                                WHEN begin_date is NULL and end_date is not NULL THEN "-"||(strftime('%Y', end_date))
                                WHEN begin_date is NULL and end_date is NULL THEN "-"
                                WHEN begin_date is not NULL and end_date is NULL then (strftime('%Y', begin_date)) || "-" 
                                ELSE (strftime('%Y', begin_date)) || "-" || (strftime('%Y', end_date)) END time_span
                            FROM objects
                                JOIN
                                productions ON objects.id = productions.obj_id
                                LEFT JOIN
                                agents ON agents.id = productions.agt_id
                                LEFT JOIN
                                agents_nationalities an ON an.agt_id = agents.id
                                LEFT JOIN
                                nationalities n ON n.id = an.nat_id
                            GROUP BY agents.name, objects.id
                            HAVING objects.id= {temp_id}"""

                print("Produced By:")
                print_output(stmt_str, PRODUCED_BY,cursor, True)
                # Classification
                stmt_str = f"""
                            SELECT group_concat(DISTINCT cls.name) 
                            FROM objects o
                                LEFT JOIN
                                objects_classifiers ocls ON ocls.obj_id = o.id
                                LEFT JOIN
                                classifiers cls ON cls.id = ocls.cls_id
                            WHERE o.id = {temp_id}"""

                print_output(stmt_str, CLASSIFIERS, cursor)
                # # Information
                stmt_str = f"""
                            SELECT type,
                                content
                            FROM objects o
                                LEFT JOIN
                                [references] r ON r.obj_id = o.id
                            where o.id = {temp_id}"""
                print("Information: ")
                print_output(stmt_str, INFORMATION, cursor)

    except Exception as ex:
        print(ex, file=stderr)
        sys.exit(1)
