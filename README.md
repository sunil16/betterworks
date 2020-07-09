BetterWorks Falcon REST API with PostgreSQL
===============================

Simple REST API using Falcon web framework.

Falcon is a high-performance Python framework for building cloud APIs, smart proxies, and app backends. More information can be found [here](https://github.com/falconry/falcon/).

Requirements
============
This project uses [virtualenv](https://virtualenv.pypa.io/en/stable/) as isolated Python environment for installation and running. Therefore, [virtualenv](https://virtualenv.pypa.io/en/stable/) must be installed. And you may need a related dependency library for a PostgreSQL database. See [install.sh](https://github.com/) for details.


Installation
============

Install all the python module dependencies in requirements.txt

```
  ./install.sh
```

Start server

```
  ./bin/run.sh start
```

Deploy
=====
You need to set `APP_ENV` environment variables before deployment. You can set LIVE mode in Linux as follows.

Linux
------
In Linux, just set `APP_ENV` to run in live mode.
```shell
export APP_ENV=live
./bin/run.sh start
```

Usage
=====

Get a collection of 5 days analysed result data (total Objective and total completed Objectives )
- Request
```shell
curl -XGET http://localhost:5000/v1/dashboard/objectives
```

- Response
```json
{
    "meta": {
        "code": 200,
        "message": "OK"
    },
    "data": {
        "total_objectives": 3,
        "complete_objectives": 1,
        "day_name": "Saturday"
    }
}
```

Get a collection of Departments and Employees and there Objectives

- Request
```shell
curl -XGET http://localhost:5000/v1/dashboard/departments
```

- Response
```json
{
    "meta": {
        "code": 200,
        "message": "OK"
    },
    "data": {
        "1": {
            "department_id": 1,
            "department_name": "Product",
            "pending_objectives": 1,
            "complete_objectives": 0,
            "employees": {
                "1": {
                    "id": 1,
                    "emp_name": "Navneet"
                }
            },
            "objectives": {
                "1": {
                    "id": 1,
                    "objective_text": "Improve HR Processes"
                }
            }
        },
        "2": {
            "department_id": 2,
            "department_name": "Engineering",
            "pending_objectives": 1,
            "complete_objectives": 1,
            "employees": {
                "2": {
                    "id": 2,
                    "emp_name": "Kailash"
                }
            },
            "objectives": {
                "2": {
                    "id": 2,
                    "objective_text": "Raise participation in Surveys"
                },
                "3": {
                    "id": 3,
                    "objective_text": "Improve Engineering Processes"
                }
            }
        }
    }
}
```
