import mysql.connector
import streamlit as st
from mysql.connector.errors import IntegrityError
import pandas as pd

def create_table():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS `dbms`.`venue_booking`(
            `event_id` INT NOT NULL,
            `venue_id` INT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES add_events(event_id) on delete cascade on update cascade,
            FOREIGN KEY (venue_id) REFERENCES venues(venue_id) on delete cascade on update cascade,
            PRIMARY KEY (event_id, venue_id)
        ) ENGINE = InnoDB;"""
    )

def add_data(values):
    c.execute('INSERT INTO venue_booking(event_id, venue_id) VALUES(%s, %s)', values)
    db.commit()

def view():
    c.execute('select * from venue_booking')
    return c.fetchall()

def delete_record(event_id, venue_id):
    c.execute(f'delete from venue_booking where event_id = %s and venue_id = %s', (event_id, venue_id))
    db.commit()
def view_events():
    c.execute('SELECT * FROM add_events')
    return c.fetchall()
def create():
    event_id_choice = st.number_input('Enter event id', value=0)
    venue_id_choice = st.number_input('Enter venue id', value=0)
    if st.button("Book Venue"):
        try:
            add_data((event_id_choice, venue_id_choice))
        except Exception as e:
            if isinstance(e, IntegrityError):
                st.error(f"ERROR: {e}")
            else:
                raise e
        else:
            st.success("Successfully booked venue!")

def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns=["event_id", "venue_id"]))
    event_ids = []
    venue_ids = []

    for i in data:
        if (event_id := i[0]) not in event_ids:
            event_ids.append(event_id)

        if (venue_id := i[1]) not in venue_ids:
            venue_ids.append(venue_id)

    event_id_choice = st.selectbox('Select event to delete', event_ids)
    venue_id_choice = st.selectbox('Select venue to delete', venue_ids)
    if st.button('Delete Booking'):
        delete_record(event_id_choice, venue_id_choice)
        st.experimental_rerun()

def main():
    st.title("Venue Booking")
    menu = ["Book", "View", "Remove"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()
    if choice == 'Book':
        
        st.subheader("Book a Venue")
        event_data = view_events()
        event_df = pd.DataFrame(event_data, columns=["event_id", "event_title", "num_days","event_price", "prize_amount","start_date", "end_date", "event_description", "slots_left"])
        st.dataframe(event_df)
        try:
            create()
        except Exception as e:
            raise e
    elif choice == 'View':
        st.subheader("Information in Table")
        try:
            data = view()
        except Exception as e:
            raise e
        df = pd.DataFrame(data, columns=["event_id", "venue_id"])
        st.dataframe(df)
    elif choice == 'Remove':
        st.subheader('Select booking to delete')
        delete()

if __name__ == '__main__':
    db = mysql.connector.connect(
        host='localhost',
        user='dbms',
        password='dbms',
        database='dbms'
    )
    c = db.cursor()

main()
