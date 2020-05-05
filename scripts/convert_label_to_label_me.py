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

df = pd.read_excel('label.xlsx', encoding='utf-8')
# %%
image_names = list(set(df['image_name'].values))
# %%
image_source = r'C:\Users\Binh Bum\Downloads\Photos\images/'

for image_name in tqdm(image_names):
    sub_df = df[df['image_name'] == image_name]
    sub_df[['x1','y1','x2','y2','x3','y3','x4','y4']] = sub_df[['x1','y1','x2','y2','x3','y3','x4','y4']].astype(float)
    data = {"version": "3.16.1",
            "flags": {},
            "shapes": [],
            "lineColor": [0, 255, 0, 128],
            "fillColor": [255, 0, 0, 128],
            "imagePath": image_name,
            "imageData": None}

    for row in sub_df.values:
        x_mean_x, y_mean_x, image_name, x1, y1, x2, y2, x3, y3, x4, y4, x_mean_y, y_mean_y, word, distance = tuple(row)
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