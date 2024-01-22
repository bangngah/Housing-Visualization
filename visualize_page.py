import streamlit as st 
import pandas as pd
import folium 
from streamlit_folium import st_folium
import plotly.express as px


def highlight_property_name(s, selected_prop_names):
    """
    Highlight the cells in the DataFrame based on the selected property names.
    """
    colors = ['background-color: yellow' if prop_name in selected_prop_names else '' for prop_name in s.index]
    return colors


def show_visualization_page(df_property):
    st.title("Map  ")
    

    map = folium.Map(location=[3.136145, 101.663632], zoom_start=9, tiles='cartoDB positron', scrollWheelZoom=False)

    # Aggregating data by district
    district_data = df_property.groupby('district').agg(
        average_rent=('monthly_rent', lambda x: round(x.mean())),  # Rounding the average rent
        average_rooms=('rooms', lambda x: round(x.mean())),  # Average number of rooms
        average_bathrooms=('bathroom', lambda x: round(x.mean())),  # Average number of bathrooms
        property_count=('monthly_rent', 'size'),  # Counting the number of properties
        property_types=('property_type', lambda x: ', '.join(set(x)))  # Types of properties
    ).reset_index()

    choropleth = folium.Choropleth(
            geo_data='DATA/mergedfile.geojson',
            data=df_property,
            columns=('district', 'monthly_rent'),
            key_on='feature.properties.name',
            fill_opacity=0.5,
            line_opacity=0.9,
            highlight=True,
        )
    choropleth.geojson.add_to(map)
    choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['name'], labels=False)
        )

    st_map = st_folium(map, width=800, height=600)
    district = ''
    if st_map['last_active_drawing']:
            district = st_map['last_active_drawing']['properties']['name']
    

    # Initialize district_info
    district_info = None            
    # Folium Choropleth map setup
    # Check if district is selected and get its information
    if district:
        district_info = district_data[district_data['district'] == district].iloc[0]

        # Creating a DataFrame for the selected district's information
        info_df = pd.DataFrame({
            'Metric': ['District', 'Average Monthly Rent', 'Average Number of Rooms', 'Average Number of Bathrooms', 'Number of Properties', 'Types of Properties'],
            'Value': [
                district,
                round(district_info['average_rent']),  # Rounded average rent
                round(district_info['average_rooms']),  # Average number of rooms
                round(district_info['average_bathrooms']),  # Average number of bathrooms
                district_info['property_count'],
                district_info['property_types']
            ]
        })

        st.write(f"### District Details")
        st.dataframe(info_df, width=700)

    st.write("-----")

    c1, c2 = st.columns((1, 1))
    with c1:
         df_property_general = pd.read_csv('district_summary.csv')
         stacked_bar_fig = px.bar(df_property_general, x='district', y='average_rent', color='property_count',
                              title='Monthly Rent by District and Property Type',
                              labels={'monthly_rent': 'Monthly Rent', 'district': 'District'},
                              height=500)
         st.plotly_chart(stacked_bar_fig)


    with c2: 
        bar_fig = px.bar(df_property, x='district', y='monthly_rent', color='district',
            title='Monthly Rent by District',
            labels={'monthly_rent': 'Monthly Rent', 'district': 'District'})
        st.plotly_chart(bar_fig)

    st.write("-----")

  # Filter options
    st.sidebar.header("Filter Options")

    # Selecting Property Type
    property_type_list = ['all'] + df_property['property_type'].unique().tolist()
    property_type = st.sidebar.selectbox("Property Type", property_type_list)

    # Selecting District
    district_list = ['all'] + df_property['district'].unique().tolist()
    district = st.sidebar.selectbox("District", district_list)

    # Selecting Monthly Rent Range
    min_rent = int(df_property['monthly_rent'].min())
    max_rent = 5000  # Setting the maximum rent to 5000
    monthly_rent = st.sidebar.slider("Monthly Rent", min_rent, max_rent, (min_rent, max_rent))

    # Selecting Number of Rooms
    max_rooms = int(df_property['rooms'].max())
    room = st.sidebar.number_input("Number of Rooms", 1, max_rooms, 1)

    # Selecting Number of Bathrooms
    max_bathrooms = int(df_property['bathroom'].max())
    bathroom = st.sidebar.number_input("Number of Bathrooms", 1, max_bathrooms, 1)

    # Adjusting filter options to 'all'
    property_type = property_type if property_type != 'all' else df_property['property_type']
    district = district if district != 'all' else df_property['district']

    # Filtering the DataFrame
    filtered_data = df_property[
    (df_property['property_type'] == property_type) &
    (df_property['district'] == district) &
    (df_property['monthly_rent'] >= monthly_rent[0]) &
    (df_property['monthly_rent'] <= monthly_rent[1]) &
    (df_property['rooms'] == room) &
    (df_property['bathroom'] == bathroom)
]
    

    # Stacked Bar Chart

    # Create stacked bar chart for monthly rent by district

    # Displaying the filtered DataFrame
    st.write(f"### Filtered Data:")
    st.dataframe(filtered_data, width=2000)



