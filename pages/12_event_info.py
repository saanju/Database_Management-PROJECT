import mysql.connector
import streamlit as st
import pandas as pd

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='dbms',
    password='dbms',
    database='dbms'
)
c = db.cursor()

# Streamlit UI
st.title("Event Information")

# Add an option to filter by user or view complete information
filter_by_user = st.checkbox("Filter by User")
user_id = None

# If the user chooses to filter by user, ask for user_id
if filter_by_user:
    user_id = st.number_input('Enter User ID', value=0)

if st.button("Get Event Information"):
    if filter_by_user and user_id:
        # Filter events by user
        query = f'''
        SELECT
            ae.event_id,
            ae.event_title,
            ae.num_days,
            ae.event_price,
            ae.prize_amount,
            ae.start_date,
            ae.end_date,
            ae.event_description,
            ae.slots_left,
            c.name,
            v.name AS venue_name,
            v.location AS venue_location,
            v.capacity AS venue_capacity,
            s.name AS sponsor_name,
            s.contact AS sponsor_contact,
            s.description AS sponsor_description,
            s.sponsorship_amount,
            p.name AS parking_name,
            p.location AS parking_location,
            p.capacity AS parking_capacity,
            p.student_access AS parking_student_access,
            p.teacher_access AS parking_teacher_access,
            p.guest_access AS parking_guest_access
        FROM add_events AS ae
        INNER JOIN club_event AS ce ON ae.event_id = ce.event_id
        INNER JOIN clubs AS c ON ce.club_id = c.club_id
        INNER JOIN venue_booking AS vb ON ae.event_id = vb.event_id
        INNER JOIN venues AS v ON vb.venue_id = v.venue_id
        INNER JOIN event_sponsors AS es ON ae.event_id = es.event_id
        INNER JOIN sponsors AS s ON es.sponsor_id = s.sponsor_id
        INNER JOIN parking AS p ON ae.event_id = p.event_id
        INNER JOIN registration AS r ON ae.event_id = r.event_id
        WHERE r.user_id = {user_id}
        '''
    else:
        # View complete event information without filtering
        query = f'''
        SELECT
            ae.event_id,
            ae.event_title,
            ae.num_days,
            ae.event_price,
            ae.prize_amount,
            ae.start_date,
            ae.end_date,
            ae.event_description,
            ae.slots_left,
            c.name,
            v.name AS venue_name,
            v.location AS venue_location,
            v.capacity AS venue_capacity,
            s.name AS sponsor_name,
            s.contact AS sponsor_contact,
            s.description AS sponsor_description,
            s.sponsorship_amount,
            p.name AS parking_name,
            p.location AS parking_location,
            p.capacity AS parking_capacity,
            p.student_access AS parking_student_access,
            p.teacher_access AS parking_teacher_access,
            p.guest_access AS parking_guest_access
        FROM add_events AS ae
        INNER JOIN club_event AS ce ON ae.event_id = ce.event_id
        INNER JOIN clubs AS c ON ce.club_id = c.club_id
        INNER JOIN venue_booking AS vb ON ae.event_id = vb.event_id
        INNER JOIN venues AS v ON vb.venue_id = v.venue_id
        INNER JOIN event_sponsors AS es ON ae.event_id = es.event_id
        INNER JOIN sponsors AS s ON es.sponsor_id = s.sponsor_id
        INNER JOIN parking AS p ON ae.event_id = p.event_id
        '''

    c.execute(query)
    event_data = c.fetchall()

    if event_data:
        if filter_by_user and user_id:
            st.write(f"Event Information for User ID: {user_id}")
        else:
            st.write("Complete Event Information")
        df = pd.DataFrame(event_data, columns=[
            "event_id", "event_title", "num_days", "event_price", "prize_amount",
            "start_date", "end_date", "event_description", "slots_left", "club_name",
            "venue_name", "venue_location", "venue_capacity", "sponsor_name",
            "sponsor_contact", "sponsor_description", "sponsorship_amount", "parking_name",
            "parking_location", "parking_capacity", "parking_student_access",
            "parking_teacher_access", "parking_guest_access"
        ])
        st.dataframe(df)
    else:
        st.warning("No events found.")
        
# Close the database connection
db.close()
