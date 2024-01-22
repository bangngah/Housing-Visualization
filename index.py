import streamlit as st 
import pandas as pd
from data_page import show_data_page
from visualize_page import show_visualization_page
from PIL import Image


st.set_page_config(layout="wide")

# Main function
def main():
    st.markdown("<h1 style='text-align: center; color: #00C59F;'>Housing Data Interacitve Visualization</h1>", unsafe_allow_html=True)
    st.caption(' Source : Federal Government')

    df_property = pd.read_csv('DATA/cleaned_dataset.csv')

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ("Home", "Data", "Visualization", "About"))

    # Display the selected page
    if choice == "Home":
        show_home_page()
    elif choice == "Data":
       show_data_page(df_property)
    elif choice == "Visualization":
        show_visualization_page(df_property)  # Pass the DataFrame here
    elif choice == "About":
        show_about_page()
    
     
#----------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions for each page
def show_home_page():
   

# Set page configuration - this should be the first Streamlit command

    # Header
    
    st.write("-----")


    st.title('Property Visualization')

    image = Image.open('images/kuala-lumpur-skyline-at-night.jpg')  # Update the path to your image
    st.image(image, caption='Kuala lumpur', width=900)

    st.write("""
        ## Property Listing Malaysia
        For this project, we are going to focus on the Selangor and Wilayah Persekutuan Kuala Lumpur as our main subject for analysis.
        There is abudance of housing for rent available here, thus we are going to explore and analyze more regarding Housing Data 
        interaction. The Property Data Visualization app is designed to provide insights into real estate markets 
        using data-driven visualizations. It aims to assist its users in making informed decisions 
        by presenting  property data in an intuitive and accessible format.
     """)

    st.write("-----")


    # Displaying the image and bullet points side by side

#----------------------------------------------------------------------------------------------------------------------------------------------------------

def show_about_page():
    st.title("About Page")
    st.write("Information about the app.")

    # Project Background
    # Technology Stack
    st.header("Technology Stack")
    st.write("""
        This application is built using a range of cutting-edge technologies:
        - **Python:** For backend logic and data processing.
        - **Streamlit:** To create the web application interface.
        - **Pandas:** For data manipulation and analysis.
        - **Folium:** Integrated with Streamlit for mapping and geospatial visualizations.
        - **GeoJSON:** For geographical data processing and mapping.
    """)

    # Team Information
    st.header("Meet the 'Team' ")
    st.write("""
        My name is Muhammad Afiq Ikmal, No matrics 208169 a Final Year Student for Bachelor of Computer Science department.
        The aim for this project is to apply data analytics and data science skills learn throughout the courses provided and
        provide a meaningful presentation. 
    """)

    # User Guide
    st.header("User Guide")
    st.write("""
        To get the most out of the app, follow these steps:
        1. **Navigate:** Use the sidebar to switch between different sections of the app.
        2. **calculate** calculate mortgages by providing user input in the provided box. 
        3. **Visualization Page:** Interact with the visualizations for deeper insights.
    """)

    # Acknowledgments
    st.header("Acknowledgments")
    st.write("""
        I would like to thank Prof Dr Fatimah Bt Sidi for guidance throughout this project and fellow friends 
        in making this project possible. Special thanks to the data providers and our beta testers for their 
        constructive feedback.
    """)

    # Contact Information
    st.header("Contact Information")
    st.write("""
        For more information, suggestions, or inquiries, please contact me at [afiqcisco@gmail.com]
        
    """)


#----------------------------------------------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    main()






