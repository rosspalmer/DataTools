import os
import pandas as pd
from sql_tables import hardcoded_tables
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float
from sqlalchemy.sql import select

class sql_manager(object):

    def __init__(self, project):
        self.proj = project
        self.eng = create_engine(engine_string(self.proj.sql_dict))
        self.meta = MetaData()
        self.tables = hardcoded_tables(self.eng, self.meta)

        self.initial_setup()

    def add_new_data(self, mode, df, data_name):

        if mode == 'ext':
            table_name = 'ext_%s' % data_name
        elif mode == 'pred':
            table_name = 'pred_%s' % data_name
        self.tables[table_name] = table_builder(self.meta, df, table_name)

        self.tables[table_name].drop(self.eng, checkfirst=True)
        self.tables[table_name].create(self.eng)

        df['id'] = df.index + 1
        self.insert_data(df, table_name)

    def insert_data(self, df, table_name):

        data_dict = df.to_dict('record')
        insert_statement = self.tables[table_name].insert()

        if self.proj.sql_dict['type'] == 'sqlite':
            insert_statement = insert_statement.prefix_with("OR IGNORE")
        if self.proj.sql_dict['type'] == 'mysql':
            insert_statement = insert_statement.prefix_with("IGNORE")

        conn = self.eng.connect()
        conn.execute(insert_statement, data_dict)
        conn.close()

    def select_data(self, table_name):

        if table_name not in self.tables:
            self.tables[table_name] = \
                Table(table_name, self.meta, auto_load=True, autoload_with=self.eng)

        sel = select([self.tables[table_name]])

        conn = self.eng.connect()
        result = conn.execute(sel)
        headers = result.keys()
        data = result.fetchall()
        if len(data) > 0:
            return pd.DataFrame(data, columns=headers)
        else:
            return pd.DataFrame(columns=headers)

    def initial_setup(self):

        if self.proj.sql_dict['type'] == 'sqlite':
            self.meta.create_all(self.eng)

        if self.proj.sql_dict['type'] == 'mysql':
            self.meta.create_all(self.eng)

def engine_string(sql_dict):

    if sql_dict['type'] == 'sqlite':
        eng_str = 'sqlite:///%s' % sql_dict['location']
    elif sql_dict['type'] == 'mysql':
        eng_str = 'mysql://root:zig2zag@localhost/dtools'

    return eng_str

def table_builder(meta, df, table_name):
    table = Table(table_name, meta,
                Column('id', Integer, primary_key=True))

    for col_name in df:
        dtype = df.dtypes[col_name]
        if dtype == 'int64':
            new_col = Column(col_name, Integer)
        elif dtype == 'float64':
            new_col = Column(col_name, Float)
        elif dtype == 'object':
            size = df[col_name].str.len().max()
            new_col = Column(col_name, String(size))
        table.append_column(new_col)
    return table
