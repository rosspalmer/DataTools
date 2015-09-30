from sqlalchemy import Table, Column, Integer, String, Float

def hardcoded_tables(eng, meta):

    table_dict = {}

    table_dict['linear_summary'] = \
        Table('linear_summary', meta,
              Column('model_id', Integer, primary_key=True, autoincrement=False),
              Column('n_var', Integer), Column('n_obs', Integer),
              Column('r_squared', Float), Column('adj_r_squared', Float),
              Column('f_stat', Float), Column('prob_f_stat', Float))

    table_dict['linear_coeff'] = \
        Table('linear_coeff', meta,
              Column('model_id', Integer, primary_key=True, autoincrement=False),
              Column('name', String(50), primary_key=True, autoincrement=False),
              Column('coeff', Float), Column('std_err', Float),
              Column('t', Float), Column('p', Float),
              Column('alpha', Float), Column('conf_l', Float),
              Column('conf_h', Float))

    table_dict['models'] = \
        Table('models', meta,
              Column('type', String(20), primary_key=True, autoincrement=False),
              Column('model_id', Integer, primary_key=True, autoincrement=False),
              Column('x_col', String(50)), Column('y_col', String(50)))

    return table_dict