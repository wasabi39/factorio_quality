"""
Streamlit frontend for the Factorio Quality Calculator.
Streamlit is a Python library that makes it easy to create web apps 
for machine learning, data science, etc.
"""

import streamlit as st
from frontend.computation_request import ComputationRequest
from backend.backend import run_simulation

#Sets the page title and icon (in the <head>).
st.set_page_config(page_title="Factorio Quality Calculator", page_icon="🚀")

#Creates a <h1> title (in the <body>).
st.title("Factorio Quality Calculator")

#Input widgets
st.header("Make a Calculation")
productivity_boost_from_research = st.number_input(
    "Enter your productivity boost from research as a percentage (e.g. 10 for 10%):", 
    value=0, 
    min_value=0, 
    max_value=300,
    step=10) / 100 #Step=10 adjust how much the increment/decrease buttons change the value.
machine_type = st.selectbox(
    "Choose a machine type:", 
    ["Electromagnetic plant", "Other (e.g. Assembling machine 3)"])

quality_of_production_modules = st.selectbox(
    "Choose a quality of production modules:", 
    ["Normal", "Uncommon", "Rare", "Epic", "Legendary"])
number_of_productivity_modules = st.number_input(
    "Enter the number of productivity modules:", 
    value=0, 
    min_value=0, 
    max_value=8) #Max value is 8, because that's the maximum number of module slots.

quality_of_quality_modules = st.selectbox(
    "Choose a quality of quality modules:", 
    ["Normal", "Uncommon", "Rare", "Epic", "Legendary"])
number_of_quality_modules = st.number_input(
    "Enter the number of quality modules:",
    value=0, 
    min_value=0, 
    max_value=8) #Max value is 8, because that's the maximum number of module slots.

st.header("Simulation Settings")

number_of_iterations = st.number_input("Enter the number of iterations:", 
                                       value=1,
                                       min_value=1,
                                       max_value=1000)

quality_1_count = st.number_input("Enter the count of normal quality items you start out with:", 
                                  value=1,
                                  min_value=0,
                                  max_value=1000000)
quality_2_count = st.number_input("Enter the count of uncommon quality items you start out with:", 
                                  value=0,
                                  min_value=0,
                                  max_value=1000000)
quality_3_count = st.number_input("Enter the count of rare quality items you start out with:", 
                                  value=0,
                                  min_value=0,
                                  max_value=1000000)
quality_4_count = st.number_input("Enter the count of epic quality items you start out with:", 
                                  value=0,
                                  min_value=0,
                                  max_value=1000000)


result = None
if st.button("Calculate"):
    computation_request = ComputationRequest(
        productivity_boost_from_research=productivity_boost_from_research,
        machine_type=machine_type,
        quality_of_production_modules=quality_of_production_modules,
        number_of_productivity_modules=number_of_productivity_modules,
        quality_of_quality_modules=quality_of_quality_modules,
        number_of_quality_modules=number_of_quality_modules,
        number_of_iterations=number_of_iterations,
        quality_1_count=quality_1_count,
        quality_2_count=quality_2_count,
        quality_3_count=quality_3_count,
        quality_4_count=quality_4_count)
        
    result_request = run_simulation(computation_request)
    st.success("Simulation completed.")
    st.success(f"After {number_of_iterations} iterations you can expect:")
    st.success(f"{result_request.quality_1_count} normal quality items.")
    st.success(f"{result_request.quality_2_count} uncommon quality items.")
    st.success(f"{result_request.quality_3_count} rare quality items.")
    st.success(f"{result_request.quality_4_count} epic quality items.")
    st.success(f"{result_request.quality_5_count} legendary quality items.")

#Sidebar for extra functionality
st.sidebar.header("Extra Tools")
st.sidebar.write("WIP.")
