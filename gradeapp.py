
import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Grade Manager")
st.write("Enter student details and marks for each subject.")

# Subjects
subjects = ["Tamil", "English", "Maths", "Science", "Social Science"]

# Initialize session state
if "students" not in st.session_state:
    st.session_state.students = []


# Grade calculation based on percentage
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


# Student entry form
st.subheader("Add Student")

with st.form("student_form"):
    name = st.text_input("Student Name")

    st.write("### Enter Subject Marks (Out of 100)")

    col1, col2, col3 = st.columns(3)

    with col1:
        tamil = st.number_input(
            "Tamil", min_value=0, max_value=100, step=1
        )
        english = st.number_input(
            "English", min_value=0, max_value=100, step=1
        )

    with col2:
        maths = st.number_input(
            "Maths", min_value=0, max_value=100, step=1
        )
        science = st.number_input(
            "Science", min_value=0, max_value=100, step=1
        )

    with col3:
        social = st.number_input(
            "Social Science", min_value=0, max_value=100, step=1
        )

    submitted = st.form_submit_button("Add Student")

    if submitted:
        if name.strip() == "":
            st.error("Please enter the student name.")
        else:
            marks = {
                "Tamil": tamil,
                "English": english,
                "Maths": maths,
                "Science": science,
                "Social Science": social
            }

            total = sum(marks.values())
            percentage = total / len(subjects)
            grade = calculate_grade(percentage)

            student = {
                "S.No": len(st.session_state.students) + 1,
                "Name": name.strip(),
                **marks,
                "Total": total,
                "Percentage": round(percentage, 2),
                "Grade": grade
            }

            st.session_state.students.append(student)
            st.success(f"{name.strip()} added successfully!")

# Display student results
st.subheader("Student Results")

if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    st.dataframe(df, use_container_width=True, hide_index=True)

    # Class statistics
    st.subheader("Class Statistics")

    average = df["Total"].mean()
    highest = df["Total"].max()
    lowest = df["Total"].min()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", len(df))
    col2.metric("Average Total", f"{average:.2f} / 500")
    col3.metric("Highest Total", f"{highest} / 500")
    col4.metric("Lowest Total", f"{lowest} / 500")

    # Download results
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="student_results.csv",
        mime="text/csv"
    )

else:
    st.info("No students added yet. Enter the first student's details above.")
