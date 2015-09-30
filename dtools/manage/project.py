import os
from simplecrypt import encrypt, decrypt

class project(object):

    def __init__(self, project_dir):
        self.abs_path = ''
        self.sql_dict = {}
        self.load_project(project_dir)

    def load_project(self, project_dir, encrypt_pass='None'):

        try:
            os.stat(project_dir)
        except OSError:
            create_project(project_dir, encrypt_pass)

        if os.path.isabs(project_dir):
            self.abs_path = project_dir
        else:
            self.abs_path = os.path.abspath(project_dir)

        if self.abs_path.endswith('/'):
            self.abs_path = self.abs_path[:-1]
            
        self.sql_dict = read_config(project_dir, encrypt_pass)
        if self.sql_dict['flavor'] == 'sqlite':
            self.sql_dict['path'] = self.abs_path

def create_project(project_dir, encrypt_pass):

    os.mkdir(project_dir)
    create_config(project_dir, encrypt_pass)

def create_config(project_dir, encrypt_pass='None'):

    config_dir = '%s/.config' % project_dir
    f = open(config_dir, 'w')

    print
    print '------Welcome to DataTools Configuration---------'
    print
    print 'Select SQL Flavor'
    print '[1] - SQLite'
    print '[2] - MySQL'
    flavor = int(raw_input('Input Number: '))
    print

    if flavor == 1:

        info = 'sqlite'
        info += ':%s.db' % raw_input('Database Name: ')

    elif flavor == 2:

        info = 'mysql'
        info += ':%s' % raw_input('Host: ')
        info += ':%s' % raw_input('Username: ')
        info += ':%s' % raw_input('Password: ')
        info += ':%s' % raw_input('Database Name: ')

    print
    print 'Encrypting Config File'
    f.write(encrypt(encrypt_pass, info))
    print 'Config File Complete'

def read_config(project_dir, encrypt_pass='None'):

    config_dir = '%s/.config' % project_dir
    f = open(config_dir, 'r').read()
    info = decrypt(encrypt_pass, f)

    sql_dic = {}
    info = info.split(":")
    if info[0] == 'sqlite':
        sql_dic['flavor'] = 'sqlite'
        sql_dic['db_name'] = info[1]
    elif info[0] == 'mysql':
        sql_dic['flavor'] = 'mysql'
        sql_dic['host'] = info[1]
        sql_dic['username'] = info[2]
        sql_dic['password'] = info[3]
        sql_dic['db_name'] = info[4]

    return sql_dic
