# Command-Line-Program-for-Art-Gallery-Search
### Descriptions of all documents and requirements

'lux.py' and 'luxdetails.py' composed two programs required for submission. The parameters required for these two command-line programs follows the input specification requirements. Inside the file, we have included Error Handling that would capture the errors in command line. We also submitted two modules that will help execute these two programs: 'filters_obj.py' and 'filters_detail.py'.

'test_lux.py' is a automated testing file which includes a list of command line/test cases we would like to run. To run this file, type 'python test_lux.py' in terminal and it will run automatically. The command lines executed upon call contains all the test cases we wanted to test. The output will be a coverage. file and htmlcov folder from coverage package. The test cases we put inside the test file included: objects that have no references, lots of references, agents with several nationalities, which also fits into purpose of boundary testing. Following these command line, we generated a test coverage report, which is named: 'coverage_index.html'. We consider these two files a combination of boundary tests and test automation. 

'out1' contains all the output we have generated from test_lux.py. To check if this matches the record from sql, we manually searched all of the test cases using sqlite studio, and have found out1 to be matching the sql queries output.

'unit_test_lux.py' and 'unit_test_luxdetails.py' contains unit testing for 'lux.py' and 'luxdetails.py' separately. We have included tests of modulized functions imported in the unit tests. We consider these two files a submission of unit testing requirement for this test. 
