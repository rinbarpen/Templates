import os
import subprocess
import sys
from argparse import ArgumentParser

python_version = str()
conda_env = str()
# gcc, cuda 映射表
cuda_version_map = {
  "7.5": "10.1",
  "8.1": "10.2",
  "9.3": "11.0",
  "10.2": "11.1",
  "11.2": "11.2"
}

def parse_args():
  global python_version, conda_env
  ArgumentParser.add_argument('-env', '--conda_env', required=True, help="要创建的conda环境")
  ArgumentParser.add_argument('-py', '--python', required=True, default="3.8", help="要安装的python版本")
  ArgumentParser.add_argument('-h', '--help', help="用法提示")
  
  args = ArgumentParser.parse_args()
  
  if args.help:
    ArgumentParser.print_usage()
    return
  
  if args.conda_env:
    conda_env = args.conda_env
  if args.python:
    python_version = args.python

def get_gcc_version():
  """
  @breif: 获取现在系统默认的gcc环境
  """
  try:
    output = subprocess.check_output(["which", "gcc"], universal_newlines=True)
    if output.startswith("/usr/bin/gcc"):
      output = subprocess.check_output(["gcc", "--version"], universal_newlines=True)
      version_line = output.split("\n")[0]
      version = version_line.split()[2]
    else:
      output = subprocess.check_output(["gcc", "--version"], universal_newlines=True)
      version_line = output.split("\n")[-1]
      version = version_line.split()[2]
      
    return version
  except subprocess.CalledProcessError:
    print("错误: 找不到 gcc.")
    print("提示：把 gcc 加入环境变量或下载 gcc.")
    # TODO：
    print("把 gcc 加入环境变量：<doc1>")
    # TODO：
    print("怎么下载 gcc ：")
    sys.exit(1)

def install_conda_environment(env_name, python_version):
  subprocess.run(["conda", "create", "-n", env_name, f"python={python_version}", "-y"], check=True)
  subprocess.run(["conda", "activate", env_name], shell=True)


def install_cuda_and_pytorch(cuda_version):
  subprocess.run(["conda", "install", "-c", "conda-forge", f"cudatoolkit={cuda_version}", "-y"], check=True)
  subprocess.run(["conda", "install", "pytorch", "torchvision", "torchaudio", f"cudatoolkit={cuda_version}", "-c", "pytorch", "-y"], check=True)

def main():
  global python_version, conda_env, cuda_version_map
  
  # 获取本系统 GCC 版本
  gcc_version = get_gcc_version()
  print(f"本系统的 GCC 版本: {gcc_version}")
  if gcc_version == "":
    raise ValueError("GCC 不存在，请安装 GCC 或配置 GCC 环境")

  cuda_version = cuda_version_map[gcc_version]
  print(f"将要下载的 CUDA 版本: {cuda_version}")
  if cuda_version == "":
    raise ValueError(f"未找到指定的 CUDA 版本")

  # 安装 conda 环境
  install_conda_environment(conda_env, python_version)
  install_cuda_and_pytorch(cuda_version)

  print(f"安装完成. 使用 conda activate {conda_env} 激活环境")

if __name__ == "__main__":
  parse_args()
  main()
