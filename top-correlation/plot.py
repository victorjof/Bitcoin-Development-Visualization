import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tools


tools.set_credentials_file(username='ghost-42', api_key='1oIJ0CFL9cP2XfIqvlJ6')

import pandas as pd 

df = pd.read_csv("./contribuition_stats.csv")

# 'status' precisa ser um valor inteiro que o represente.
# O mapeamento foi feito para { 'non-member': 0, 'member':1 }
df['status'] = list(map(lambda x: 0 if x[:3] == "non" else 1, df['status']))

# Ordenando o conjunto de dados de forma decrescente 
df = df.sort_values(by=["num_issues", "num_pulls", "num_commits"], ascending=[False,False,False])

length = len(df["status"])

print("Cabeçalho do conjunto de dados")
print(df.head(n = 20))
print("Tamanho do conjunto:", length)

# Calculo dos maximos e mínimos de cada intervalo.
# OBS: Usado como parametro para construir a visualização de coordenadas paralelas
minimo_issues , maximo_issues  = [min(df['num_issues' ]),max(df['num_issues' ])]
minimo_pulls  , maximo_pulls   = [min(df['num_pulls'  ]),max(df['num_pulls'  ])]
minimo_commits, maximo_commits = [min(df['num_commits']),max(df['num_commits'])]

minimo_all = min(minimo_commits, minimo_issues, minimo_pulls)
maximo_all = max(maximo_commits, maximo_issues, maximo_pulls)

print()
print("Minimos e maximos")
print("Issues : [", minimo_issues , maximo_issues , "]")
print("Pulls  : [", minimo_pulls  , maximo_pulls  , "]")
print("Commits: [", minimo_commits, maximo_commits, "]")
print("All    : [", minimo_all    , maximo_all    , "]")

status_0 = df['status'][0]

print()
print("Legenda das cores das linhas")
if(status_0 == 1):
    print("[0,'blue']: member")
    print("[1,'red ']: non-member")
else:
    print("[1,'red ']: member")
    print("[0,'blue']: non-member")

# Conjunto de dados sem slice
data = [
    go.Parcoords(
        line = dict(color = df['status'], colorscale = [[0,'blue'],[1,'red']]),
        dimensions = [
            dict(range = [-2, 3],
                tickvals = [0,1],
                label = 'Status',
                ticktext = ["Non-member", "Member"],
                values = df['status']),
            dict(range = [minimo_issues, maximo_issues],
                #constraintrange = [1,2], # intervalo inicial desbloquiado
                label = 'Issues',
                values = df['num_issues']),
            dict(range = [minimo_pulls, maximo_pulls],
                label = 'Pulls',
                values = df['num_pulls']),
            dict(range = [minimo_commits, maximo_commits],
                label = 'Commits',
                values = df['num_commits']),
        ]
    )
]

'''
# Intervalo para o slace do conjunto de dados
end_interval   = 20

data = [
    go.Parcoords(
        line = dict(color = df['status'], colorscale = [[0,'blue'],[1,'red']]),
        dimensions = [
            dict(range = [-2, 3],
                tickvals = [0,1],
                label = 'Status',
                ticktext = ["Non-member", "Member"],
                values = df['status'][:end_interval]),
            dict(range = [minimo_issues, maximo_issues],
                #constraintrange = [1,2], # intervalo inicial desbloquiado
                label = 'Issues',
                values = df['num_issues'][:end_interval]),
            dict(range = [minimo_pulls, maximo_pulls],
                label = 'Pulls',
                values = df['num_pulls'][:end_interval]),
            dict(range = [minimo_commits, maximo_commits],
                label = 'Commits',
                values = df['num_commits'][:end_interval]),
        ]
    )
]
'''
layout = go.Layout(
    plot_bgcolor = '#E5E5E5',
    paper_bgcolor = '#E5E5E5',
    showlegend = True
)

fig = go.Figure(data = data, layout = layout)
py.plot(fig, filename = 'parcoords-basic')
