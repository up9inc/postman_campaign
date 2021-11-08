# UP9 Tests

This directory contains generated tests for your services, created by [UP9](https://up9.com).

**Note:** The generated assertions have been commented out.

### File structure
- [tests.py](/tests.py) - main file with test cases inside, grouped into classes by service.
- [authentication.py](/authentication.py) - a file to inject authentication into tests, more information inside the file.
- [up9lib.py](/up9lib.py) - UP9 helper library with functions and classes.
- [data](/data) - a directory that contains datasets, body payloads and [service mapping file](#connecting-to-your-services).

### Connecting to your services
In order to know where to run the tests, we provide a mapping file for all services.
The file is located in `data/target_services.json`.
Additionally, you can set the address via environment variables (e.g. `TARGET_<SERVICE_NAME>`), it will have precedence over file.

## Running tests
`tests.py` contains ready to run test code, that can be run ad-hoc, or integrated into CI pipeline.
See [results](#junit-results) for more information about analyzing test results.

### Using Docker
Build docker:
`docker build -t up9-ayslan_10_hotmail_com .`

Run tests:
`docker run -it up9-ayslan_10_hotmail_com:latest`

Run tests with service override:
`docker run -it -e TARGET_CARTS=localhost:55000 up9-ayslan_10_hotmail_com:latest`

### Running locally
Just install several dependencies from PyPi:
1. `pip3 install apiritif jsonpath_ng lxml pytest ddt`
2. `pytest tests.py`

### Running a single test

Locate the test you want to run, then specify its class name and test case name for Pytest:
  `pytest -v tests.py::Tests_api_mysvc_io::test_01_post_api_v1_order__8`

## Sample
```
>> docker run -it up9-ayslan_10_hotmail_com:latest
============================= test session starts ==============================
platform linux -- Python 3.8.7, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: /up9
plugins: apiritif-0.9.6
collecting ... collected 43 items

tests.py .F.............FFFFFFFFFFFFFFF...FFFFFFFFFF                     [100%]
```

## JUnit Results
While pytest results are great, it also offers a way to generate JUnit.xml files, especially valuable for CI pipelines such as Jenkins.
Add `--junitxml=<path>` to the pytest command to generate them.

## Contact
Email us at info@up9.com
