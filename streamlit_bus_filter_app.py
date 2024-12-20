import streamlit as st
import pandas as pd
import mysql.connector
import os

# --- SQL DATABASE SETUP ---
# Fetch MySQL password securely from environment variables
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "PASSWORD")  # Replace with your actual password in the env variable

# Establish the connection to MySQL
@st.cache_resource
def get_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=MYSQL_PASSWORD,
            database="REDBUS",
            auth_plugin="mysql_native_password"  # Explicitly specify the plugin
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Fetch data from the 'bus_routes' table
@st.cache_data
def fetch_data():
    connection = get_connection()
    if connection:
        query = "SELECT * FROM bus_routes"
        df = pd.read_sql(query, connection)
        connection.close()

        # Fill missing seats and ensure correct types
        df['seats_available'] = df['seats_available'].fillna(0).astype(int)
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame on connection failure

# --- STREAMLIT APP DESIGN ---
# App Header
st.markdown(
    """
    <style>
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
    .footer {
        text-align: center;
        margin-top: 20px;
        color: gray;
        font-size: 0.9rem;
    }
    .bus-card {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #F9F9F9;
        color: #333;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .bus-card h3 {
        color: #D73036;
    }
    .bus-card p {
        color: #555;
    }
    </style>
    <div class="header">
        <h1>RedBus - Filter Your Bus</h1>
        <img src="https://s3.rdbuz.com/Images/rdc/rdc-redbus-logo.svg" style="width: 100px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

# Fetch bus data
df = fetch_data()

if df.empty:
    st.error("Unable to fetch data. Please check your database connection.")
else:
    # Sidebar Filters
    st.sidebar.title("🔍 Filters")

    # State Filter
    states = ["All"] + list(df['state'].dropna().unique())
    state_filter = st.sidebar.selectbox("Select State", options=states)
    if state_filter != "All":
        df = df[df['state'] == state_filter]

    # Bus Type Filter
    bustypes = ["All"] + list(df['bustype'].dropna().unique())
    bustype_filter = st.sidebar.selectbox("Bus Type", options=bustypes)
    if bustype_filter != "All":
        df = df[df['bustype'] == bustype_filter]

    # Route Name Filter
    routes = ["All"] + list(df['route_name'].dropna().unique())
    route_filter = st.sidebar.selectbox("Route Name", options=routes)
    if route_filter != "All":
        df = df[df['route_name'] == route_filter]

    # Price Range Filter
    if not df.empty:
        min_price, max_price = st.sidebar.slider(
            "Price Range", min_value=int(df['price'].min()), max_value=int(df['price'].max()), value=(0, 6000)
        )
        df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

    # Star Rating Filter
    if not df.empty:
        min_rating, max_rating = st.sidebar.slider(
            "Star Rating", min_value=1.0, max_value=5.0, value=(1.0, 5.0)
        )
        df = df[(df['star_rating'] >= min_rating) & (df['star_rating'] <= max_rating)]

    # Seats Available Filter with NaN Handling
    if not df.empty:
        if pd.isna(df['seats_available']).all():
            st.warning("No bus available due to missing seat data.")
            df = pd.DataFrame()  # Reset DataFrame to empty
        else:
            df['seats_available'] = df['seats_available'].fillna(0).astype(int)
            max_seats = int(df['seats_available'].max())
            min_seats, max_seats = st.sidebar.slider(
                "Seats Available", min_value=0, max_value=max_seats, value=(0, max_seats)
            )
            df = df[(df['seats_available'] >= min_seats) & (df['seats_available'] <= max_seats)]

    # --- DISPLAY FILTERED RESULTS ---
    st.markdown("### Available Buses")
    if not df.empty:
        for _, row in df.iterrows():
            st.markdown(f"""
            <div class="bus-card">
                <h3>{row['busname']} ({row['bustype']})</h3>
                <p><strong>Route:</strong> {row['route_name']}</p>
                <p><strong>Departing:</strong> {row['departing_time']} | <strong>Reaching:</strong> {row['reaching_time']}</p>
                <p><strong>Duration:</strong> {row['duration']} | <strong>Seats Available:</strong> {row['seats_available']}</p>
                <p><strong>Price:</strong> ₹{row['price']} | <strong>Rating:</strong> ⭐ {row['star_rating']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No buses found matching the selected filters.")

    # Footer
    st.markdown(
        """
        <div class="footer">
            Powered by <strong>RedBus</strong>. Visit <a href="https://www.redbus.in" target="_blank">redBus.in</a> for more details.
        </div>
        """,
        unsafe_allow_html=True
    )
