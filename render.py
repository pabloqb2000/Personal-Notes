import os
import json
from os import path
from jinja2 import FileSystemLoader, Environment
from utils import *
from posixpath import join

class Renderer:
    def __init__(self, env, writer, input_dir, output_dir):
        self.env = env
        self.writer = writer
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.config_filename = 'app_data.json'

    def render_dir(self, dir, app_data):
        folder_name = path.basename(dir)
        
        if folder_name in ['static', 'resources']:
            input_dir = join(self.input_dir, dir)
            output_dir = join(self.output_dir, dir)
            self.writer.copy_dir(input_dir, output_dir)
        elif folder_name in ['templates']:
            pass
        else:
            self.render_recursive(dir, app_data)

    def render_file(self, file, app_data):
        file_name = path.basename(file)
        file_name, extension = path.splitext(file_name)
        input_file = join(self.input_dir, file)
        output_file = join(self.output_dir, file)

        if file_name + extension == self.config_filename:
            pass
        elif extension == '.html':            
            template = self.env.get_template(file)
            content = template.render(app_data=app_data)
            self.writer.write_file(output_file, content)
        else:
            self.writer.copy_file(input_file, output_file)

    def render(self):
        self.render_recursive('')

    def render_recursive(self, dir, app_data={}):
        sdir = join(self.input_dir, dir)
        source = os.listdir(sdir)

        if self.config_filename in source:
            with open(join(sdir, self.config_filename), 'rt') as f:
                app_data.update(json.load(f))

        for f in source:
            fdir = join(dir, f)
            f = join(self.input_dir, fdir)
            if path.isdir(f):
                self.render_dir(fdir, app_data)
            else:
                self.render_file(fdir, app_data)


def run():
    input_dir = r'./source'
    output_dir = r'./docs'
    delete_all = True
        
    loader = FileSystemLoader(input_dir)
    env = Environment(loader=loader, autoescape=True)
    # writer = DebugFileWriter()
    writer = FileWriter()
    renderer = Renderer(env, writer, input_dir, output_dir)

    if delete_all:
        writer.delete_dir(output_dir)
    renderer.render()

if __name__ == '__main__':
    run()