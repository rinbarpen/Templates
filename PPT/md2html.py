import os
import sys

if len(sys.argv) < 3:
  print("参数不足")
  print("Usage: $in $out [verbose]")
  exit(1)

md_file = sys.argv[1]
html_file = sys.argv[2]

pandoc_path = "pandoc.exe" # 替换成你的pandoc路径
if len(sys.argv) > 3 and sys.argv[3] == "verbose":
  pandoc_argv_str = "{pandoc_path} {md_file} -o {html_file} -t revealjs -s -V theme=white --slide-level=2".format(pandoc_path=pandoc_path, md_file=md_file, html_file=html_file)
  pandoc_argv = pandoc_argv_str.split()
  os.execvp(pandoc_path, pandoc_argv)
else:
  pandoc_argv_str = "{pandoc_path} {md_file} -o {html_file} -t revealjs -s -V theme=white -V center=false -V controlsTutorial=false -V slideNumber=true --slide-level=2".format(pandoc_path=pandoc_path, md_file=md_file, html_file=html_file)
  pandoc_argv = pandoc_argv_str.split()
  os.execvp(pandoc_path, pandoc_argv)
