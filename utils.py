import os,shutil
def ignore_files(dirname,lsdir):
  return [f for f in lsdir if os.path.isfile(f) or f.startswith(".")]
def copy_folder_structure(name):
  """util for copying folder structure without files
     takes a name  and copies from name-images to name-processed
  """
  shutil.copytree(f"{name}-images",f"{name}-images-processed",ignore=ignore_files)
