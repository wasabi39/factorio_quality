import streamlit as st

#Title of the app
st.title("Interactive Web App")

#Input widgets
st.header("Make a Calculation")
number = st.number_input("Enter a number:", value=0)
operation = st.selectbox("Choose an operation:", ["Square", "Double", "Cube"])

#Perform calculation
result = None
if st.button("Calculate"):
    if operation == "Square":
        result = number ** 2
    elif operation == "Double":
        result = number * 2
    elif operation == "Cube":
        result = number ** 3

    st.success(f"The result of {operation.lower()} is: {result}")

#Sidebar for extra functionality
st.sidebar.header("Extra Tools")
st.sidebar.write("Add anything here, like links or extra features.")
