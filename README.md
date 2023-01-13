# sqlite

All the written codes are for the convenience of working with sqlite3 for programmer friends.

Download
--------

You can also install from this repository.

    git clone https://github.com/goldaaa/sqlite.git

Then, install the library with

    python setup.py install


Importing
---------
    from sqlite import Sqlite
    sql = Sqlite(name_file='sqlite')
    sql.table = 'users'

Create
---------
    from datetime import date
    sql.create(
        first_name='test', last_name='out_test',
        birthday=date(2022, 1, 1),
        code_melli=1234567890, student_code=12345,
        courses=['aa', 'bb'],
        grades=[17, 20]
    )

Search
---------
    sql.search(
        columns=['id', 'first_name'], order=['id'],
        # character=True,
        id=(1, 2),  # or id=1
        first_name=('test', 'apptest'),  # or first_name='e'
    )


Delete
---------
    sql.delete(rowid=5)

Update
---------
    sql.update(rowid=5, first_name='test')


Get
---------
    sql.get(
        columns=['id', 'first_name'],
        id=1,
        # first_name='test',
    )

Views
---------
    sql.views(rows=['id', 'first_name', 'last_name'], order=['first_name', 'last_name'])
    sql.views()


If you are interested in financial support, you can send a message through Gmail if you have any questions.

gmail: goldaaa.program@gmail.com

[github sqlite](https://github.com/goldaaa/sqlite)
