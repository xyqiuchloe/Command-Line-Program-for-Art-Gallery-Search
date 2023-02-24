"""
This module retrieves the detail of an object from a database and displays them 
in a formatted table. The function module defines a set of functions that
takes an integer ID parameter and displays the object's details with the matching
ID using SQL queries to extract data from the 'lux.sqlite' database.
The table.py module is imported to format and display the results in a readable way.

The following constants are defined at the beginning of the module:
AGT_IND: the index of the agent in the database
DEP_IND: the index of the department in the database
CLS_IND: the index of the classification in the database

Exceptions are handled using a try-except block.
"""
# import argparse
from sys import stderr
import sys
from contextlib import closing
from sqlite3 import connect
from table import Table
# INITIALIZE CONSTANT
AGT_IND = 2
DEP_IND = 4
CLS_IND = 5
DATABASE = 'file:lux.sqlite?mode=ro'
FORMAT_FLAG = ["w", "w", "w", "w", "w", "p"]
FORMAT_SEP = ","
HEADER = ["ID", "Label", "Produced By", "Date", "Member of", "Classified As"]

def filter_term2(*args): # args: eg.[["dep", "Yale Gallary"], ["agt", "Van Gogh"]]
    """
    The function filter_term2 takes variable number of arguments and returns a string of 
    SQL query with having clause to filter and order the search result.

    Usage:
    - filter_term2([["dep", "Yale Gallary"], ["agt", "Van Gogh"]])

    Arguments:
    - *args: A list of lists where each inner list contains two string elements. 
        The first element represents the search filter category, and the second element 
        represents the search term.

    Returns:
    - A string that represents the SQL query with having clause to filter and order the 
    search result.
    """
    temp_str = ""
    temp = []
    # take the first having clause
    if len(args) > 0:
        temp.append(get_option_name(args[0][0]))
        temp_str += f"HAVING {get_option_name(args[0][0])} like '%{args[0][1]}%' "
    # rest of having clause
    for i in range(1, len(args)):
        temp.append(get_option_name(args[i][0]))
        temp_str += f"AND {get_option_name(args[i][0])} like '%{args[i][1]}%' "
    # order filter
    temp_str += "ORDER BY label ASC, temp1.date ASC "
    if "agents_name" in temp:
        temp_str += ", temp1.name ASC"
        temp.remove("agents_name")
    if "departments_name" in temp:
        temp_str += ", departments_name ASC "
        temp.remove("departments_name")
    if "classifiers_name" in temp:
        temp_str += ", classifiers_name ASC "
        temp.remove("classifiers_name")
    temp_str += " limit 1000"
    return temp_str

def get_option_name(temp_str):
    """
    This function takes a string as input and returns the corresponding option name 
    based on the string value.

    Arguments:
    - temp_str: A string representing an option. It can be one of the following values:
        - 'dep': Represents the departments option.
        - 'agt': Represents the agents option.
        - 'cls': Represents the classification option.
        - 'label': Represents the label option.

    Returns:
    - A string representing the corresponding option name if the input string matches 
    any of the predefined values.
    - Otherwise, it returns None.
    """
    if temp_str == "dep":
        return "departments_name"
    if temp_str == "agt":
        return "agents_name"
    if temp_str == "cls":
        return "classifiers_name"
    if temp_str == "label":
        return "objects.label"
    return None



def get_filtered_objects(temp_filter):
    """
    Retrieves and prints the details of  objects from a database that satisfy several given
    filter conditions, and then displays the results in a formatted table.
    
    Arguments:
    - temp_filter: A string representing the filter condition.
    
    Raises an exception and exits the program if there is an error connecting to or querying 
    the database.
    """
    database_url = DATABASE
    try:
        with connect(database_url, isolation_level=None,
        uri=True) as connection:

            with closing(connection.cursor()) as cursor:

                stmt_str = f"""
                            select objects.id,  objects.label, group_concat(distinct (temp1.name || ' ('||temp1.part||')' )) as agents_name ,temp1.date, 
                                group_concat(distinct departments.name) as departments_name, group_concat(distinct temp2.name ) as classifiers_name
                        
                                from
                                (select o.id, p.part, a.name, o.date from
                                    objects  o
                                    left outer join productions p on p.obj_id = o.id
                                        left outer join agents a on a.id = p.agt_id        
                                    order by a.name  ) as temp1 
                                    
                                left join objects on objects.id = temp1.id
                                    left join objects_departments on objects_departments.obj_id = objects.id
                                        left join departments on departments.id = objects_departments.dep_id
                                
                                left join 
                                    (select o.id, lower(c.name) as name
                                        from objects o
                                        left outer join objects_classifiers oc on o.id = oc.obj_id
                                        left outer join classifiers c on oc.cls_id = c.id
                                        order by lower(c.name)) as temp2 on temp2.id = objects.id
                            
                            group by objects.id   {temp_filter}"""

                cursor.execute(stmt_str)
                #cursor.execute(stmt_str,  {"st" : filter})# this prepare statement doesn't work #

                row = cursor.fetchone()
                str_list = HEADER
                temp = []
                count = 0

                while row is not None:
                    row = list(row)
                    temp.append(row)
                    count += 1
                    row = cursor.fetchone()
                table = Table(str_list, temp, format_str = FORMAT_FLAG, preformat_sep = FORMAT_SEP)

                print(f"Search produced {count} objects")
                print(table)
    except Exception as ex:
        print(ex, file=stderr)
        sys.exit(1)
