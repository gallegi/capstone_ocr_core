#%%
import pandas as pd

#%%
df = pd.read_excel('sample.xlsx')
gg_df = pd.read_excel('google_output.xlsx',encoding='utf-8')
gg_df = gg_df[['x_mean','y_mean','word','image_name']]
#%%
z = pd.merge(df,gg_df,how='left',on='image_name')
z['distance'] = ((z['x_mean_x'] - z['x_mean_y'])**2 + (z['y_mean_x'] - z['y_mean_y'])**2)**(1/2)
z = z[z['distance']<2000]
#%%
z = z.sort_values("distance").groupby(['x_mean_x','y_mean_x','image_name'],as_index=False).first()

#%%
z.to_excel('label.xlsx',encoding='utf-8',index=False)