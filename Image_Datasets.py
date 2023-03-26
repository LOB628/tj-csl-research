import torch
from torch.utils.data import Dataset
from torchvision import datasets
from PIL import Image
from os import remove
import pandas as pd



def general_transform_factory(pretensor_transforms_all,posttensor_transforms_all):
  def general_transform(pretensor_transforms,posttensor_transforms):
    return torchvision.transforms.Compose([*pretensor_transforms_all,*pretensor_transforms,ToTensor(),posttensor_transforms_all,*posttensor_transforms])

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
      img=Image.open(f"{self.file_path}/{self.df.iloc[index]['file_name']}"),self.df.iloc[index][self.class_name]
      if _==None:
        return self.transformation_function_default(img)
      pre,post=_
      return self.transformation_function(pre,post)(img)

  def __len__(self):
      return len(self.df.index)#rowcount
class Images_Dataset_SAVE(Images_Dataset):
    def __init__(self, df,transformation_function,file_path="",class_name="category_id",file_extension="",save_to=None,use_file_path_in_save_to=False,del_orig_after_saved=False):
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
      super().__init__(df,transformation_function,file_path=file_path,class_name=class_name)
      if save_to is None:
        self.save_to = file_path
      else:
        self.save_to=save_to
      if use_file_path_in_save_to:
         self.save_to += file_path
      self.saved=dict()
      self.del_orig_after_saved=del_orig_after_saved
      self.file_extension=file_extension
    def load(self,file_name):
      return torch.load(f"{self.save_to}/{file_name}.{self.file_extension}")  
    def save(self,obj,file_name):
      return torch.save(obj,f"{self.save_to}/{file_name}.{self.file_extension}")
    def __getitem__(self,index):    
      if index not in self.saved:
        i=self.df.iloc[index]["file_name"]
        self.saved[index]=i
        self.save(super().__getitem__(index)[0],i)
        if self.del_orig_after_saved:
          remove(f"{self.file_path}/{i}")
      else:
        i=self.saved[index]
      return self.load(i),self.df.iloc[index][self.class_name]

