from shutil import copyfile, copytree, rmtree
import os

class FileWriter:
    def copy_file(self, input_file, output_file):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        copyfile(input_file, output_file)
    
    def copy_dir(self, input_dir, output_dir):
        copytree(input_dir, output_dir)

    def write_file(self, output_file, content):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, '+wt') as f:
            f.write(content)
    
    def delete_dir(self, dir):
        if os.path.exists(dir):
            rmtree(dir)

class DebugFileWriter:
    def copy_file(self, input_file, output_file):
        print(output_file, '(copy)')
    
    def copy_dir(self, input_dir, output_dir):
        print(output_dir, '(copy)')

    def write_file(self, output_file, content):
        print(output_file, '(rendered)')
    
    def delete_dir(self, dir):
        print(dir, '(delete)')