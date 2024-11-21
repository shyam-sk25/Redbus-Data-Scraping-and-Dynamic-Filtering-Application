import streamlit as st
import mysql.connector
import pandas as pd

# MySQL Database Connection
mydb = mysql.connector.connect(
    host="127.0.0.1",  # MySQL host (commonly localhost)
    user="root",       # Your MySQL username
    password="SHYAM@sk25",  # Your MySQL password
    database="REDBUS"  # Name of your database
)

# Create a cursor object to interact with the database
cursor = mydb.cursor()

# SQL Query to fetch all data from the bus_routes table
query = "SELECT * FROM bus_routes"
cursor.execute(query)

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Convert the fetched data into a DataFrame
columns = ['id', 'route_name', 'route_link', 'busname', 'bustype', 'departing_time', 'duration', 'reaching_time', 'price', 'seats_available', 'star_rating']
df = pd.DataFrame(rows, columns=columns)

# Close the cursor and connection after fetching data
cursor.close()
mydb.close()

# Convert time columns to proper datetime format
df['departing_time'] = pd.to_datetime(df['departing_time'], errors='coerce').dt.time
df['reaching_time'] = pd.to_datetime(df['reaching_time'], errors='coerce').dt.time

# Handle cases where time is NaT or NaN and replace with a default time '00:00:00'
df['departing_time'] = df['departing_time'].fillna(pd.to_datetime('00:00:00').time())
df['reaching_time'] = df['reaching_time'].fillna(pd.to_datetime('00:00:00').time())

# Streamlit app header
st.title("RedBus Bus Routes")
st.write("Explore the bus routes with various filters")

# Filter for busname (All option included)
busname_filter = st.selectbox("Select Bus Name", options=["All"] + list(df['busname'].unique()))

# Filter for bustype (All option included)
bustype_filter = st.selectbox("Select Bus Type", options=["All"] + list(df['bustype'].unique()))

# Filter for route_name (All option included)
route_filter = st.selectbox("Select Route Name", options=["All"] + list(df['route_name'].unique()))

# Filter for price (range)
price_filter = st.selectbox("Select Price Range", options=["All", "250-500", "500-1000", "1000+"])

# Filter for star_rating
star_rating_filter = st.slider("Select Star Rating", min_value=1, max_value=5, value=(1, 5))

# Filter for seats_available
seats_filter = st.slider("Select Seat Availability", min_value=0, max_value=100, value=(0, 100))

# Filter for duration
duration_filter = st.selectbox("Select Duration Filter", options=["All", "1-2 hours", "2-3 hours", "3+ hours"])

# Filter for departing_time (Anytime option added)
departing_time_filter = st.selectbox("Select Departing Time", options=["Anytime", "Morning (06:00-12:00)", "Afternoon (12:00-18:00)", "Night (18:00-24:00)"])

# Filter for reaching_time (Anytime option added)
reaching_time_filter = st.selectbox("Select Reaching Time", options=["Anytime", "Morning (06:00-12:00)", "Afternoon (12:00-18:00)", "Night (18:00-24:00)"])

# Apply filters

# Busname filter
if busname_filter != "All":
    df = df[df['busname'] == busname_filter]

# Bustype filter
if bustype_filter != "All":
    df = df[df['bustype'] == bustype_filter]

# Route filter
if route_filter != "All":
    df = df[df['route_name'] == route_filter]

# Price filter
if price_filter != "All":
    if price_filter == "250-500":
        df = df[(df['price'] >= 250) & (df['price'] <= 500)]
    elif price_filter == "500-1000":
        df = df[(df['price'] > 500) & (df['price'] <= 1000)]
    elif price_filter == "1000+":
        df = df[df['price'] > 1000]

# Star rating filter
df = df[df['star_rating'].between(star_rating_filter[0], star_rating_filter[1])]

# Seat availability filter
df = df[(df['seats_available'] >= seats_filter[0]) & (df['seats_available'] <= seats_filter[1])]

# Duration filter
if duration_filter != "All":
    if duration_filter == "1-2 hours":
        df = df[df['duration'].str.contains("1 hour|2 hours")]
    elif duration_filter == "2-3 hours":
        df = df[df['duration'].str.contains("2 hours|3 hours")]
    elif duration_filter == "3+ hours":
        df = df[df['duration'].str.contains("3 hours")]

# Departing Time filter
if departing_time_filter != "Anytime":
    if departing_time_filter == "Morning (06:00-12:00)":
        df = df[df['departing_time'].between(pd.to_datetime('06:00:00').time(), pd.to_datetime('12:00:00').time())]
    elif departing_time_filter == "Afternoon (12:00-18:00)":
        df = df[df['departing_time'].between(pd.to_datetime('12:00:00').time(), pd.to_datetime('18:00:00').time())]
    elif departing_time_filter == "Night (18:00-24:00)":
        df = df[df['departing_time'].between(pd.to_datetime('18:00:00').time(), pd.to_datetime('23:59:59').time())]

# Reaching Time filter
if reaching_time_filter != "Anytime":
    if reaching_time_filter == "Morning (06:00-12:00)":
        df = df[df['reaching_time'].between(pd.to_datetime('06:00:00').time(), pd.to_datetime('12:00:00').time())]
    elif reaching_time_filter == "Afternoon (12:00-18:00)":
        df = df[df['reaching_time'].between(pd.to_datetime('12:00:00').time(), pd.to_datetime('18:00:00').time())]
    elif reaching_time_filter == "Night (18:00-24:00)":
        df = df[df['reaching_time'].between(pd.to_datetime('18:00:00').time(), pd.to_datetime('23:59:59').time())]

# Display the filtered DataFrame
st.write("Filtered Bus Routes", df)

# Display the DataFrame in a table format for better visualization
st.dataframe(df)
