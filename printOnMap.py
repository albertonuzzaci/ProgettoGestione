import pandas as pd
import numpy as np
import plotly.express as px
import random

#creating random data
df = pd.DataFrame({'lat':[51.56861],
       'lon':[ -0.1127],
       'category':[random.choice(['a', 'b', 'c', 'd'])]}
                  )

fig = px.scatter_mapbox(df, 
                        lat='lat',
                        lon='lon',
                        color='category',
                        center={'lat':51.509865,
                                'lon':-0.118092},
                        zoom=10)

fig.update_layout(mapbox_style='open-street-map')

fig.show()