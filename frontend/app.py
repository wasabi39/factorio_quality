"""
Streamlit frontend for the Factorio Quality Calculator.
Streamlit is a Python library that makes it easy to create web apps 
for machine learning, data science, etc.
"""

import requests
import streamlit as st
from computation_request import ComputationRequest


def create_computation_request():
    """
    Creates the form asking for user input, returns an object containing
    what the user has currently entered into the form when called.
    """
    # Input widgets
    st.header("Factory Settings")
    productivity_boost_from_research = st.number_input(
        "Enter your productivity boost from research" + 
        " as a percentage (e.g. 10 for 10%):", value=0) / 100
    machine_type = st.selectbox(
        "Choose a machine type:", 
        ["Electromagnetic plant", "Other (e.g. Assembling machine 3)"])

    quality_of_production_modules = st.selectbox(
        "Choose a quality of production modules:", 
        ["Normal", "Uncommon", "Rare", "Epic", "Legendary"])
    number_of_productivity_modules = st.number_input(
        "Enter the number of productivity modules:", value=0)
    
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

    return ComputationRequest(
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
        quality_4_count=quality_4_count
    )

def display_results(result, number_of_iterations):
    """
    Displays the results of the simulation.
    """
    st.success("Simulation completed.")
    if number_of_iterations == 1:
        st.success("After 1 iteration you can expect:")
    else:
        st.success(f"After {number_of_iterations} iterations you can expect:")
    st.success(f"{result['quality_1_count']} normal quality items.")
    st.success(f"{result['quality_2_count']} uncommon quality items.")
    st.success(f"{result['quality_3_count']} rare quality items.")
    st.success(f"{result['quality_4_count']} epic quality items.")
    st.success(f"{result['quality_5_count']} legendary quality items.")
    
def run_simulation():
    """
    Creates the simulation form, sends the simulation API request when the
    user presses the "Run Simulation" button.
    """
    computation_request = create_computation_request()
    if st.button("Run Simulation"):
        try:
            response = requests.post("http://backend:8000/simulate", 
                                     json=computation_request.model_dump(), 
                                     timeout=10)
            if response.status_code == 200:
                result = response.json()
                display_results(result, computation_request.number_of_iterations)
            else:
                st.write("Error: ", response.status_code)
        except requests.exceptions.RequestException as e:
            st.write("An error occurred: ", e)

def main():
    """
    Creates the Streamlit web app.
    """
    #Sets the page title and icon (in the <head>).
    st.set_page_config(page_title="Factorio Quality Calculator", 
                    page_icon="🚀")
    #Creates a <h1> title (in the <body>).
    st.title("Factorio Quality Calculator")
    run_simulation()
    #Sidebar for extra functionality
    st.sidebar.header("About")
    st.sidebar.markdown("This app calculates the expected number of items of each quality " +
                        "level after a certain number of iterations in Factorio.")
    st.sidebar.markdown("One iteration is the act of producing an item, " +
                        "and then recycling it if it's not legendary quality.")
    st.sidebar.markdown("The simulation assumes you're using legendary quality modules 3 " +
                        "in your recycling machines.")
    st.sidebar.markdown("[Source code on Github 😊](https://github.com/wasabi39/factorio_quality)")
        
if __name__ == "__main__":
    main()
    