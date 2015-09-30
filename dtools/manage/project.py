import os

class project(object):

    def __init__(self, project_dir):
        self.abs_path = ''
        self.sql_dict = {}
        self.read_config(project_dir)

    def read_config(self, project_dir):

        try:
            os.stat(project_dir)
        except OSError:
            create_project(project_dir)

        config_dir = '%s/.config' % project_dir
        f = open(config_dir,'r')

        if os.path.isabs(project_dir):
            self.abs_path = project_dir
        else:
            self.abs_path = os.path.abspath(project_dir)

        if self.abs_path.endswith('/'):
            self.abs_path = self.abs_path[:-1]
            
        self.sql_dict['type'] = 'sqlite'
        self.sql_dict['location'] = '%s/dtools.db' % (self.abs_path)

def create_project(project_dir):

    os.mkdir(project_dir)
    config_dir = '%s/.config' % project_dir
    f = open(config_dir, 'w')
    f.write('dtools\n')