# Redbus Data Scraping and Dynamic Filtering Application

This project scrapes bus data from the Redbus website using **Selenium** and presents the data through an interactive web application built with **Streamlit**. The data is stored in an **SQL** database and can be filtered by various parameters such as bus type, price, route, and seat availability.

## Project Overview

This project automates the process of scraping detailed bus information from the Redbus platform. It retrieves data such as:
- **Bus routes**: Start and end points
- **Bus name**: Service provider
- **Bus type**: Sleeper, Seater, AC, Non-AC
- **Departure and arrival time**
- **Duration**
- **Star rating**
- **Price**
- **Seat availability**

The data is stored in a structured **SQL database** and can be analyzed and filtered interactively using a **Streamlit** app.

## Technologies Used

- **Selenium**: For web scraping the data from the Redbus website.
- **SQL**: For storing and querying the scraped data.
- **Pandas**: For data manipulation and analysis.
- **Streamlit**: For creating the interactive web application.
- **Python**: The primary programming language used.

**Problem Statement**
This project aims to revolutionize the transportation industry by automating the collection of bus travel data from Redbus and providing tools for analysis and filtering via an interactive web application.

**Project Deliverables**
Data Scraping: Selenium-based scripts to scrape bus data.
Database Storage: SQL database schema and scripts to store and retrieve the data.
Streamlit Application: Interactive app for data filtering and visualization.
Primary Tools and Libraries Used
Selenium: Used for web scraping to extract bus data such as routes, prices, seat availability, and ratings from the Redbus website.
SQL: Used for storing the scraped data in a structured database format and querying it for analysis and filtering.
Pandas: Used for manipulating, cleaning, and analyzing the scraped data before storing it in the database or displaying it in the application.
Streamlit: Used to create an interactive web application for filtering, displaying, and analyzing the scraped data.
**Usage**
The Streamlit app allows you to filter the bus data based on the following parameters:

Bus Type: Filter by sleeper, seater, AC, etc.
Route: Filter based on the start and end locations.
Price Range: Filter buses based on price.
Seat Availability: Filter based on available seats.
Use the interactive UI to customize your search and see real-time results

**Database Schema**
The data is stored in the bus_routes table, which has the following schema:

sql

**Table: bus_routes**

| Column Name        | Data Type  | Description                                      |
|--------------------|------------|--------------------------------------------------|
| id                 | INT        | Primary Key (Auto-incrementing)                  |
| route_name         | TEXT       | Name of the bus route (start and end locations)  |
| route_link         | TEXT       | URL to the route details                         |
| busname            | TEXT       | Name of the bus service provider                 |
| bustype            | TEXT       | Type of the bus (e.g., Sleeper, Seater, AC)      |
| departing_time     | TIME       | Scheduled departure time                         |
| duration           | TEXT       | Duration of the journey                          |
| reaching_time      | TIME       | Expected arrival time                            |
| star_rating        | FLOAT      | Rating of the bus (1-5 stars)                    |
| price              | DECIMAL    | Price of the bus ticket                          |
| seats_available    | INT        | Number of available seats                        |
**Column Descriptions:**
id: Auto-incrementing primary key for uniquely identifying each bus route entry.
route_name: The name of the bus route (start and end locations).
route_link: URL link to the detailed route information on the Redbus website.
busname: The name of the bus service provider.
bustype: Type of bus (e.g., Sleeper, Seater, AC, Non-AC).
departing_time: The time when the bus is scheduled to depart.
duration: Total duration of the bus journey.
reaching_time: Expected arrival time of the bus at the destination.
star_rating: Passenger rating of the bus service, typically ranging from 1 to 5 stars.
price: Cost of the bus ticket for the journey.
seats_available: Number of seats available on the bus at the time of scraping.

**Conclusion**
This project provides a powerful and interactive solution to extract, analyze, and filter bus data from Redbus. By automating the data collection process and presenting it through a user-friendly Streamlit interface, users can easily explore bus routes, pricing, seat availability, and more. The integration of SQL and Pandas allows for efficient data storage, manipulation, and querying.

**Future Improvements**
Implement additional filters such as bus amenities and operator details.
Integrate real-time data updates for price and availability.
Improve the application's performance for large datasets.
**Getting Involved**
Feel free to fork this repository, contribute, and suggest new features. Open issues if you encounter any problems, and pull requests are always welcome for improvements.
