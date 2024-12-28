import streamlit as st
from flight_dashboard import Db
import plotly.graph_objects as go
from PIL import Image

# creating the db object"
db = Db()

# sideBar
st.sidebar.title("Choose Insights")

user_options = st.sidebar.selectbox(
    "Menu", ["Select One", "Check_Flights", "Analytics"]
)

if user_options == "Check_Flights":
    st.title("Check Flights")

    col1, col2 = st.columns(2)

    city = db.fetch_city_name()
    with col1:
        source = st.selectbox("Source", sorted(city))
    with col2:
        destination = st.selectbox("Destination", sorted(city))

    if st.button("Search"):
        results = db.fetch_all_cities(source, destination)
        if isinstance(results, str):
            st.warning(results)
        else:
            st.dataframe(results)


elif user_options == "Analytics":
    st.title("Analytics")
    airline, frequency = db.airline_freq()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value",
        )
    )

    st.header("Pie chart")
    st.plotly_chart(fig)
else:
    # Title
    st.title("Interactive Flight Data Analysis")
    st.write(
        """
        Welcome to the Flight Analytics Dashboard! This tool allows you to:
        
        - Check available flights between selected cities.
        - Analyze trends like airline frequency with interactive visualizations.
        - Access data hosted on Supabase for seamless performance.
        - Benefit from efficient querying powered by advanced SQL techniques.
        
        Explore the dashboard to gain insights into flight data and trends!
        """
    )

    # Image
    image = Image.open(
        "business-technology-travel-transportation-concept-600nw-1319730824.png"
    )
    resized_image = image.resize((650, 590))
    st.image(resized_image)
