import streamlit as st
from flight_dashboard import Db
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import pandas as pd

# Creating the db object
db = Db()

# Sidebar
st.sidebar.title("Choose Insights")

user_options = st.sidebar.selectbox(
    "Menu", ["Select One", "Check_Flights", "Analytics", "Business Insights"]
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

    # Airline Frequency Pie Chart
    airline, frequency = db.airline_freq()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value",
        )
    )
    st.header("Airline Frequency Pie Chart")
    st.plotly_chart(fig)

    # Busiest Routes
    st.subheader("Busiest Routes")
    busiest_routes = db.busiest_routes()
    busiest_routes_df = pd.DataFrame(
        busiest_routes, columns=["Source", "Destination", "Total_Flights"]
    )
    st.dataframe(busiest_routes_df)

    # Seasonal Trends (Monthly) - Line chart
    st.subheader("Seasonal Trends (Monthly)")
    monthly_trends = db.seasonal_trends_monthly()
    monthly_trends_df = pd.DataFrame(monthly_trends, columns=["Month", "Total_Flights"])
    monthly_trends_df["Month"] = monthly_trends_df["Month"].str.strip()
    monthly_trends_df["Month"] = pd.Categorical(
        monthly_trends_df["Month"],
        categories=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        ordered=True,
    )
    monthly_trends_df.sort_values("Month", inplace=True)
    fig_monthly = px.line(
        monthly_trends_df,
        x="Month",
        y="Total_Flights",
        title="Monthly Flight Trends",
        labels={"Month": "Month", "Total_Flights": "Total Flights"},
    )
    st.plotly_chart(fig_monthly)

    # Seasonal Trends (Yearly) - Line chart
    st.subheader("Seasonal Trends (Yearly)")
    yearly_trends = db.seasonal_trends_yearly()
    yearly_trends_df = pd.DataFrame(yearly_trends, columns=["Season", "Total_Flights"])

    # Manually order seasons for better line chart visualization
    season_order = ["Winter", "Spring", "Summer", "Fall"]
    yearly_trends_df["Season"] = pd.Categorical(
        yearly_trends_df["Season"], categories=season_order, ordered=True
    )
    yearly_trends_df.sort_values("Season", inplace=True)

    fig_yearly = px.line(
        yearly_trends_df,
        x="Season",
        y="Total_Flights",
        title="Yearly Flight Trends by Season",
        labels={"Season": "Season", "Total_Flights": "Total Flights"},
    )
    st.plotly_chart(fig_yearly)

elif user_options == "Business Insights":
    st.title("Business Insights")

    # Top Revenue-Generating Routes
    st.subheader("Top Revenue-Generating Routes")
    top_routes = db.revenue_insights()
    top_routes_df = pd.DataFrame(
        top_routes, columns=["Source", "Destination", "Revenue"]
    )
    st.dataframe(top_routes_df)

    # Top Airlines by Revenue
    st.subheader("Top Airlines by Revenue")
    top_airlines = db.highest_revenue_airline()
    top_airlines_df = pd.DataFrame(top_airlines, columns=["Airline", "Total_Revenue"])
    st.dataframe(top_airlines_df)

    # Revenue by Source Cities
    st.subheader("Revenue by Source Cities")
    source_revenue = db.top_revenue_source_cities()
    source_revenue_df = pd.DataFrame(
        source_revenue, columns=["Source", "Total_Revenue"]
    )

    source_revenue_df["Total_Revenue"] = (
        source_revenue_df["Total_Revenue"]
        .str.replace("M", "", regex=False)
        .astype(float)
        * 1_000_000
    )

    fig_source = px.bar(
        source_revenue_df,
        x="Source",
        y="Total_Revenue",
        title="Revenue by Source Cities",
        labels={"Source": "Source City", "Total_Revenue": "Total Revenue (in $)"},
    )
    st.plotly_chart(fig_source)

    # Revenue by Destination Cities
    st.subheader("Revenue by Destination Cities")
    destination_revenue = db.top_revenue_destination_cities()
    destination_revenue_df = pd.DataFrame(
        destination_revenue, columns=["Destination", "Total_Revenue"]
    )
    destination_revenue_df["Total_Revenue"] = (
        destination_revenue_df["Total_Revenue"]
        .str.replace("M", "", regex=False)
        .astype(float)
        * 1_000_000
    )

    fig_destination = px.bar(
        destination_revenue_df,
        x="Destination",
        y="Total_Revenue",
        title="Revenue by Destination Cities",
        labels={"Destination": "Destination City", "Total_Revenue": "Total Revenue"},
    )
    st.plotly_chart(fig_destination)

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
