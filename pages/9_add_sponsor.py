import mysql.connector
import streamlit as st
import pandas as pd
from mysql.connector.errors import IntegrityError

def create_table():
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS `dbms`.`sponsors`(
            `sponsor_id` INT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(128) NOT NULL,
            `contact` VARCHAR(128) NOT NULL,
            `description` TEXT,
            `sponsorship_amount` DECIMAL(10, 2) NOT NULL,
            PRIMARY KEY (sponsor_id)
        ) ENGINE = InnoDB;"""
    )

def add_data(values):
    c.execute('INSERT INTO sponsors(name, contact, description, sponsorship_amount) VALUES(%s, %s, %s, %s)', values)
    db.commit()

def view():
    c.execute('SELECT * FROM sponsors')
    return c.fetchall()

def delete_record(sponsor_id):
    c.execute('DELETE FROM sponsors WHERE sponsor_id = %s', (sponsor_id,))
    db.commit()

def update(sponsor_id, attribute, new_value):
    c.execute(f'UPDATE sponsors SET `{attribute}` = %s WHERE sponsor_id = %s', (new_value, sponsor_id))
    db.commit()

def create():
    name = st.text_input('Sponsor Name: ')
    contact = st.text_input('Contact Information: ')
    description = st.text_area('Description: ')
    sponsorship_amount = st.number_input('Sponsorship Amount: ')
    
    if st.button("Add Sponsor"):
        try:
            add_data((name, contact, description, sponsorship_amount))
        except Exception as e:
            if isinstance(e, IntegrityError):
                st.error(f"ERROR: {e}")
            else:
                raise e
        else:
            st.success("Successfully added sponsor!")

def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns=["sponsor_id", "name", "contact", "description", "sponsorship_amount"]))
    sponsor_ids = [i[0] for i in data]
    sponsor_id_choice = st.selectbox('Select sponsor to delete', sponsor_ids)
    if st.button('Delete Sponsor'):
        delete_record(sponsor_id_choice)
        st.experimental_rerun()

def update_sponsor():
    data = view()
    st.dataframe(pd.DataFrame(data, columns=["sponsor_id", "name", "contact", "description", "sponsorship_amount"]))
    sponsor_ids = [i[0] for i in data]
    sponsor_id_choice = st.selectbox('Select sponsor to update', sponsor_ids)
    selected_sponsor = next((item for item in data if item[0] == sponsor_id_choice), None)
    
    if selected_sponsor:
        st.subheader(f'Update Sponsor (Sponsor ID: {sponsor_id_choice})')
        st.write("Current Details:")
        st.write(f"Name: {selected_sponsor[1]}")
        st.write(f"Contact: {selected_sponsor[2]}")
        st.write(f"Description: {selected_sponsor[3]}")
        st.write(f"Sponsorship Amount: {selected_sponsor[4]}")
        
        attribute = st.selectbox('Select attribute to update', ["name", "contact", "description", "sponsorship_amount"])
        new_value = st.text_input(f"Enter a new value for {attribute}", value=selected_sponsor[1 + ["name", "contact", "description", "sponsorship_amount"].index(attribute)])
        
        if st.button("Update"):
            try:
                update(sponsor_id_choice, attribute, new_value)
                st.success("Sponsor details updated!")
            except Exception as e:
                raise e

def main():
    st.title("Sponsor Management")
    menu = ["Add Sponsor", "View Sponsors", "Update Sponsor", "Remove Sponsor"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()
    if choice == 'Add Sponsor':
        st.subheader("Enter Sponsor Details")
        create()
    elif choice == 'View Sponsors':
        st.subheader("Sponsor Information")
        data = view()
        df = pd.DataFrame(data, columns=["sponsor_id", "name", "contact", "description", "sponsorship_amount"])
        st.dataframe(df)
    elif choice == 'Update Sponsor':
        st.subheader("Select Sponsor to Update")
        update_sponsor()
    elif choice == 'Remove Sponsor':
        st.subheader('Select Sponsor to Remove')
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
