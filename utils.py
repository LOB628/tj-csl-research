import os,shutil,torch
def ignore_files(dirname,lsdir):
  return [f for f in lsdir if os.path.isfile(f) or f.startswith(".")]
def copy_folder_structure(name):
  """util for copying folder structure without files
     takes a name  and copies from name-images to name-processed
  """
  shutil.copytree(f"{name}-images",f"{name}-images-processed",ignore=ignore_files)

class getitem_identity:
    def __init__(self):
        pass
    def __getitem__(self,key):
        return key
def toLabel(element,length=1,convert_category_id=getitem_identity):
  ret=torch.zeros(length)
  ret[convert_category_id[element]]=1
  return ret  
