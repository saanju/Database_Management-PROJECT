import mysql.connector
import streamlit as st
import pandas as pd
from mysql.connector.errors import IntegrityError

def create_table():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS `dbms`.`registration`(
            `event_id` INT NOT NULL,
            `user_id` INT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES add_events(event_id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (event_id, user_id)
        ) ENGINE = InnoDB;"""
    )

def add_data(values):
    c.execute('INSERT INTO registration(event_id, user_id) VALUES(%s, %s)', values)
    db.commit()

def view():
    c.execute('SELECT * FROM registration')
    return c.fetchall()

def delete_record(event_id, user_id):
    c.execute('DELETE FROM registration WHERE event_id = %s AND user_id = %s', (event_id, user_id))
    db.commit()

def get_user(event_id, user_id):
    c.execute('SELECT * FROM registration WHERE event_id = %s AND user_id = %s', (event_id, user_id))
    return c.fetchall()

def create():
    event_id_choice = st.number_input('Enter event id', value=0)
    user_id_choice = st.number_input('Enter user id', value=0)
    if st.button("Add User"):
        try:
            add_data((event_id_choice, user_id_choice))
        except Exception as e:
            if isinstance(e, IntegrityError):
                st.error(f"ERROR: {e}")
            else:
                raise e
        else:
            st.success("Successfully added record!")

def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns=["event_id", "user_id"]))
    event_ids = []
    user_ids = []

    for i in data:
        if (event_id := i[0]) not in event_ids:
            event_ids.append(event_id)

        if (user_id := i[1]) not in user_ids:
            user_ids.append(user_id)

    event_id_choice = st.selectbox('Select event to delete', event_ids)
    user_id_choice = st.selectbox('Select user to delete', user_ids)
    if st.button('Delete Record'):
        delete_record(event_id_choice, user_id_choice)
        st.experimental_rerun()

def viewList():
    c.execute('SELECT event_id, GROUP_CONCAT(CONCAT(users.user_id, " | ", users.first_name)) FROM registration JOIN users ON users.user_id=registration.user_id GROUP BY event_id;')
    return c.fetchall()

def view_events():
    c.execute('SELECT * FROM add_events')
    return c.fetchall()

def main():
    st.title("Event Registration")
    menu = ["Register for Event", "View Registrations", "Delete Registration"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()

    if choice == 'Register for Event':
        st.subheader("View and Register for Events")
        try:
            data=view_events()
        except Exception as e:
            raise e
        df = pd.DataFrame(data, columns=["event_id", "event_title", "num_days","event_price", "prize_amount","start_date", "end_date", "event_description", "slots_left"])
        st.dataframe(df)

        event_id_choice = st.number_input('Enter event id to register', value=0)
        user_id_choice = st.number_input('Enter user id', value=0)
        if st.button("Register for Event"):
            try:
                add_data((event_id_choice, user_id_choice))
                st.success("Successfully registered for the event!")
            except Exception as e:
                if isinstance(e, IntegrityError):
                    st.error(f"ERROR: {e}")
                else:
                    raise e

    elif choice == 'View Registrations':
        st.subheader("Registration Information")
        try:
            data = viewList()
        except Exception as e:
            raise e
        df = pd.DataFrame(data, columns=["event_id", "user_id"])
        st.dataframe(df)

    elif choice == 'Delete Registration':
        st.subheader("Delete Registration")
        try:
            delete()
        except Exception as e:
            raise e

if __name__ == '__main__':
    db = mysql.connector.connect(
        host='localhost',
        user='dbms',
        password='dbms',
        database='dbms'
    )
    c = db.cursor()

main()
