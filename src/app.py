
import os
import streamlit as st
from dotenv import load_dotenv
from llm import call_groq_llm
from db import connect_to_database, execute_query, close_connection

load_dotenv()

st.set_page_config(page_title="Convert prompt to SQL query", page_icon=":books:")

# Database setup
DB_NAME = "students.db"
conn = connect_to_database(DB_NAME)

st.title("SQL Query Generator from Natural Language")

st.sidebar.header("Database Operations")

# --- Table Creation ---
with st.sidebar.expander("Create New Table (Natural Language)", expanded=False):
    nl_create_table = st.text_input(
        "Describe the table you want to create (e.g. 'Create a table for teachers with id, name, and subject')",
        key="nl_create_table"
    )
    if st.button("Create Table (NL)", key="create_table_nl_btn"):
        if nl_create_table:
            create_table_sql = call_groq_llm(nl_create_table)
            st.write("Generated SQL:")
            st.code(create_table_sql, language='sql')
            result = execute_query(conn, create_table_sql)
            if result is not None:
                st.success("Table created (or already exists).")
            else:
                st.error("Failed to create table. Check your description or try again.")
        else:
            st.warning("Please describe the table you want to create.")

# --- Add Entry to Table ---
with st.sidebar.expander("Add Entry (Natural Language)", expanded=False):
    nl_add_entry = st.text_input(
        "Describe the entry you want to add (e.g. 'Add a student named John, age 20, grade 3')",
        key="nl_add_entry"
    )
    if st.button("Add Entry (NL)", key="add_entry_nl_btn"):
        if nl_add_entry:
            insert_sql = call_groq_llm(nl_add_entry)
            st.write("Generated SQL:")
            st.code(insert_sql, language='sql')
            result = execute_query(conn, insert_sql)
            if result is not None:
                st.success("Entry added.")
            else:
                st.error("Failed to add entry. Check your description or try again.")
        else:
            st.warning("Please describe the entry you want to add.")

# --- Alter Table ---
with st.sidebar.expander("Alter Table (Natural Language)", expanded=False):
    nl_alter_table = st.text_input(
        "Describe how you want to alter the table (e.g. 'Add a column email to students table')",
        key="nl_alter_table"
    )
    if st.button("Alter Table (NL)", key="alter_table_nl_btn"):
        if nl_alter_table:
            alter_sql = call_groq_llm(nl_alter_table)
            st.write("Generated SQL:")
            st.code(alter_sql, language='sql')
            result = execute_query(conn, alter_sql)
            if result is not None:
                st.success("Table altered.")
            else:
                st.error("Failed to alter table. Check your description or try again.")
        else:
            st.warning("Please describe how you want to alter the table.")

# --- Main App: Table Management and Prompt to SQL ---
st.header("Database Table Management")

# Show all tables in the database
show_tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = execute_query(conn, show_tables_query)
table_names = [row[0] for row in tables] if tables else []

if table_names:
    selected_table = st.selectbox("Select a table to view its contents:", table_names)
    if selected_table:
        st.subheader(f"Contents of table: {selected_table}")
        table_data = execute_query(conn, f"SELECT * FROM {selected_table};")
        if table_data:
            # Get column names
            import sqlite3
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({selected_table});")
            columns = [info[1] for info in cursor.fetchall()]
            cursor.close()
            st.dataframe([dict(zip(columns, row)) for row in table_data])
        else:
            st.info("Table is empty.")
else:
    st.info("No tables found in the database.")

st.header("Ask in Simple Language (Table Management)")
nl_command = st.text_input("Describe what you want to do (e.g. 'Show all students older than 20', 'Delete all entries from teachers', 'Add a new student named Alice, age 22, grade 3'):")
run_nl_command = st.button("Run Command")

if run_nl_command:
    if nl_command:
        sql_query = call_groq_llm(nl_command)
        if sql_query:
            st.write("Generated SQL Query:")
            st.code(sql_query, language='sql')
            result = execute_query(conn, sql_query)
            if result is not None:
                st.write("Query Results:")
                st.dataframe(result)
            else:
                st.success("Command executed (no results to display).")
        else:
            st.error("Failed to generate SQL query.")
    else:
        st.warning("Please enter a command.")