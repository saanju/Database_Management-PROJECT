import mysql.connector
import streamlit as st
import pandas as pd
from mysql.connector.errors import IntegrityError

def create_table():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS `dbms`.`club_event` (
            `club_id` INT NOT NULL,
            `event_id` INT NOT NULL,
            FOREIGN KEY (club_id) REFERENCES clubs(club_id) on delete cascade on update cascade,
            FOREIGN KEY (event_id) REFERENCES add_events(event_id) on delete cascade on update cascade,
            PRIMARY KEY (club_id, event_id)
        ) ENGINE = InnoDB;"""
    )

def add_data(values):
    c.execute('INSERT INTO club_event(club_id, event_id) VALUES(%s, %s)', values)
    db.commit()

def view():
    c.execute('SELECT clubs.club_id, clubs.name AS club_name, add_events.event_id, add_events.event_title FROM club_event JOIN clubs ON club_event.club_id = clubs.club_id JOIN add_events ON club_event.event_id = add_events.event_id;')
    return c.fetchall()

def delete_record(club_id, event_id):
    c.execute(f'DELETE FROM club_event WHERE club_id = %s AND event_id = %s', (club_id, event_id))
    db.commit()
def view_events():
    c.execute('SELECT * FROM add_events')
    return c.fetchall()
def get_club_event(club_id, event_id):
    c.execute('SELECT * FROM club_event WHERE club_id = %s AND event_id = %s', (club_id, event_id))
    return c.fetchall()

def create():
    club_id_choice = st.number_input('Enter club id', value=0)
    event_id_choice = st.number_input('Enter event id', value=0)
    if st.button("Add Club-Event Connection"):
        try:
            add_data((club_id_choice, event_id_choice))
        except Exception as e:
            if isinstance(e, IntegrityError):
                st.error(f"ERROR: {e}")
            else:
                raise e
        else:
            st.success("Successfully added club-event connection!")

def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns=["club_id", "club_name", "event_id", "event_title"]))
    pairs = [(i[0], i[2]) for i in data]
    selected_pair = st.selectbox('Select club-event connection to delete', pairs)
    club_id_choice, event_id_choice = selected_pair
    if st.button('Delete Club-Event Connection'):
        delete_record(club_id_choice, event_id_choice)
        st.experimental_rerun()

def main():
    st.title("Manage Club-Event Connections")

    menu = ["Add", "View", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()
    if choice == 'Add':
        st.subheader("View Events")
        event_data = view_events()
        event_df = pd.DataFrame(event_data, columns=["event_id", "event_title", "num_days","event_price", "prize_amount","start_date", "end_date", "event_description", "slots_left"])
        st.dataframe(event_df)
        st.subheader("Add Club-Event Connection")
        create()
    elif choice == 'View':
        st.subheader('View Club-Event Connections')
        data = view()
        df = pd.DataFrame(data, columns=["club_id", "club_name", "event_id", "event_title"])
        st.dataframe(df)
    elif choice == 'Delete':
        st.subheader('Delete Club-Event Connection')
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
