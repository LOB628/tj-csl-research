import pandas
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

formats={"coco":unpack_coco}
def test():
    return formats
if __name__ == "__main__":
    #expecting inputs as format value
    import sys
    print(formats[str(sys.argv[1])](sys.argv[2]))
