# %%
import json

import pandas as pd
import cv2
import numpy as np
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image

from tqdm import tqdm
# %%

df = pd.read_json(r'C:\Users\Binh Bum\Downloads\Photos\batch_2/google_output.json')
# %%
image_names = list(set(df['image_name'].values))
# %%
print(','.join(df.columns))
#%%
image_source = 'data/vnpost/vnpost_train/'

for image_name in tqdm(image_names):
    sub_df = df[df['image_name'] == image_name]
    if len(sub_df) ==0:
        continue
    sub_df[['x1','y1','x2','y2','x3','y3','x4','y4']] = sub_df[['x1','y1','x2','y2','x3','y3','x4','y4']].astype(float)
    data = {"version": "3.16.1",
            "flags": {},
            "shapes": [],
            "lineColor": [0, 255, 0, 128],
            "fillColor": [255, 0, 0, 128],
            "imagePath": image_name,
            "imageData": None}

    for row in sub_df.values:
        x1,y1,x2,y2,x3,y3,x4,y4,x_mean,y_mean,image_name,word = tuple(row)
        shape_data = {"label": word,
                      "line_color": None,
                      "fill_color": None,
                      "points": [
                          [x1, y1],
                          [x2, y2],
                          [x3, y3],
                          [x4, y4]
                      ],
                      "shape_type": "polygon",
                      "flags": {}}

        data['shapes'].append(shape_data)
    json.dump(data,open(image_source+image_name.replace('.jpg','.json'),'w',encoding='utf-8'))

