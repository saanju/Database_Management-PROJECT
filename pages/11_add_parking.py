import mysql.connector
import streamlit as st
import pandas as pd


def create_table():
    c.execute(f"""CREATE TABLE IF NOT EXISTS `dbms`.`parking`(
    `parking_id` INT NOT NULL AUTO_INCREMENT,
    `event_id` INT NOT NULL,
    `name` VARCHAR(128) NOT NULL,
    `location` VARCHAR(128) NOT NULL,
    `capacity` INT NOT NULL,
    `student_access` BOOLEAN,
    `teacher_access` BOOLEAN,
    `guest_access` BOOLEAN,
     PRIMARY KEY(`parking_id`),
     FOREIGN KEY (`event_id`) REFERENCES add_events(`event_id`) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE = InnoDB;""")


def add_parking(values):
    c.execute('INSERT INTO parking(event_id, name, location, capacity, student_access, teacher_access, guest_access) VALUES(%s, %s, %s, %s, %s, %s, %s)', values)
    db.commit()


def view_parking(event_id):
    c.execute('SELECT * FROM parking WHERE event_id = %s', (event_id,))
    return c.fetchall()

def view_events():
    c.execute('SELECT * FROM add_events')
    return c.fetchall()
def delete_parking(parking_id):
    c.execute(f'DELETE FROM parking WHERE parking_id = %s', (parking_id, ))
    db.commit()


def update_parking(parking_id, attr_choice, updated_attri):
    c.execute(f'UPDATE parking SET `{attr_choice}` = %s WHERE parking_id = %s', (updated_attri, parking_id))
    db.commit()


def get_parking(parking_id):
    c.execute(f'SELECT * FROM parking WHERE parking_id = %s', (parking_id,))
    return c.fetchall()


def create_parking():
    event_id_choice = st.number_input('Enter event id', value=0)
    name = st.text_input("Name:")
    location = st.text_input("Location:")
    capacity = st.number_input("Capacity:")
    student_access = st.checkbox("Student Access")
    teacher_access = st.checkbox("Teacher Access")
    guest_access = st.checkbox("Guest Access")

    if st.button("Add Parking"):
        add_parking((event_id_choice, name, location, capacity, student_access, teacher_access, guest_access))
        st.success("Successfully added parking!")


def delete_parking_view(event_id):
    data = view_parking(event_id)
    st.dataframe(pd.DataFrame(data, columns=["parking_id", "event_id", "name", "location", "capacity", "student_access", "teacher_access", "guest_access"]))
    parking_ids = [i[0] for i in data]
    parking_id_choice = st.selectbox('Select parking to delete', parking_ids)
    if st.button('Delete Parking'):
        delete_parking(parking_id_choice)
        st.experimental_rerun()


def edit_parking_view(event_id):
    data = view_parking(event_id)
    st.dataframe(pd.DataFrame(data, columns=["parking_id", "event_id", "name", "location", "capacity", "student_access", "teacher_access", "guest_access"]))
    parking_ids = [i[0] for i in data]
    parking_id_choice = st.selectbox('Select parking to edit', parking_ids)
    data = get_parking(parking_id_choice)
    if data:
        attri = ["parking_id", "event_id", "name", "location", "capacity", "student_access", "teacher_access", "guest_access"]
        attri_choice = st.selectbox('Select attribute to update', attri)
        updated_attri = st.text_input(f"Enter a new value for {attri_choice}")
        if updated_attri == '':
            updated_attri = data[0][attri.index(attri_choice)]
        if st.button("Update"):
            update_parking(parking_id_choice, attri_choice, updated_attri)
            st.success("Updated!")


def view_parking_view(event_id):
    data = view_parking(event_id)
    st.dataframe(pd.DataFrame(data, columns=["parking_id", "event_id", "name", "location", "capacity", "student_access", "teacher_access", "guest_access"]))


def main():
    st.title("Add Parking")
    menu = ["Add Parking", "Edit Parking", "Remove Parking", "View Parking"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()

    if choice == 'Add Parking':
        event_data = view_events()
        event_df = pd.DataFrame(event_data, columns=["event_id", "event_title", "num_days","event_price", "prize_amount","start_date", "end_date", "event_description", "slots_left"])
        st.dataframe(event_df)
        st.subheader("Enter parking details")
        try:
            create_parking()
        except Exception as e:
            raise e
    elif choice == 'Edit Parking':
        st.subheader("Parking Information")
        event_id = st.number_input('Enter event id', value=0)
        try:
            edit_parking_view(event_id)
        except Exception as e:
            raise e
    elif choice == 'Remove Parking':
        st.subheader("Parking Information")
        event_id = st.number_input('Enter event id', value=0)
        try:
            delete_parking_view(event_id)
        except Exception as e:
            raise e
    elif choice == 'View Parking':
        st.subheader("Parking Information")
        event_id = st.number_input('Enter event id', value=0)
        try:
            view_parking_view(event_id)
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
