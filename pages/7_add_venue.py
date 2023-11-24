import mysql.connector
import streamlit as st
import pandas as pd

# Function to create the "venues" table if it doesn't exist
def create_venue_table():
    c.execute(f"""CREATE TABLE IF NOT EXISTS `dbms`.`venues` (
    `venue_id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(128) NOT NULL,
    `location` VARCHAR(128) NOT NULL,
    `capacity` INT NOT NULL,
    PRIMARY KEY(`venue_id`)
) ENGINE = InnoDB;""")

# Function to add venue data to the "venues" table
def add_venue_data(values):
    c.execute('INSERT INTO venues(name, location, capacity) VALUES(%s, %s, %s)', values)
    db.commit()

# Function to view all venues
def view_venues():
    c.execute('SELECT * FROM venues')
    return c.fetchall()

# Function to delete a venue record
def delete_venue(venue_id):
    c.execute('DELETE FROM venues WHERE venue_id = %s', (venue_id, ))
    db.commit()

# Function to update venue details
def update_venue(choice, attrichoice, updated_attri):
    c.execute(f'UPDATE venues SET `{attrichoice}` = %s WHERE venue_id = %s', (updated_attri, choice))
    db.commit()

# Streamlit page for adding venue details
def create_venue():
    st.title("Add Venue")
    name = st.text_input("Venue Name: ")
    location = st.text_input("Venue Location: ")
    capacity = st.number_input("Venue Capacity: ")
    
    if st.button("Add Venue Details"):
        add_venue_data((name, location, capacity))
        st.success("Venue details added successfully!")

# Streamlit page for viewing venue details
def view_venue():
    st.title("View Venues")
    data = view_venues()
    df = pd.DataFrame(data, columns=["venue_id", "name", "location", "capacity"])
    st.dataframe(df)

# Streamlit page for deleting venue details
def delete_venue_page():
    st.title("Delete Venue")
    data = view_venues()
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select venue to delete', user_ids)
    if st.button('Delete Venue'):
        delete_venue(choice)
        st.success("Venue deleted successfully!")

# Streamlit page for editing venue details
def edit_venue():
    st.title("Edit Venue")
    data = view_venues()
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select venue_id', user_ids)
    data = [list(item) for item in data]
    
    if data:
        attri = ["venue_id", "name", "location", "capacity"]
        attrichoice = st.selectbox('Select attribute to update', attri)
        updated_attri = st.text_input(f"Enter a new value for {attrichoice}")
        if updated_attri == '':
            updated_attri = data[user_ids.index(choice)][attri.index(attrichoice)]
        if st.button("Update"):
            update_venue(choice, attrichoice, updated_attri)
            st.success("Venue details updated!")

# Main function for the Streamlit app
def main():
    st.title("Venue Management")
    menu = ["Add Venue", "View Venues", "Edit Venue", "Delete Venue"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_venue_table()

    if choice == 'Add Venue':
        create_venue()
    elif choice == 'View Venues':
        view_venue()
    elif choice == 'Delete Venue':
        delete_venue_page()
    elif choice == 'Edit Venue':
        edit_venue()

if __name__ == '__main__':
    db = mysql.connector.connect(
        host='localhost',
        user='dbms',
        password='dbms',
        database='dbms'
    )
    c = db.cursor()

main()
