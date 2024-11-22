import streamlit as st
import pandas as pd
import mysql.connector

# MySQL Database Connection
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="local_host",  # MySQL host (commonly localhost)
        user="root",       # Your MySQL username
        password="password",  # Your MySQL password
        database="REDBUS"  # Name of your database
    )

# Fetch data from the 'bus_routes' table
@st.cache_data
def fetch_data():
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM bus_routes"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ['id', 'route_name', 'route_link', 'busname', 'bustype', 'departing_time', 'duration', 'reaching_time', 'price', 'seats_available', 'star_rating']
    df = pd.DataFrame(rows, columns=columns)
    cursor.close()
    connection.close()
    return df

# Fetch data into a DataFrame
df = fetch_data()

# Page Styling for Header and Filters
st.markdown("""
    <style>
    body {
        background-color: white;
    }
    .header {
        background-color: #D73036;
        padding: 20px;
        text-align: center;
        color: white;
        font-family: Arial, sans-serif;
    }
    .header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    .bus-card {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        font-family: Arial, sans-serif;
    }
    .bus-card h3 {
        color: #D73036;
        margin: 0;
        font-size: 1.5rem;
    }
    .bus-card p {
        margin: 5px 0;
        color: #333;
        font-size: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 20px;
        color: gray;
        font-size: 0.9rem;
    }
    </style>
    <div class="header">
        <h1>RedBus - Filter Your Bus</h1>
        <img src="https://s3.rdbuz.com/Images/rdc/rdc-redbus-logo.svg" alt="RedBus Logo" style="width: 100px; height: auto;">
    </div>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.title("🔍 Filters")
st.sidebar.markdown("Use the filters below to customize your search:")

# Filter for "Bus Type"
bustype_filter = st.sidebar.selectbox("Bus Type", options=["All"] + list(df['bustype'].unique()))
if bustype_filter != "All":
    df = df[df['bustype'] == bustype_filter]

# Filter for "Route Name"
route_filter = st.sidebar.selectbox("Route Name", options=["All"] + list(df['route_name'].unique()))
if route_filter != "All":
    df = df[df['route_name'] == route_filter]

# Filter for "Price Range"
min_price, max_price = st.sidebar.slider("Price Range", min_value=0, max_value=6000, value=(0, 6000))
df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

# Filter for "Star Rating"
min_rating, max_rating = st.sidebar.slider("Star Rating", min_value=1.0, max_value=5.0, value=(1.0, 5.0))
df = df[(df['star_rating'] >= min_rating) & (df['star_rating'] <= max_rating)]

# Filter for "Seat Availability"
min_seats, max_seats = st.sidebar.slider("Seats Available", min_value=0, max_value=int(df['seats_available'].max()), value=(0, int(df['seats_available'].max())))
df = df[(df['seats_available'] >= min_seats) & (df['seats_available'] <= max_seats)]

# Display Filtered Results
st.markdown("### Available Buses")
if not df.empty:
    for _, row in df.iterrows():
        st.markdown(f"""
        <div class="bus-card">
            <h3>{row['busname']} ({row['bustype']})</h3>
            <p>Route: {row['route_name']}</p>
            <p>Departing: {row['departing_time']} | Reaching: {row['reaching_time']}</p>
            <p>Duration: {row['duration']} | Seats Available: {row['seats_available']}</p>
            <p>Price: ₹{row['price']} | Rating: ⭐ {row['star_rating']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No buses found matching the selected filters.")

# Footer
st.markdown("""
    <div class="footer">
        Powered by <strong>RedBus</strong>. Visit <a href="https://www.redbus.in" target="_blank">redBus.in</a> for more details.
    </div>
""", unsafe_allow_html=True)
