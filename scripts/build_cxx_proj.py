import os
import subprocess
import sys
from argparse import ArgumentParser
import shutil

proj_name = ''
root_dir = '.'
template_dir = '~/Template'
use_qt = False
use_lib = False

def parse_args():
  """
  
  """
  global root_dir, template_dir
  
  parser = ArgumentParser(description = 'Build a cxx project')
  parser.add_argument('-r', '--root', type=str, default=root_dir, help='Root directory of the project')
  parser.add_argument('-n', '--name', type=str, required=True, help='The project name')
  parser.add_argument('-t', '--template', type=str, default=template_dir, help='Template files live')
  parser.add_argument('--qt', help='Use qt CMakeLists instead of original one')
  parser.add_argument('--lib', help='Use lib CMakeLists instead of original one')

  args = parser.parse_args()
  return args

def set_args():
  global root_dir, proj_name, template_dir, use_qt
  args = parse_args()
  if args.root == '':
    raise ValueError('The project root must be specified')
  else:
    root_dir = os.path.dirname(args.root)
  
  if args.name:
    proj_name = args.name
    if proj_name == '' or proj_name.find('/') != -1 or proj_name.find('\\') != -1:
      raise ValueError('Error format project name: %s' % proj_name)
  
  if args.template:
    template_dir = os.path.expanduser(args.template)
  else:
    raise ValueError('The template directory must be specified')
  if args.qt:
    use_qt = True
  if args.lib:
    use_lib = True
  

def create_dir_if_not_exists(path):
  if not os.path.exists(path):
    os.makedirs(path)

def copy_file_if_not_exists(src, dst):
  if not os.path.exists(dst):
    shutil.copy(src, dst)

def build():
  global root_dir, proj_name, template_dir, use_qt, use_lib
  set_args()
  
  project_path = os.path.join(root_dir, proj_name)
  create_dir_if_not_exists(project_path)
  
  src_path = os.path.join(project_path, 'src', proj_name)
  include_path = os.path.join(project_path, 'src', 'include', proj_name)
  third_party_path = os.path.join(project_path, '3rdparty')
  tests_path = os.path.join(project_path, 'tests')
  
  create_dir_if_not_exists(src_path)
  create_dir_if_not_exists(include_path)
  create_dir_if_not_exists(third_party_path)
  
  copy_file_if_not_exists(os.path.join(template_dir, '.clang-format'), os.path.join(project_path, '.clang-format'))
  if use_qt:
    copy_file_if_not_exists(os.path.join(template_dir, 'qt', 'CMakeLists.txt'), os.path.join(project_path, 'CMakeLists.txt'))
  elif use_lib:
    copy_file_if_not_exists(os.path.join(template_dir, 'CMakeLists-Lib.txt'), os.path.join(project_path, 'CMakeLists.txt'))
  else:
    copy_file_if_not_exists(os.path.join(template_dir, 'CMakeLists.txt'), os.path.join(project_path, 'CMakeLists.txt'))

  scripts_src = os.path.join(template_dir, 'scripts')
  scripts_dst = os.path.join(project_path, 'scripts')
  if not os.path.exists(scripts_dst):
    shutil.copytree(scripts_src, scripts_dst)

  tests_src = os.path.join(template_dir, 'tests')
  tests_dst = os.path.join(project_path, 'tests')
  if not os.path.exists(tests_dst):
    shutil.copytree(tests_src, tests_dst)
  
  ex_src = os.path.join(template_dir, 'examples')
  ex_dst = os.path.join(project_path, 'examples')
  if not os.path.exists(ex_dst):
    shutil.copytree(ex_src, ex_dst)
    
  copy_file_if_not_exists(os.path.join(template_dir, 'requirements.txt'), os.path.join(project_path, 'requirements.txt'))
  

if '__main__' == __name__:
  build()
