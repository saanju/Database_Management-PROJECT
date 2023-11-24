import mysql.connector
import streamlit as st
import pandas as pd

def create_table():
    c.execute(f"""CREATE TABLE IF NOT EXISTS `dbms`.`clubs`(
    `club_id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(128) NOT NULL,
    `club_head` VARCHAR(128) NOT NULL,
    `contact` VARCHAR(128) NOT NULL,
    `description` VARCHAR(255),
    PRIMARY KEY(`club_id`)
    ) ENGINE = InnoDB;""")

def add_club(values):
    c.execute('INSERT INTO clubs(name, club_head, contact, description) VALUES(%s, %s, %s, %s)', values)
    db.commit()

def view_clubs():
    c.execute('SELECT * FROM clubs')
    return c.fetchall()

def delete_club(club_id):
    c.execute(f'DELETE FROM clubs WHERE club_id = %s', (club_id, ))
    db.commit()

def update_club(club_id, attr_choice, updated_attri):
    c.execute(f'UPDATE clubs SET `{attr_choice}` = %s WHERE club_id = %s', (updated_attri, club_id))
    db.commit()

def get_club(club_id):
    c.execute(f'SELECT * FROM clubs WHERE club_id = %s', (club_id,))
    return c.fetchall()

def create_club():
    name = st.text_input("Club Name:")
    club_head = st.text_input("Club Head:")
    contact = st.text_input("Contact:")
    description = st.text_input("Description (optional):")
    
    if st.button("Add Club"):
        add_club((name, club_head, contact, description))
        st.success("Successfully added club!")

def delete_club_view():
    data = view_clubs()
    st.dataframe(pd.DataFrame(data, columns=["club_id", "name", "club_head", "contact", "description"]))
    club_ids = [i[0] for i in data]
    club_id_choice = st.selectbox('Select club to delete', club_ids)
    if st.button('Delete Club'):
        delete_club(club_id_choice)
        st.experimental_rerun()

def edit_club_view():
    data = view_clubs()
    st.dataframe(pd.DataFrame(data, columns=["club_id", "name", "club_head", "contact", "description"]))
    club_ids = [i[0] for i in data]
    club_id_choice = st.selectbox('Select club to edit', club_ids)
    data = get_club(club_id_choice)
    if data:
        attri = ["club_id", "name", "club_head", "contact", "description"]
        attri_choice = st.selectbox('Select attribute to update', attri)
        updated_attri = st.text_input(f"Enter a new value for {attri_choice}")
        if updated_attri == '':
            updated_attri = data[0][attri.index(attri_choice)]
        if st.button("Update"):
            update_club(club_id_choice, attri_choice, updated_attri)
            st.success("Updated!")

def view_club_data():
    data = view_clubs()
    st.subheader("Club Information")
    st.dataframe(pd.DataFrame(data, columns=["club_id", "name", "club_head", "contact", "description"]))

def main():
    st.title("Club Management")
    menu = ["Add Club", "Edit Club", "Remove Club", "View Clubs"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()

    if choice == 'Add Club':
        st.subheader("Enter club details")
        try:
            create_club()
        except Exception as e:
            raise e
    elif choice == 'Edit Club':
        st.subheader("Club Information")
        try:
            edit_club_view()
        except Exception as e:
            raise e
    elif choice == 'Remove Club':
        st.subheader("Club Information")
        try:
            delete_club_view()
        except Exception as e:
            raise e
    elif choice == 'View Clubs':
        st.subheader("View Club Information")
        try:
            view_club_data()
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
