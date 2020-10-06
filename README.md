# Get views from MSSQL database

This is a python module to get the view of the last data from DSTI's student survey

## Installation

Structure of the module:

```bash
.
├── __init__.py
├── lib
│   ├── connection.py
│   ├── encryption.py
│   ├── get_all_data.py
│   ├── __init__.py
│   ├── missing_pkg.py
│   ├── query_template.py
│   ├── README.md
│   └── refresh_view.py
├── mssql_view.py
├── setup.py
└── Views
```
Go inside the `MSSQL_view` folder and run `python mssql_view.py`. If missing dependencies are found they should be installed

## Usage

Once program is run. It will generate a `SQL` query to get the latest data under the form a view. The view will be saved as a `csv` file under the `Views` folder. If data have been updated in the database the user should run this script again to get the latest data.
