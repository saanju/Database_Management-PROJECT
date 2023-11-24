import mysql.connector
import streamlit as st
from mysql.connector.errors import IntegrityError
import pandas as pd

def create_table():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS `dbms`.`event_sponsors`(
            `event_id` INT NOT NULL,
            `sponsor_id` INT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES add_events(event_id) on delete cascade on update cascade,
            FOREIGN KEY (sponsor_id) REFERENCES sponsors(sponsor_id) on delete cascade on update cascade,
            PRIMARY KEY (event_id, sponsor_id)
        ) ENGINE = InnoDB;"""
    )

def add_data(values):
    c.execute('INSERT INTO event_sponsors(event_id, sponsor_id) VALUES(%s, %s)', values)
    db.commit()

def view():
    c.execute('select * from event_sponsors')
    return c.fetchall()
def view_events():
    c.execute('SELECT * FROM add_events')
    return c.fetchall()

def delete_record(event_id, sponsor_id):
    c.execute(f'delete from event_sponsors where event_id = %s and sponsor_id = %s', (event_id, sponsor_id))
    db.commit()

def create():
    event_id_choice = st.number_input('Enter event id', value=0)
    sponsor_id_choice = st.number_input('Enter sponsor id', value=0)
    if st.button("Add Sponsor"):
        try:
            add_data((event_id_choice, sponsor_id_choice))
        except Exception as e:
            if isinstance(e, IntegrityError):
                st.error(f"ERROR: {e}")
            else:
                raise e
        else:
            st.success("Successfully added sponsor!")

def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns=["event_id", "sponsor_id"]))
    event_ids = []
    sponsor_ids = []

    for i in data:
        if (event_id := i[0]) not in event_ids:
            event_ids.append(event_id)

        if (sponsor_id := i[1]) not in sponsor_ids:
            sponsor_ids.append(sponsor_id)

    event_id_choice = st.selectbox('Select event to remove sponsorship', event_ids)
    sponsor_id_choice = st.selectbox('Select sponsor to remove sponsorship', sponsor_ids)
    if st.button('Remove Sponsorship'):
        delete_record(event_id_choice, sponsor_id_choice)
        st.experimental_rerun()

def main():
    st.title("Sponsorship Management")
    menu = ["Add", "View", "Remove"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()
    if choice == 'Add':
        event_data = view_events()
        event_df = pd.DataFrame(event_data, columns=["event_id", "event_title", "num_days","event_price", "prize_amount","start_date", "end_date", "event_description", "slots_left"])
        st.dataframe(event_df)
        st.subheader("Enter details")
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
        df = pd.DataFrame(data, columns=["event_id", "sponsor_id"])
        st.dataframe(df)
    elif choice == 'Remove':
        st.subheader('Select sponsorship to remove')
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
