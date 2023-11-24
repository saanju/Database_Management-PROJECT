import mysql.connector
import streamlit as st

def get_event_prize_stats():
    db = mysql.connector.connect(
        host='localhost',
        user='dbms',
        password='dbms',
        database='dbms'
    )
    cursor = db.cursor()

    # Find the maximum prize amount for each event
    max_prize_query = """
    SELECT event_id, MAX(prize_amount) AS max_prize
    FROM add_events
    GROUP BY event_id;
    """
    cursor.execute(max_prize_query)
    max_prize_data = cursor.fetchall()

    # Count the number of users registered for each event
    registered_users_query = """
    SELECT event_id, event_title, COUNT(DISTINCT user_id) AS registered_users
    FROM registration
    GROUP BY event_id;
    """
    cursor.execute(registered_users_query)
    registered_users_data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    db.close()

    return max_prize_data, registered_users_data

def main():
    st.title("Event Analysis")

    max_prize_data, registered_users_data = get_event_prize_stats()

    # Display the event data with max prize and registered users
    st.subheader("Events with Maximum Prize Amount")
    for row in max_prize_data:
        st.write(f"Event: {row[1]}, Max Prize Amount: {row[2]}")

    st.subheader("Events with Number of Registered Users")
    for row in registered_users_data:
        st.write(f"Event: {row[1]}, Registered Users: {row[2]}")

if __name__ == '__main__':
    main()
