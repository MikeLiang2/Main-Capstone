All case tested in the three files below:

All_API_TESTED_WITH_EXPECTED.pdf

API_TEST_FOR_Unauthorized.pdf

API_TEST_FOR_FAILED.pdf



All_API_TESTED_WITH_EXPECTED:
Includes all API's success case, after account verified, login
Includes all API's expected input and output format, headers, in json format.

API_TEST_FOR_Unauthorized.
Includes all API's 401 case when account not verified, without login

API_TEST_FOR_FAILED
Includes all API's Bad Request:
example:
	entering weird data format
	missing required column
	other failure from the database:
		such as user, data not found
		failed to make changes
		constraint related error

For all three files, non used API such as get/users/{id} are not tested
Those are pre-defined API by FastAPI-user library
Some methods are redefined.

The database shows in content.pdd

git_repo:
https://github.com/MikeLiang2/Main-Capstone.git
