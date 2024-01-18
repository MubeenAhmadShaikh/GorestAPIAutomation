
# GorestAPI Automation


The Gorest API Automation project is an api testing framework that ensures the reliability and security of gorest APIs through a range of features. Gorest APIs are freely available APIs with Bearer access token and tons of features. The framework incorporates data-driven testing, positive/negative tests validation, and Pytest parameterizations for efficient test of multiple data. With logging and detailed reporting, it provides insights into test results. The project includes a retry mechanism for handling limited request failures and validates various aspects such as authentication,content-type, response time, pagination parameters, status codes, response structure, and response validation. Custom assertions enhance test coverage, making it a comprehensive framework for thorough API testing.


## Run using Docker Container

- Docker containers makes it easy to run the tests in a specific environment where you do not have to install anything specifically. Just pull the image and run simple command to run the tests.
- Image to use for this project [gorestapi-automation](https://hub.docker.com/r/mubeenahmadshaikh/gorestapi-automation)
- All the instructions are given on docker image overview for running tests in container


## Points to know before running the project locally
- Signup to go rest for the access token https://gorest.co.in/
- store the access token in `conf.ini` file in `token` variable
- Access token is required for POST, PUT, PATCH and DELETE methods.
- Created data with a particular access token will only be available for same user and not to the rest.
- According to gorest we can access the GET request without Bearer token but the data created during tests won't be available to validate, Hence used Bearer token for GET requests also.
- Data will be removed on daily basis.
- Do check the website https://gorest.co.in for more details on `request-rate-limits` `pagination parameters` `status codes` `curl example for REST API`

## Run Locally 
- Clone the Project
```bash
git clone https://github.com/MubeenAhmadShaikh/GorestAPIAutomation.git
```
- Go to the project directory

```bash
cd GorestAPIAutomation
```

- Install dependencies

```bash
pip install -r requirements.txt
```
- Create `conf.ini` file using `conf.ini.templates` file in root directory and edit the `token` variable
```bash
token = your_access_token_here
```
- Navigate to tests directory
```bash
cd tests
```

- Run all the tests

```bash
pytest -s -v
```



## Generating Allure and HTML reports


#### Pytest Html report
Dependensies
`pytest-html`
- Run the tests using following command
```bash
pytest test_filename.py -s -v -m "marker_name" --html=path_to_save_report/report.html
```
Generated Pytest HTML report.
#### Allure interactive report
Dependensies
`allure-pytest` `allure commandline`

- Run the tests using following command
```bash
pytest test_filename.py -s -v -m "marker_name" --alluredir=path_to_directory_for_saving_json_data
```

- Using the JSON data generated for tests generate allure reports with following command
```bash
allure serve path_to_directory_of_json_data
```

- To save the html to system use following command
```bash
allure generate path_to_directory_of_json_data
```
- Video of allure interactive reports

### Details of arguments

| Parameter | Option     | Description                |
| :-------- |:-----------| :------------------------- |
| `pytest` | `required` | Pytest command to run the tests from terminal |
| `test_filename.py` | `optional` | To run the tests from specific file if not provided all the files with 'test_' or '_test' will be considered |
| `-s` | `optional` | for displaying console logs|
| `-v` | `optional` | for displaying additional details |
| `-m "marker_name"` | `optional` | To run the customised markers \| **Accepted values**: [positive, negative]|
| `--html="Path/file_name.html"` | `optional` | To generate the html report at given path  |
| `--alluredir=path_to_directory_for_saving_json_data` | `optional` | To generate the json data files for allure report at given path  |
| `allure serve ` | `required` | To generate the Allure report using json data files at given path  |


## Features

- GET, POST, PUT, PATCH, DELETE APIs Tested 
- API Test Automation
- RESTapis Testing
- Schema Validation
- Response data Validation
- Data driven tests 
- End-to-end tests 
- Positive/negative tests
- Pytest Parameterizations
- Logging 
- Interactive reporting [ HTML Reporting | Allure Reporting ]
- Retry mechanisam for limited requests
- Auth validations using Bearer token
- status code validation
- Searching | Pagination validation
- content-type | environment | response time validations
- Auth token verification
- Response body validation
- Custom assertions


## Developed using

- Python
- Pytest
- Requests library
- Allure reports
- Docker

## 🛠 Skills

`Python` `Pytest` `Allure reports` `Docker` `HTML reports` `Automation Testing` `API Testing`  `RESTapi`