import streamlit as st
import PyPDF2

# Dummy login details
users = {
    'teacher': {'simran': 'simran'},
    'students': {'karthik': 'karthik', 'nitin': 'nitin', 'vinu': 'vinu'}
}

# Session state to keep track of user login
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 0
if 'pdf_file' not in st.session_state:
    st.session_state['pdf_file'] = None
if 'total_pages' not in st.session_state:
    st.session_state['total_pages'] = 0

# Login Function
def login():
    st.title("Login")
    user_type = st.radio("Login as:", ["Teacher", "Student"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if user_type == "Teacher" and username in users['teacher'] and users['teacher'][username] == password:
            st.session_state['user_type'] = "teacher"
            st.session_state['username'] = username
            st.success(f"Welcome Teacher {username}")
        elif user_type == "Student" and username in users['students'] and users['students'][username] == password:
            st.session_state['user_type'] = "student"
            st.session_state['username'] = username
            st.success(f"Welcome Student {username}")
        else:
            st.error("Invalid login credentials")

# Teacher Dashboard
def teacher_dashboard():
    st.title("Teacher Dashboard")

    # Upload PDF
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file is not None:
        st.session_state['pdf_file'] = uploaded_file
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        st.session_state['total_pages'] = pdf_reader.numPages
    
    if st.session_state['pdf_file']:
        st.write(f"Total Pages: {st.session_state['total_pages']}")
        current_page = st.number_input("Page", min_value=0, max_value=st.session_state['total_pages'] - 1, step=1, value=st.session_state['current_page'])
        st.session_state['current_page'] = current_page
        
        # Display PDF page
        if st.button("Show Page"):
            st.write(f"Showing Page {current_page + 1}")
            # Render the current page of the PDF
            st.pdf_display(st.session_state['pdf_file'].read(), page=current_page)

    # Display connected students
    st.write("Connected Students:")
    for student in users['students']:
        st.write(f"Student: {student}")

# Student Dashboard
def student_dashboard():
    st.title("Student Dashboard")
    
    if st.session_state['pdf_file']:
        st.write(f"Viewing page {st.session_state['current_page'] + 1}")
        st.pdf_display(st.session_state['pdf_file'].read(), page=st.session_state['current_page'])
    else:
        st.warning("Waiting for the teacher to upload a PDF.")

# Main function
def main():
    if st.session_state['user_type'] is None:
        login()
    else:
        if st.session_state['user_type'] == "teacher":
            teacher_dashboard()
        elif st.session_state['user_type'] == "student":
            student_dashboard()

if __name__ == "__main__":
    main()
