import numpy as np
import pandas as pd
import janitor
from sklearn.manifold import TSNE
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import random
random.seed(42)

# convert recipes in text form to datamatrix with ingredients as features
def featurize_recipes(filename):
    ls = []
    with open(filename) as f:
        for line in f:
            d={}
            line=line.lower()
            line=line.replace('\n','')
            l=line.split(' - ')
            if 'stir' in l:
                d['stir']=1
            elif 'shake' in l:
                d['shake']=1
            if any(['twist' in word for word in l]):
                d['twist']=1
            if any(['wheel' in word for word in l]):
                d['wheel']=1
            if any(['cherry' in word for word in l]):
                d['cherry']=1
            for word in l:
                s=word.split('ml')
                if all(i not in s[0] for i in ['a','e','i','o','u','d']):
                    try:
                        d[s[1]]=float(s[0])
                    except:
                        pass
            d['name']=l[0]
            ls.append(d)
    empty = dict.fromkeys(set().union(*ls), 0)
    L1 = [dict(empty, **d) for d in ls]
    df=pd.DataFrame(L1)
    df=df.clean_names().remove_empty()
    return df

# dimensionality reduction with t-SNE and plotting in plotly with colored
# base alcohol; expects .csv data matrix and .txt recipe database
def get_recipe_tsne(filename,sourcefile):
    df=pd.read_csv(filename)
    df2=df.drop(['name'],axis=1)
    tsne=TSNE(n_components=2,verbose=1,perplexity=40,random_state=42,
              n_iter=1500)
    tsne_results=tsne.fit_transform(df2)
    df['x-tsne']=tsne_results[:,0]
    df['y-tsne']=tsne_results[:,1]
    rec=[]
    with open(sourcefile) as f1:
        for line in f1:
            line=line.replace('\n','')
            rec.append(line)
    df['recipe']=pd.Series(rec)
    a=df._white_rum>15
    b=df._brown_rum>15
    trace0=go.Scatter(x=df.loc[a|b,['x-tsne']].squeeze(),
                y=df.loc[a|b,['y-tsne']].squeeze(),
                name='Rum',mode='markers',
                      marker=dict(size=10,opacity=0.85,line=dict(width=2)),
                      text=df.loc[a|b,['recipe']].values.tolist())
    try:
        c=df._blanco_tequila>15
    except:
        c=False*len(df.name)
    try:
        d=df._reposado_tequila>15
    except:
        d=False*len(df.name)
    try:
        d2=df._mezcal>15
    except:
        d2=False*len(df.name)
    trace1=go.Scatter(x=df.loc[c|d|d2,['x-tsne']].squeeze(),
                y=df.loc[c|d|d2,['y-tsne']].squeeze(),
                name='Tequila',mode='markers',
                      marker=dict(size=10,opacity=0.85,line=dict(width=2)),
                      text=df.loc[c|d|d2,['recipe']].values.tolist())
    try:
        e=df._bourbon>15
    except:
        e=False*len(df.name)
    try:
        f=df._rye>15
    except:
        f=False*len(df.name)
    try:
        g=df._scotch>15
    except:
        g=False*len(df.name)
    try:
        h=df._irish_whiskey>15
    except:
        h=False*len(df.name)
    try:
        i=df._laphroaig_scotch>15
    except:
        i=False*len(df.name)
    trace2=go.Scatter(x=df.loc[e|f|g|h|i,['x-tsne']].squeeze(),
                y=df.loc[e|f|g|h|i,['y-tsne']].squeeze(),
                name='Whiskey',mode='markers',
                      marker=dict(size=10,opacity=0.85,line=dict(width=2)),
                      text=df.loc[e|f|g|h|i,['recipe']].values.tolist())
    try:
        j=df._cognac>15
    except:
        j=False*len(df.name)
    try:
        k=df._apple_brandy>15
    except:
        k=False*len(df.name)
    try:
        l=df._calvados>15
    except:
        l=False*len(df.name)
    trace3=go.Scatter(x=df.loc[j|k|l,['x-tsne']].squeeze(),
                y=df.loc[j|k|l,['y-tsne']].squeeze(),
                name='Brandy',mode='markers',
                      marker=dict(size=10,opacity=0.85,line=dict(width=2)),
                      text=df.loc[j|k|l,['recipe']].values.tolist())
    try:
        m=df._gin>15
    except:
        m=False*len(df.name)
    try:
        n=df._sloe_gin>15
    except:
        n=False*len(df.name)
    trace4=go.Scatter(x=df.loc[m|n,['x-tsne']].squeeze(),
                y=df.loc[m|n,['y-tsne']].squeeze(),
                name='Gin',mode='markers',
                      marker=dict(size=10,opacity=0.85,line=dict(width=2)),
                      text=df.loc[m|n,['recipe']].values.tolist())
    trace5=go.Scatter(x=df.loc[~(a|b|c|d|e|f|g|h|i|j|k|l|m|n),['x-tsne']].squeeze(),
                y=df.loc[~(a|b|c|d|e|f|g|h|i|j|k|l|m|n),['y-tsne']].squeeze(),
                name='Other',mode='markers',
                      marker=dict(size=10,opacity=0.85,line=dict(width=2)),
                      text=df.loc[~(a|b|c|d|e|f|g|h|i|j|k|l|m|n),['recipe']].values.tolist())
    data=[trace0,trace1,trace2,trace3,trace4,trace5]
    layout = go.Layout(title = 't-SNE of Cocktail Recipes',
                       hovermode='closest',
              yaxis = dict(title='Dim 2',zeroline = False),
              xaxis = dict(title='Dim 1',zeroline = False)
             )
    fig=dict(data=data,layout=layout)
    py.iplot(fig,filename='output_clustering')
