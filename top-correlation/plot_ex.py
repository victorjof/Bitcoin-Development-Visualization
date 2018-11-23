import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tools

import pandas as pd 

df = pd.read_csv("https://raw.githubusercontent.com/bcdunbar/datasets/master/iris.csv")

'''
data = [
    go.Parcoords(
        line = dict(color = df['species_id'],
                   colorscale = [[0,'#D7C16B'],[0.5,'#23D8C3'],[1,'#F3F10F']]),
        dimensions = list([
            dict(range = [0,8],
                constraintrange = [4,8],
                label = 'Sepal Length', values = df['sepal_length']),
            dict(range = [0,8],
                label = 'Sepal Width', values = df['sepal_width']),
            dict(range = [0,8],
                label = 'Petal Length', values = df['petal_length']),
            dict(range = [0,8],
                label = 'Petal Width', values = df['petal_width'])
        ])
    )
]
'''
#minimum,maximum = min(df['sepal_length']), max(df['sepal_length'])
#minimum,maximum = min(df['sepal_width'], minimum), max(df['sepal_width'], maximum)
#minimum,maximum = min(df['petal_length'], minimum), max(df['petal_length'], maximum)
#minimum,maximum = min(df['petal_width'], minimum), max(df['petal_width'], maximum)

minimum,maximum = [0,8]

data = [
    go.Parcoords(
        line = dict(color = df['species_id'],
                   colorscale = [[0,'#D7C16B'],[0.5,'#23D8C3'],[1,'#F3F10F']]),
        dimensions = [
            dict(range = [minimum,maximum],
                label = 'Sepal Length', values = df['sepal_length']),
            dict(range = [minimum,maximum],
                label = 'Sepal Width', values = df['sepal_width']),
            dict(range = [minimum,maximum],
                label = 'Petal Length', values = df['petal_length']),
            dict(range = [minimum,maximum],
                label = 'Petal Width', values = df['petal_width'])
        ]
    )
]

layout = go.Layout(
    plot_bgcolor = '#E5E5E5',
    paper_bgcolor = '#E5E5E5'
)

fig = go.Figure(data = data, layout = layout)
py.plot(fig, filename = 'parcoords-basic')