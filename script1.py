from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/plot/')
def plot():
    
    import pandas as pd
    import numpy as np

    #import folium
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.resources import CDN

    from bokeh.models import ColumnDataSource, ColorBar
    from bokeh.palettes import Spectral6
    from bokeh.transform import linear_cmap
    df=pd.read_csv("Santa_Margarita_pre.csv",parse_dates=['fecha'],decimal='.')
    aapl = np.array(df['pronostico'])
    aapl_dates = np.array(df['fecha'], dtype=np.datetime64)

    

    # output to static HTML file
    #0output_file("app3/templates/SMargarita.html", title="Prediction example")




    # add renderers
    #Use the field name of the column source
    mapper = linear_cmap(field_name='y', palette=Spectral6 ,low=min(aapl) ,high=max(aapl))

    source = ColumnDataSource(dict(x=aapl_dates,y=aapl))

    # create a new plot with a a datetime axis type
    p =figure(plot_width=1000, plot_height=500, x_axis_type="datetime", title="Previsión niveles NO2 (Est. Santa Margarita, A Coruña, Galicia, España)")
    p.circle(x='x', y='y', line_color=mapper,color=mapper, fill_alpha=1, size=12, source=source)

    color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))

    p.add_layout(color_bar, 'right')


    #p.circle(aapl_dates, aapl, size=10, color='black', alpha=0.2, legend='NO2')
    p.line(aapl_dates, aapl, color='navy')
    script1,div1= components(p)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]
    return render_template("plot.html",script1=script1,div1=div1,
                           cdn_css=cdn_css,cdn_js=cdn_js)
                           
                           

    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
