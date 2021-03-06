import pickle
import pandas as pd
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", help="", type=str)

args = parser.parse_args()
data_path = args.data_path

train_df = pd.read_pickle('./fsod_train_df.pkl')
train_dict = train_df.to_dict('index')
print(len(train_dict))

images_ls = []
images_name_ls = []
annotations_ls = []
categories_raw_ls = []
for key, value in train_dict.items():
    categories_raw_ls.append(value['category_name'])
categories_raw_ls = list(set(categories_raw_ls))

categories_ls = []
for cnt, item in enumerate(categories_raw_ls):
    categories_dict = {}
    categories_dict['supercategory'] = 'none'
    categories_dict['id'] = cnt + 1
    categories_dict['name'] = item
    categories_ls.append(categories_dict)

images_name_dict = {}
for key, value in train_dict.items():
    img_path = value['image_path']
    assert os.path.exists(img_path)
    # images
    if value['image_name'] in images_name_ls:
        continue
    images_name_ls.append(value['image_name'])
    images_dict = {}
    images_dict['id'] = int('2019' + '%09d' % (key))
    images_dict['file_name'] = value['image_path'].replace('./all_images', os.path.join(data_path, 'fsod/all_images'))
    
    images_dict['width'] = int(value['width'])
    images_dict['height'] = int(value['height'])
    images_ls.append(images_dict)
    images_name_dict[value['image_name']] = int('2019' + '%09d' % (key))

new_image_ls = []
for key, value in train_dict.items():
    img_path = value['image_path']
    assert os.path.exists(img_path)
    annotations_dict = {}
    annotations_dict['ignore'] = 0
    new_image_ls.append(value['image_name'])
    annotations_dict['image_id'] = images_name_dict[value['image_name']]


    annotations_dict['segmentation'] = 0
    annotations_dict['bbox'] = value['bbox'] 
    annotations_dict['area'] = 99999
    annotations_dict['category_id'] = categories_raw_ls.index(value['category_name']) + 1
    annotations_dict['iscrowd'] = 0
    annotations_dict['id'] = str(key)
    annotations_ls.append(annotations_dict)

print('category number: ', len(categories_ls))
print('image number: ', len(images_ls))
print('annotation number: ', len(annotations_ls))
final_dict = {}
final_dict['images'] = images_ls
final_dict['type'] = 'instances'
final_dict['annotations'] = annotations_ls
final_dict['categories'] = categories_ls

filename = 'train.json'
with open(filename, 'w') as f:
    f.write(json.dumps(final_dict))
