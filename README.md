linguist telegram bot
=====================

### Dependencies

#### Python

* Interpreter `python` 2.7+

* Packages

    - `python-telegram-bot` 4.0rc1
    - `psycopg2` 2.6.1

To install all packages at once run

```sh
$ pip install --user -r requirements.txt
```

#### DBMS

* `PostgreSQL` 9.3 (with materialized view support)

To install database schema run

```sh
$ psql -h localhost -d linguist -f schema.sql
```

Unpack `dict_data.sql` if needed

```sh
$ tar -xf dict_data.sql.tar.gz
```

At last create dictionary data and refresh materialized view

```sh
$ psql -h localhost -d linguist -f dict_data.sql
$ psql -h localhost -d linguist -c 'refresh materialized view v_dictionary'
```

### LICENSE

Copyright (c) 2016 Dmitriy Olshevskiy. MIT LICENSE.

See LICENSE for details.
