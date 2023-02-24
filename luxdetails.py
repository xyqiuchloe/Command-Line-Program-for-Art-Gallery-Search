"""
This module provides a command-line interface for displaying details of an object 
in a database. The module requires the argparse function, sqlite database, and 
filters_detail.py to function properly.

Usage:
    python luxdetails.py <object_id>

Positional arguments:
    id(int)   The ID of the art piece to display details for.

The module uses the argparse module to parse command-line arguments. If an 
invalid argument is passed, an error message is printed to the console. 
If the ID passed is not valid, the filters_detail.object_details function will raise a ValueError.

Example usage:
    python my_module.py 52916
"""
import argparse
import sys
import filters_detail

def main():
    """Parse command line arguments and display details of the object with the specified ID.

    Usage:
       luxdetails.py <id>

    Arguments:
        id(int)  The ID of the art piece to display details for.

    """
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("integer",metavar = "id",
    help = "the id of the object whose details should be shown") #metavar
    try:
        args = parser.parse_args()
    except SystemExit:
        print("Please enter a valid command")
        sys.exit(1)
    try:
        filters_detail.object_details(int(args.integer))
    except ValueError:
        print("Please enter a valid id number")

# -------------------------------------------
if __name__ == '__main__':
    main()
