import pandas as pd
import json
import re
import functools
import os.path

#for types:
import _io
#doing it with "overloading" 
#allows function to take
"""
file path
file
str
dict
"""
#args
def unpack_overloader_decorator(func):
    @functools.wraps(func)
    def new(data,*args,**kwargs):
        file=None
        if type(data) is str and os.path.exists(data):#if it is a file path:
            file=open(data,"r")
        if type(data) is _io.TextIOWrapper: #if it is a file        
            file=data
        if file:
            data=file.read()
            file.close()
        if type(data) is str:
            try:
                data=json.loads(data)
            except ValueError:
                raise Exception(f"Invalid json data:\n{data}")
        if type(data) is dict:
            return func(data,*args,**kwargs)
        else: 
            raise Exception("Invalid Argument type")
    return new
@unpack_overloader_decorator     
def unpack_coco(coco_dict:dict)->(dict,dict,dict):
    info=coco_dict["info"]
    categories=coco_dict["categories"]
    annotations_with_img={ annotation["image_id"]:annotation for annotation in coco_dict["annotations"]}
    tempimages={image["id"]:image for image in coco_dict["images"]}
    for id in annotations_with_img:
        annotations_with_img[id].update(tempimages[id])
        annotations_with_img[id].pop("id")
        annotations_with_img[id].pop("image_id")
    return info,categories,annotations_with_img

def mega_entry_to_dict(entry,threshold=0,output=None,coco_df=None):
  i=0
  for detection in entry['detections']:
    if detection['conf']>threshold:
      output[(entry.name,i)]=pd.concat([pd.Series({'conf':detection['conf'],'bbox':detection['bbox'],'mega_category':detection["category"]}),coco_df.loc[entry.name]])
      i+=1      
@unpack_overloader_decorator
def unpack_mega(data,df_imgs=None,WIDTH=None,HEIGHT=None):
    annotations_with_img={ annotation["file"]:annotation for annotation in data["images"]}
    raw_df_mega=pd.DataFrame.from_dict(annotations_with_img,orient="index")
    raw_df_mega['file_name']=raw_df_mega['file'].apply(lambda s:"/".join(s.split('/')[1:]))
    raw_df_mega.drop('file',axis=1,inplace=True)
    raw_df_mega.index=raw_df_mega.index.map(lambda s:"/".join(s.split('/')[1:]).split('.')[0])
    tdict={}
    raw_df_mega.apply(mega_entry_to_dict,threshold=0,output=tdict,coco_df=df_imgs,axis=1)
    raw_df_mega_expanded=pd.DataFrame.from_dict(tdict).T
    raw_df_mega_expanded['converted_box']=raw_df_mega_expanded['bbox'].apply(lambda box:[box[0],box[1],box[0]+box[2],box[1]+box[3]])
    if WIDTH and HEIGHT:#all images same size
      raw_df_mega_expanded['converted_box']=raw_df_mega_expanded['converted_box'].apply(lambda box:[box[0]*WIDTH,box[1]*HEIGHT,box[2]*WIDTH,box[3]*HEIGHT])
      df=raw_df_mega_expanded.drop('bbox',axis=1)
    else:
      df=raw_df_mega_expanded
    return df
formats={"coco":unpack_coco,"mega":unpack_mega}
def test():
    return formats
def snapshot_safari_paths_from_name(name,name_abbrev):#for working with kaggle
    datapath=f'../input/snapshot-{name}/'
    cameras=f'{name_abbrev}_S1.lila/{name_abbrev}_S1'
    #(2*path)[:-1] b/c unzipping results in the file being placed under a folder of its name
    metadata=(2*f'Snapshot{name[0].upper()+name[1:]}_S1_v1.0.json/')[:-1]
    mega_A=(2*f'snapshot-safari_{name_abbrev}_mdv5a.0.0_results.json/')[:-1]
    mega_B=(2*f'snapshot-safari_{name_abbrev}_mdv5b.0.0_results.json/')[:-1]
    return datapath,cameras,metadata,mega_A,mega_B

if __name__ == "__main__":
    #expecting inputs as format value
    import sys
    print(formats[str(sys.argv[1])](sys.argv[2]))
