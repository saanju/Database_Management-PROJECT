import mysql.connector
import streamlit as st
import pandas as pd


def create_table():
    c.execute(f"""CREATE TABLE IF NOT EXISTS `dbms`.`add_events`(
    `event_id` INT NOT NULL AUTO_INCREMENT,
    `event_title` VARCHAR(128) NOT NULL,
    `num_days` INT NOT NULL,
    `event_price` INT NOT NULL ,
    `prize_amount` INT NOT NULL default 0,
    `start_date` DATE NOT NULL,
    `end_date` DATE NOT NULL,
    `event_description` VARCHAR(128) NOT NULL,
    `slots_left` INT NOT NULL DEFAULT 3,
     PRIMARY KEY(`event_id`)
) ENGINE = InnoDB;""")

def add_data(values):
    c.execute('INSERT INTO add_events(event_title, num_days,event_price,prize_amount,start_date,end_date,event_description, slots_left) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', values)
    db.commit()


def view():
    c.execute('select * from add_events')
    return c.fetchall()

def delete_record(user_id):
    c.execute(f'delete from add_events where event_id = %s', (user_id, ))
    db.commit()

def update(choice, attrichoice, updated_attri):
    c.execute(f'update add_events SET `{attrichoice}` = "{updated_attri}" where event_id = "{choice}"')
    db.commit()

def get_user(user_id):
    c.execute(f'select * from add_events where event_id = "{user_id}"')
    return c.fetchall()


def create():
    event_title = st.text_input("Event Title: ")
  
    num_days = st.number_input("Number of Days: ", value=0)
    event_price = st.number_input("Event Price: ")
    prize_amount=st.number_input("Event Prize amount: ")
    start_date = st.date_input("Start Date: ")
    end_date = st.date_input("End Date: ")
    event_description=st.text_input("Event Description: ")
    slots_left = st.number_input("Enter number of slots: ", value=3)
    if st.button("Add Event Details"):
        add_data((event_title, num_days,event_price,prize_amount,start_date,end_date,event_description, slots_left))
        st.success("Successfully added record!")


def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["event_id", "event_title", "num_days", "event_price","prize_amount", "start_date", "end_date","event_description","slots_left"]))
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select event to delete', user_ids)
    if st.button('Delete Record'):
        delete_record(choice)
        st.experimental_rerun()


def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ["event_id", "event_title", "num_days", "event_price","prize_amount", "start_date", "end_date","event_description","slots_left"]))
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select event_id', user_ids)
    data = get_user(choice)
    if data:
        attri = ["event_id", "event_title", "num_days", "event_price","prize_amount", "start_date", "end_date","event_description","slots_left"]
        attrichoice = st.selectbox('Select attribute to update', attri)
        updated_attri = st.text_input(f"Enter a new value for {attrichoice}")
        if updated_attri == '':
            updated_attri = data[0][attri.index(attrichoice)]
        if st.button("Update"):
            update(choice, attrichoice, updated_attri)
            st.success("Updated!")


def main():
    st.title("Add Events")
    menu = ["Add", "View", "Edit", "Remove"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()
    if choice == 'Add':
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
        df = pd.DataFrame(data, columns = ["event_id", "event_title", "num_days", "event_price","prize_amount", "start_date", "end_date","event_description","slots_left"])
        st.dataframe(df)
    
    elif choice == 'Remove':
        st.subheader('Select row to delete')
        delete()
    elif choice == 'Edit':
        st.subheader('Select row to update')
        edit()


if __name__ == '__main__':
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'dbms',
        password = 'dbms',
        database = 'dbms'
    )
    c = db.cursor()

main()