###-----------------------------------------------------------------------------------------
### Libraries
###-----------------------------------------------------------------------------------------
from streamlit_folium import st_folium
from bokeh.models.widgets import Div
from folium import IFrame
import streamlit as st
import pandas as pd
import folium
import base64
import math

###-----------------------------------------------------------------------------------------
### Dataset
###-----------------------------------------------------------------------------------------
df = pd.read_csv('Miscellaneous/data.csv', sep=';')
df_from_2015 = df[df['Year']>= 2015]
data = df_from_2015

###-----------------------------------------------------------------------------------------
### Initial settings (of the map)
###-----------------------------------------------------------------------------------------
resolution = 75
width      = 7
height     = 3
station    = '42'
lon, lat   = 15.004,37.734
m          = folium.Map(location=[lat, lon], zoom_start=5)

###-----------------------------------------------------------------------------------------
### Utilities funtions:
###         isnan(value)
###         add_element_to_map(name, country, year, month, day, tsunami, earthquake)
###-----------------------------------------------------------------------------------------
def isnan(value):
    try:
        return math.isnan(float(value))
    except:
        return False


def add_element_to_map(name, country, year, month, day, tsunami, earthquake):

   png = 'Miscellaneous/images/' + name + '.jpg'
   encoded = base64.b64encode(open(png, 'rb').read())

   # -----------------------------------------------------
   # TSUNAMI      ❌ 
   # EARTHQUAKE   ❌ 
   # -----------------------------------------------------
   if ((isnan(tsunami) and isnan(earthquake))):
      html = f'''
         <font face="Arial">
            <table>
               <tr>
                  <th>🗻</th>
                  <td>{name}</td>
               </tr>
               <tr>
                  <th>🌍</th>
                  <td>{country}</td>
               </tr>
               <tr>
                  <th>💥</th>
                  <td>{year}</td>
            </table>
         </font><br>
      '''
      html    = html + '''<img src="data:image/png;base64,{}">'''
      html    = html.format
      iframe  = IFrame(html(encoded.decode('UTF-8')), width=(width*resolution)-110, height=(height*resolution)+120)
      popup   = folium.Popup(iframe, max_width=2650)
      icon    = folium.Icon(color="blue", icon="ok")
      marker  = folium.Marker(location=[lon, lat], popup=popup, icon=icon)
      marker.add_to(m)

   # -----------------------------------------------------
   # TSUNAMI      ❌
   # EARTHQUAKE   ✅ 
   # -----------------------------------------------------
   elif (isnan(tsunami)):
      html = f'''
         <font face="Arial">
            <table>
               <tr>
                  <th>🗻</th>
                  <td>{name}</td>
               </tr>
               <tr>
                  <th>🌍</th>
                  <td>{country}</td>
               </tr>
               <tr>
                  <th>💥</th>
                  <td>{year}</td>
            </table>
         </font><br>
         <font face="Arial" color="#B53737">
            <b>In {year} the eruption generated an earthquake! ⛔️</b><br><br>
         </font>
      '''
      html    = html + '''<img src="data:image/png;base64,{}">'''
      html    = html.format
      iframe  = IFrame(html(encoded.decode('UTF-8')), width=(width*resolution)-110, height=(height*resolution)+170)
      popup   = folium.Popup(iframe, max_width=2650)
      icon    = folium.Icon(color="red", icon="ok")
      marker  = folium.Marker(location=[lon, lat], popup=popup, icon=icon)
      marker.add_to(m)

   # -----------------------------------------------------
   # TSUNAMI      ✅
   # EARTHQUAKE   ❌
   # -----------------------------------------------------
   elif (isnan(earthquake)):
      html = f'''
         <font face="Arial">
            <table>
               <tr>
                  <th>🗻</th>
                  <td>{name}</td>
               </tr>
               <tr>
                  <th>🌍</th>
                  <td>{country}</td>
               </tr>
               <tr>
                  <th>💥</th>
                  <td>{year}</td>
            </table>
         </font><br>
         <font face="Arial" color="#B53737">
            <b>In {year} the eruption generated a tsunami! ⛔️</b><br><br>
         </font>
      '''
      html    = html + '''<img src="data:image/png;base64,{}">'''
      html    = html.format
      iframe  = IFrame(html(encoded.decode('UTF-8')), width=(width*resolution)-110, height=(height*resolution)+170)
      popup   = folium.Popup(iframe, max_width=2650)
      icon    = folium.Icon(color="red", icon="ok")
      marker  = folium.Marker(location=[lon, lat], popup=popup, icon=icon)
      marker.add_to(m)

   # -----------------------------------------------------
   # TSUNAMI      ✅
   # EARTHQUAKE   ✅
   # -----------------------------------------------------
   else:
      html = f'''
         <font face="Arial">
            <table>
               <tr>
                  <th>🗻</th>
                  <td>{name}</td>
               </tr>
               <tr>
                  <th>🌍</th>
                  <td>{country}</td>
               </tr>
               <tr>
                  <th>💥</th>
                  <td>{year}</td>
               </table>
         </font><br>
         <font face="Arial" color="#B53737">
            <b>In 2019 the eruption generated a tsunami and an earthquake! ⛔️</b><br><br>
         </font>
      '''
      html    = html + '''<img src="data:image/png;base64,{}">'''
      html    = html.format
      iframe  = IFrame(html(encoded.decode('UTF-8')), width=(width*resolution)-110, height=(height*resolution)+190)
      popup   = folium.Popup(iframe, max_width=2650)
      icon    = folium.Icon(color="red", icon="ok")
      marker  = folium.Marker(location=[lon, lat], popup=popup, icon=icon)
      marker.add_to(m)

###-----------------------------------------------------------------------------------------
### Add elements to the map
###-----------------------------------------------------------------------------------------
for i in range(len(data)):
    lon        = float(data.iloc[i]['Coordinates'].split(',')[0])
    lat        = float(data.iloc[i]['Coordinates'].split(',')[1])
    name       = data.iloc[i]['Volcano Name']
    country    = data.iloc[i]['Country']
    tsunami    = data.iloc[i]['Flag Tsunami']
    earthquake = data.iloc[i]['Flag Earthquake']
    year       = data.iloc[i]['Year']
    month      = data.iloc[i]['Month']
    day        = data.iloc[i]['Day']
    add_element_to_map(name, country, year, month, day, tsunami, earthquake)
    print('Added volcano ', name, ', which erupted in ', year)

###-----------------------------------------------------------------------------------------
### Web-Page Settings
###-----------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
c1, c2, c3 = st.columns((20, 60, 20))
c4, c5, c6 = st.columns((5, 90, 5))

with c2:

    if st.button('Hello 👋'):
        js = "window.location.href = 'https://paulinomoskwa.github.io/Hello/'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)

    st.markdown('''
        <h1 style='text-align: center;'>Volcanic Eruptions 2015-2022 🌋</h1>
        <p style='text-align: center;'>Navigate the map to find out which volcanoes erupted from 2015 to 2022.<br>
        <p1 style="color:red">Some eruptions <p2 style="color:black">caused tsunamis or earthquakes, <p3 style="color:blue">others <p4 style="color:black">did not.</p4></p3></p2></p1>
        <br>Data comes from 
        <a href="https://public.opendatasoft.com/explore/dataset/significant-volcanic-eruption-database/information/?location=2,3.18934,-2.23&basemap=jawg.light">significant volcanic eruption database</a>.
        </p>
    ''', unsafe_allow_html=True)
    st.markdown('')

with c5:
    st_folium(m, width=1400, height=500)
