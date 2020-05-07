#%%
import editdistance
import pandas as pd

from tqdm import tqdm
#%%

df_label = pd.read_json(r"C:\Users\Binh Bum\Downloads\Photos\test_label\label.json")
df_tess = pd.read_json(r"C:\Users\Binh Bum\Downloads\Photos\test_label\tess_output.json")
df_dl = pd.read_json(r"C:\Users\Binh Bum\Downloads\Photos\test_label\dl_output.json")
#%%
df_label = df_label[['image_name','word']]
df_label['label'] = df_label['word']
del df_label['word']
#%%
df_tess['tess_output'] = df_tess['word']
del df_tess['word']
#%%
df  = pd.merge(df_label,df_dl,on='image_name')

#%%
sims = []
for row in tqdm(df.values):
    image_name,label,tess_output= tuple(row)
    label = label.replace('\n','').lower()
    tess_output = tess_output.replace('\n','').lower()

    sims = 1 - editdistance.eval(label.lower(),tess_output.lower()) / max(len(label), len(tess_output))
#%%
df['sims'] = sims
df = df[['image_name','sims']]
#%%
df['sims'].mean()