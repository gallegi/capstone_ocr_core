#%%
import pandas as pd
import cv2
import numpy as np
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
#%%

df = pd.read_excel('label.xlsx',encoding='utf-8')
#%%
selected_image_name = 'IMG_1860.jpg'
image_source = r'C:\Users\Binh Bum\Downloads\Photos\images/'

sub_df= df[df['image_name'] == selected_image_name]
#%%
sub_df[['x1','y1','x2','y2','x3','y3','x4','y4']] = sub_df[['x1','y1','x2','y2','x3','y3','x4','y4']].astype(int)
#%%
img = cv2.imread(image_source+selected_image_name)
for row in sub_df.values:
    x_mean_x,y_mean_x,image_name,x1,y1,x2,y2,x3,y3,x4,y4,x_mean_y,y_mean_y,word,distance = tuple(row)
    cnt = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
    cv2.drawContours(img,[cnt],0,(255,0,0),5)

fontpath = "./AlegreyaSansSC-Medium.otf" # <== 这里是宋体路径
font = ImageFont.truetype(fontpath, 32)
img_pil = Image.fromarray(img)
draw = ImageDraw.Draw(img_pil)
print(' '.join(list(sub_df['word'].values)))
for row in sub_df.values:
    x_mean_x,y_mean_x,image_name,x1,y1,x2,y2,x3,y3,x4,y4,x_mean_y,y_mean_y,word,distance = tuple(row)

    # cv2.circle(img,(int(x_mean_x),int(y_mean_x)),5,(0,255,0),-1)

    draw.text((int(x_mean_x),int(y_mean_x)),  '.', font = font, fill = (255,0,0,255))
    draw.text((int(x_mean_x),int(y_mean_x)),  word, font = font, fill = (0,255,0,255))
img = np.array(img_pil)
cv2.imwrite('sample.png',img)


#%%

