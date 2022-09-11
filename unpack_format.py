import pandas
import json
import re
import functools
import os.path
"""
file path
file
str
dict
"""

#doing it with "overloading"
def unpack_overloader_decorator(func):
    @functools.wraps(func)
    def new(data,*args,**kwargs):
        #match(type(data)) pytorch stable does not support 3.10
        t=type(data)
        file_opened=False
        if t is str and os.path.exists(t):#if it is a file path:
            file=open(t,"r")
            file_opened=True
        if t is _io.TextIOWrapper:#if it is a file
            if file_opened:
                t=file.read()
                file.close()
            else:
                origin=file.tell()
                t=file.read()
                file.seek(origin)
        if t is str:
            try:
                t=json.loads(t)
            except ValueError:
                raise Exception(f"Invalid json data:\n{t}")
        if t is dict:
            return func(data,*args,**kwargs)
        else: 
            raise Exception("Invalid Argument type")
    return new
@unpack_overloader_decorator     
def unpack_coco(coco_dict:dict)->pandas.DataFrame:
    info=coco_dict["info"]
    categories=coco_dict["categories"]
    annotations_with_img={ annotation["image_id"]:annotation for annotation in coco_dict["annotations"]}
    tempimages={image["id"]:image for image in coco_dict["images"]}
    for id in annotations_with_img:
        annotations_with_img[id].update(tempimages[id])
    return info,categories,annotations_with_img

formats={"coco":unpack_coco}
def test():
    return formats
if __name__ == "__main__":
    #expecting inputs as format value
    import sys
    print(formats[str(sys.argv[1])](sys.argv[2]))
