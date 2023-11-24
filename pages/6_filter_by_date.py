import mysql.connector
import streamlit as st
import pandas as pd

# Connect to the database
db = mysql.connector.connect(
    host='localhost',
    user='dbms',
    password='dbms',
    database='dbms'
)
c = db.cursor()

# Streamlit UI
st.title("Get Events in Date Range")

start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
if start_date <= end_date and st.button("Get Events"):
    try:
        # Call the stored procedure
        c.callproc("get_events_in_date_range", (start_date, end_date))

        # Retrieve the result set
        result = c.stored_results()
        data = list(result)[0].fetchall()

        if not data:
            st.warning("No events found in the specified date range.")
        else:
            df = pd.DataFrame(data, columns=["event_id", "event_title", "num_days", "event_price", "prize_amount", "start_date", "end_date", "event_description", "slots_left"])
            st.dataframe(df)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Close the database connection
db.close()
