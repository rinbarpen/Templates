import os
import subprocess
import sys
from argparse import ArgumentParser
import logging
import json

repo_mapper = {}
req_repos = []
repo_file = "scripts/repo_infos.json"

def parse_args():
  global repo_file
  """
      | --update  update local repos info
      | --export {<source_dir='.'> <output_filename='repo_infos.json'>} export {source_dir}'s repos info to {output_filename}
      | -h|--help get the help information
      | -l|--load <repo_name>{:<version>} ...
      | -a|--add <repo_name> <url> <version1> <version2> ...
      | -r|--remove {<repo_name>|<url>} [<version1> <version2> ...]
  """
  parser = ArgumentParser(description="Manage local git repositories.")
  parser.add_argument('--update', action='store_true', help="Update local repos info")
  parser.add_argument('--export', nargs='*', default=None, help="Export repos info from the source directory to the configuration file")
  parser.add_argument('-l', '--load', type=str, nargs='+', help="Load repository by name")
  parser.add_argument('-a', '--add', nargs='+', help="Add a repository: <repo_name> <url> <version1> <version2> ...")
  parser.add_argument('-r', '--remove', nargs='+', help="Remove a repository or specific versions")
  parser.add_argument('-c', '--config', type=str, default=repo_file, help="Set the configuration file")
  args = parser.parse_args()
  return args

def clone_repo(repo_name: str, version: str = None):
  """
  Clone a repo with version from network
  Args:
      repo_name: the name of the repo to clone
      version: the version of the repo to clone
  """
  if version is None:
    version = repo_mapper[repo_name]["versions"][0]

  try:
    print(f'Cloning repository {repo_name} with version {version}')
    os.system(f'git clone --depth 1 {repo_mapper[repo_name]["url"]} -b {version} 3rdparty/{repo_name}')
  except OSError:
    logging.warning(f'Couldn\'t clone repository {repo_name} with version {version}')

def load_repos():
  """
  Load repos' info
  """
  global repo_mapper, repo_file
  with open(repo_file, 'r') as f:
    repo_mapper = json.load(f)

def save_repos():
  """
  Save repos' info to local file
  """
  global repo_mapper, repo_file
  with open(repo_file, 'w') as f:
    json.dump(repo_mapper, f, indent=2)

def add_repo(repo_name, url, versions):
  """
  Add repo into the list of repos
  Args:
      repo_name: repo name
      url: remote url
      versions: the list of versions
  """
  repo_mapper[repo_name] = {
    "url": url,
    "versions": versions
  }

def remove_repo(repo_name_or_url, versions=None):
  """
  Remove a repo from the list of repos
  Args:
      repo_name_or_url: The name of the repo or the url to remove 
      versions: removed versions
  """
  if versions:
    for repo_name, repo_info in list(repo_mapper.items()):
      if repo_name == repo_name_or_url or repo_info["url"] == repo_name_or_url:
        repo_mapper[repo_name]["versions"] = [v for v in repo_info["versions"] if v not in versions]
        if not repo_mapper[repo_name]["versions"]:
          del repo_mapper[repo_name]
  else:
    repo_mapper.pop(repo_name_or_url, None)
    repo_mapper = {k: v for k, v in repo_mapper.items() if v["url"] != repo_name_or_url}

def read_dir(source_dir):
  """
  Get repos' info from the given source directory
  Args:
      source_dir: path to the directory containing the repos
  """
  global repo_mapper
  for root, dirs, files in os.walk(source_dir):
    for dir in dirs:
      repo_path = os.path.join(root, dir)
      if os.path.isdir(os.path.join(repo_path, '.git')):
        try:
          url = subprocess.check_output(['git', '-C', repo_path, 'config', '--get', 'remote.origin.url']).strip().decode()
          # version = subprocess.check_output(['git', '-C', repo_path, 'config', '--get', 'fetch']).strip().decode()
          try:
            version = subprocess.check_output(['git', '-C', repo_path, 'describe', '--tags', '--abbrev=0']).strip().decode()
          except subprocess.CalledProcessError:
            version = None
          repo_mapper[dir] = {"url": url, "versions": [version]}
        except subprocess.CalledProcessError as e:
          logging.warning(f'Could not retrieve info for repo at {repo_path}: {e}')


def main():
  args = parse_args()
  
  if args.export is not None:
    print('export')
    if len(args.export) == 2:
      source_dir = args.export[0]
      output_filename = args.export[1]
    elif len(args.export) == 1:
      source_dir = args.export[0]
      output_filename = 'repo_infos.json'
    else:
      source_dir = '.'
      output_filename = 'repo_infos.json'
    
    read_dir(source_dir)
    
    print(f'export to {output_filename}')
    with open(output_filename, 'w') as f:
      json.dump(repo_mapper, f, indent=2)
    
    return
  
  if args.config:
    global repo_file
    repo_file = args.config
  
  if args.update:
    load_repos()

  if args.load:
    load_repos()
    for i in range(0, len(args.load)):
      repo_name = args.load[i].split(':')[0]
      version = args.load[i].split(':')[1] if len(args.load[i].split(':')) > 1 else None
      req_repos.append((repo_name, version))

  if args.add:
    load_repos()
    repo_name, url, *versions = args.add
    add_repo(repo_name, url, versions)

  if args.remove:
    load_repos()
    repo_name_or_url, *versions = args.remove
    remove_repo(repo_name_or_url, versions)

  for repo in req_repos:
    clone_repo(repo[0], repo[1])    

  if args.add or args.remove:
    save_repos()
  
  if args.load:
    # extract required
    with open('requirements.txt', 'w+') as f:
      for i in range(0, len(args.load)):
        repo_name = args.load[i].split(':')[0]
        version = args.load[i].split(':')[1] if len(args.load[i].split(':')) > 1 else repo_mapper[repo_name]["versions"][0]
        f.write('{}={}\n'.format(repo_name, '*.*' if version is None else version))

if __name__ == "__main__":
  main()
