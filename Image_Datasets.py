import torch
import torchvision
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
from PIL import Image
from os import remove
import pandas as pd
def general_transform_factory(pretensor_transforms_all,posttensor_transforms_all):
  def general_transform(pretensor_transforms,posttensor_transforms):
    return torchvision.transforms.Compose([*pretensor_transforms_all,*pretensor_transforms,ToTensor(),*posttensor_transforms_all,*posttensor_transforms])
  return general_transform
class Images_Dataset(Dataset):
  """
  Takes a pandas dataframe that has filenames for images and labels
   an image transformation function to be applied when getting a value
   access at file_path/file_name
  """
  def __init__(self, df,file_path="",class_name="category_id",pretensor_transforms_all=lambda x:x,posttensor_transforms_all=lambda x:x):
      self._validate(df,class_name)
      self.df = df
      self.transformation_function = general_transform_factory(pretensor_transforms_all,posttensor_transforms_all)
      self.transformation_function_default = self.transformation_function([],[])
      self.file_path=file_path
      self.class_name=class_name
  @staticmethod
  def _validate(obj,class_name):
      # verify file name and class name are present in df
      if "file_name" not in obj.columns:
          raise AttributeError("missing file_name")
      if class_name not in obj.columns:
          raise AttributeError(f"missing class label - {class_name}")
  def __getitem__(self,index):
      #return transformed image,label
      _=df.iloc[index]["transforms"]
      img=Image.open(f"{self.file_path}/{self.df.iloc[index]['file_name']}")
      if _==None:
        return self.transformation_function_default(img),self.df.iloc[index][self.class_name]
      pre,post=_
      return self.transformation_function(pre,post)(img),self.df.iloc[index][self.class_name]

  def __len__(self):
      return len(self.df.index)#rowcount
class Images_Dataset_SAVE(Images_Dataset):
    def __init__(self, df,file_path="",class_name="category_id",file_extension="",save_to=None,use_file_path_in_save_to=False,del_orig_after_saved=False,pretensor_transforms_all=lambda x:x,posttensor_transforms_all=lambda x:x):
      """

      access at file_path/file_name
      save at save_to/file_name
      load at save_to/file_name
                               remove file extension if file_extension is not None
                               if so replace with .file_extension
      if use_file_path_in_save_to
      then save at save_to/file_path/file_name

      Uses torch.save and torch.load
      if saved as a pytorch tensor extension should be pt
      """
      df['processed']=False
      super().__init__(df,file_path=file_path,class_name=class_name,pretensor_transforms_all=pretensor_transforms_all,posttensor_transforms_all=posttensor_transforms_all)
      if save_to is None:
        self.save_to = file_path
      else:
        self.save_to=save_to
      if use_file_path_in_save_to:
         self.save_to += file_path
      self.del_orig_after_saved=del_orig_after_saved
      self.file_extension=file_extension
      if 'processed' not in df.columns:
        df['processed']=False
    def load(self,file_name):
      return torch.load(f"{self.save_to}/{file_name}.{self.file_extension}")  
    def save(self,obj,file_name):
      return torch.save(obj,f"{self.save_to}/{file_name}.{self.file_extension}")
    def __getitem__(self,index):    
      i=self.df.iloc[index]["file_name"]
    #fix later
      #if not self.df.iloc[index]['processed']:
      #  df.iloc[index, df.columns.get_loc('processed')] = True #avoid chained indexing
      #  self.save(super().__getitem__(index)[0],i)
      #  if self.del_orig_after_saved:
      #     os.remove(f"{self.file_path}/{i}")
      return self.load(i),self.df.iloc[index][self.class_name]
    def loopall(self):#process all images
        for i in range(len(self)):
            self[i]


