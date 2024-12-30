import streamlit as st

#Title of the app
st.title("Factorio Quality Calculator")

#Input widgets
st.header("Make a Calculation")
productivity_boost_from_research = st.number_input("Enter your productivity boost from research, as a percentage (e.g. 10 for 10%):", value=0)
machine_type = st.selectbox("Choose a machine type:", ["Electromagnetic plant", "Other (e.g. Assembling machine 3)"])

quality_of_production_modules = st.selectbox("Choose a quality of production modules:", ["Normal", "Uncommon", "Rare", "Epic", "Legendary"])
number_of_productivity_modules = st.number_input("Enter your number of productivity module 3s:", value=0)

quality_of_quality_modules = st.selectbox("Choose a quality of quality modules:", ["Normal", "Uncommon", "Rare", "Epic", "Legendary"])
number_of_quality_modules = st.number_input("Enter your number of quality module 3s:", value=0)

number_of_iterations = st.number_input("Enter your number of quality module 3s:", value=1)

#TODO Perform calculation
result = None
if st.button("Calculate"):
    if quality_of_quality_modules == "Square":
        result = 2 ** 2
    elif quality_of_quality_modules == "Double":
        result = 2 * 2
    elif quality_of_quality_modules == "Cube":
        result = 2 ** 3

    st.success(f"The result of {quality_of_quality_modules.lower()} is: {result}")

#Sidebar for extra functionality
st.sidebar.header("Extra Tools")
st.sidebar.write("WIP.")
