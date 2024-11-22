
import streamlit as st
from backend import create_user, get_valid_descriptions, calculate_total_cost_by_role, verify_user, get_instructors, create_instructor, update_instructor, delete_instructor,get_managers, create_facility_demand, create_parking_demand, get_facilities, create_facility, update_facility , delete_facility, get_facility_demand, compare_facility_demand_supply, delete_facility_demand, get_available_parking, get_parking_demand, update_parking_availability, delete_parking_demand, create_parking_demand, load_parking_demand, load_available_parking
from backend import get_facilities, get_facility_demand, get_instructors, get_managers, get_management_committee, create_user, delete_user, get_salary_statistics
st.set_page_config(page_title="Facilities Management System")

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None


def switch_page(page_name):
    st.session_state.page = page_name


def login_page():
    st.title("Facilities Management System")
    st.subheader("Login")

    name = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            if name and password:  # Check if fields are not empty
                role = verify_user(name, password)
                if role:
                    st.success(f"Welcome, {name}! You are logged in as a {role}.")
                    st.session_state.role = role
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please fill in all fields")

    with col2:
        if st.button("New User? Create Account"):
            switch_page("create_user")
            st.rerun()
def create_user_page():
    st.title("Facilities Management System")
    st.subheader("Create New User")

    name = st.text_input("Name")
    role = st.selectbox("Role", ["Supervisor", "Activities", "User","Facilities","Security"])
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create User"):
            if name and password and confirm_password:  # Check if fields are not empty
                if password == confirm_password:
                    try:
                        create_user(name, role, password)
                        st.success("User created successfully! Please login.")
                        # Wait 2 seconds then switch to login page
                        st.balloons()
                        st.session_state.page = "login"
                        st.rerun()
                    except Exception as e:
                        if "Duplicate entry" in str(e):
                            st.error("Username already exists. Please choose a different username.")
                        else:
                            st.error(f"An error occurred: {str(e)}")
                else:
                    st.error("Passwords do not match")
            else:
                st.warning("Please fill in all fields")

    with col2:
        if st.button("Back to Login"):
            switch_page("login")
            st.rerun()
def main_page():
    st.title("Facilities Management System")
    st.subheader(f"Role-Based Access for {st.session_state.role}")

    if st.session_state.role == "Supervisor":
        supervisor_page()
    elif st.session_state.role == "Activities":
        st.write("You have access to the instructor table.")

        # Display the instructor table
        st.subheader("Instructor Management")
        instructor_data = get_instructors()
        instructor_df = st.dataframe(instructor_data)

        # Add a new instructor
        st.subheader("Add New Instructor")
        name = st.text_input("Instructor Name")
        description_options = get_valid_descriptions()
        description = st.selectbox("Description", description_options)
        salary = st.number_input("Salary", min_value=0.0, format="%.2f")
        manager_id = st.selectbox("Manager", [row["manager_id"] for row in get_managers()])

        if st.button("Add Instructor"):
            try:
                create_instructor(name, description, salary, manager_id)
                st.success("Instructor added successfully!")
                # Refresh the instructor table
                instructor_data = get_instructors()
                instructor_df.dataframe(instructor_data)
            except Exception as e:
                st.error(f"Error adding instructor: {str(e)}")

        # Update an existing instructor
        st.subheader("Update Instructor")
        instructor_id = st.selectbox("Select Instructor", [row["activity_id"] for row in instructor_data])
        new_name = st.text_input("New Instructor Name")
        new_description_options = get_valid_descriptions()
        new_description = st.selectbox("New Description", new_description_options)
        new_salary = st.number_input("New Salary", min_value=0.0, format="%.2f")
        new_manager_id = st.selectbox("New Manager", [row["manager_id"] for row in get_managers()])

        if st.button("Update Instructor"):
            try:
                update_instructor(instructor_id, new_name, new_description, new_salary, new_manager_id)
                st.success("Instructor updated successfully!")
                # Refresh the instructor table
                instructor_data = get_instructors()
                instructor_df.dataframe(instructor_data)
            except Exception as e:
                st.error(f"Error updating instructor: {str(e)}")

        # Delete an existing instructor
        st.subheader("Delete Instructor")
        instructor_id_to_delete = st.selectbox("Select Instructor to Delete", [row["activity_id"] for row in instructor_data])

        if st.button("Delete Instructor"):
            try:
                delete_instructor(instructor_id_to_delete)
                st.success("Instructor deleted successfully!")
                # Refresh the instructor table
                instructor_data = get_instructors()
                instructor_df.dataframe(instructor_data)
            except Exception as e:
                st.error(f"Error deleting instructor: {str(e)}")
        st.subheader("Calculate Cost to Association")
        if st.button("Calculate Cost"):
            try:
                cost_by_role = calculate_total_cost_by_role()
                st.write("Total Cost by Role:")
                for row in cost_by_role:
                    st.write(f"{row['description']}: ${row['total_cost']:.2f}")
            except Exception as e:
                st.error(f"Error calculating total cost: {str(e)}")
        st.subheader("Instructor Salary Analysis")
        if st.button("View Salary Statistics"):
            try:
                salary_stats = get_salary_statistics()

                # Create columns for the statistics
                st.write("Salary Statistics by Role")

                # Create a formatted table
                for stat in salary_stats:
                    with st.expander(f"{stat['description']} Statistics"):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Number of Instructors", stat['instructor_count'])
                            st.metric("Average Salary", f"${stat['avg_salary']:.2f}")

                        with col2:
                            st.metric("Minimum Salary", f"${stat['min_salary']:.2f}")
                            st.metric("Maximum Salary", f"${stat['max_salary']:.2f}")

                        with col3:
                            st.metric("Total Cost", f"${stat['total_cost']:.2f}")
            except Exception as e:
                st.error(f"Error displaying salary statistics: {str(e)}")
    elif st.session_state.role == "User":
        st.subheader("Facility Demand")
        facility = st.selectbox("Facility", ["Plumber", "Electrician", "Gardener", "Painter"])
        flat_no = st.text_input("Flat Number")

        if st.button("Submit Facility Demand"):
            try:
                create_facility_demand(facility, flat_no)
                st.success("Facility demand submitted successfully!")
            except Exception as e:
                st.error(f"Error submitting facility demand: {str(e)}")

        st.subheader("Parking Demand")
        flat_no_parking = st.text_input("Flat Number",key="flat_no_parking")
        num_vehicles = st.number_input("Number of Vehicles", min_value=1, step=1, format="%d", key="num_vehicles")

        if st.button("Submit Parking Demand"):
            try:
                create_parking_demand(flat_no_parking, num_vehicles)
                st.success("Parking demand submitted successfully!")
            except Exception as e:
                st.error(f"Error submitting parking demand: {str(e)}")
    elif st.session_state.role == "Facilities":
        facilities_page()
    elif st.session_state.role == "Security":
        security_page()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.page = "login"
        st.rerun()


def facilities_page():
    st.title("Facilities Management System")
    st.subheader("Facilities Role - Manage Facility Demand and Availability")

    # Section 1: Facility Demand Management
    st.subheader("Manage Facility Demand")

    # Display existing demands
    demand_data = get_facility_demand()

    # Create two columns - one for the table and one for delete functionality
    col1, col2 = st.columns([3, 1])

    with col1:
        st.write("Facility Demand Table:")
        st.dataframe(demand_data)

    with col2:
        if demand_data:  # Only show delete option if there are demands
            st.write("Delete Demand:")
            # Create unique identifiers for each demand
            demands = [(row['facility'], row['flat_no']) for row in demand_data]

            # Create display strings for the selectbox
            demand_options = [f"Facility: {facility}, Flat: {flat_no}"
                              for facility, flat_no in demands]

            selected_demand = st.selectbox(
                "Select Demand to Delete",
                options=demand_options,
                key="delete_demand_select"
            )

            if st.button("Delete Selected Demand"):
                try:
                    # Parse the selected option
                    facility = selected_demand.split(',')[0].split(':')[1].strip()
                    flat_no = int(selected_demand.split(',')[1].split(':')[1].strip())

                    delete_facility_demand(facility, flat_no)
                    st.success("Facility demand deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting facility demand: {str(e)}")

    # Form to create new facility demand
    st.subheader("Add New Facility Demand")
    facility = st.selectbox("Facility", ["Plumber", "Electrician", "Gardener", "Painter"], key="cr_new_facility_demand")
    flat_no = st.number_input("Flat Number", min_value=1, step=1, format="%d", key="flat_no_demand")

    if st.button("Add Facility Demand"):
        try:
            create_facility_demand(facility, flat_no)
            st.success("Facility demand added successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error adding facility demand: {str(e)}")

    # Section 2: Facilities Available
    st.subheader("Manage Available Facilities")
    facility_data = get_facilities()
    st.write("Facilities Available Table:")
    st.dataframe(facility_data)

    # Form to add new facility
    st.subheader("Add New Facility")
    new_facility_name = st.selectbox("Facility", ["Plumber", "Electrician", "Gardener", "Painter"],
                                     key="add_new_facility_demand")
    availability_status = st.selectbox("Availability Status", ["Available", "Unavailable"])
    manager_id = st.selectbox("Manager", [row["manager_id"] for row in get_managers()])

    if st.button("Add Facility"):
        try:
            create_facility(new_facility_name, availability_status, manager_id)
            st.success("Facility added successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error adding facility: {str(e)}")

    # Section for updating and deleting facilities
    st.subheader("Update or Delete Facilities")
    if facility_data:
        facility_id = st.selectbox("Select Facility", [row["facility_id"] for row in facility_data])

        # Update fields
        update_name = st.selectbox("Facility", ["Plumber", "Electrician", "Gardener", "Painter"])
        update_status = st.selectbox("New Availability Status", ["Available", "Unavailable"], key="update_status")
        update_manager_id = st.selectbox("New Manager", [row["manager_id"] for row in get_managers()],
                                         key="update_manager")

        if st.button("Update Facility"):
            try:
                update_facility(facility_id, update_name, update_status, update_manager_id)
                st.success("Facility updated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error updating facility: {str(e)}")

        if st.button("Delete Facility"):
            try:
                delete_facility(facility_id)
                st.success("Facility deleted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error deleting facility: {str(e)}")

    # Facility Demand vs Availability Analysis
    st.subheader("Facility Demand vs Availability Analysis")

    if st.button("Compare Demand and Availability"):
        results = compare_facility_demand_supply()

        # Create a clean table display
        comparison_data = []
        for facility, data in results.items():
            comparison_data.append({
                "Facility": facility,
                "Demand": data['demand'],
                "Available": data['available'],
                "Status": data['status']
            })

        # Display results in a DataFrame
        st.dataframe(comparison_data)

        # Display detailed analysis with color coding
        for facility, data in results.items():
            if data['status'] == 'Requirements met':
                st.success(f"{facility}: {data['status']} (Excess capacity: {data['difference']})")
            else:
                st.error(f"{facility}: {data['status']}")


import streamlit as st

def security_page():
    st.title("Security Management System")
    st.subheader("Parking Management")

    # Display Available Parking table
    st.subheader("Available Parking Spots")
    parking_data = get_available_parking()
    parking_df = st.dataframe(parking_data)

    # Display Parking Demand table
    st.subheader("Parking Demand")
    demand_data = get_parking_demand()
    demand_df = st.dataframe(demand_data)

    # Parking Summary
    total_spots = len(parking_data)
    available_spots = sum(1 for spot in parking_data if spot["availability"] == "Available")
    total_demand = sum(demand["num_vehicles"] for demand in demand_data)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Parking Spots", total_spots)
    with col2:
        st.metric("Available Spots", available_spots)
    with col3:
        st.metric("Total Demand", total_demand)

    # Inputs for new parking demand
    st.subheader("Add New Parking Demand")
    flat_no = st.number_input("Enter Flat No", min_value=1, step=1)
    num_vehicles = st.number_input("Number of Parking Spots Needed", min_value=1, step=1)

    # Check if parking demand can be fulfilled
    if st.button("Add Parking Demand"):
        if num_vehicles > available_spots:
            st.warning("Cannot fulfill demand, parking is full or insufficient spots available.")
        else:
            try:
                create_parking_demand(flat_no, num_vehicles)
                st.success(f"Parking demand for flat {flat_no} added successfully.")
                # Refresh demand and parking tables
                demand_data = get_parking_demand()
                parking_data = get_available_parking()
                demand_df.dataframe(demand_data)
                parking_df.dataframe(parking_data)
            except Exception as e:
                st.error(f"Error adding parking demand: {str(e)}")

    # Delete parking demand functionality
    if demand_data:
        st.subheader("Remove Parking Demand")
        flat_no = st.selectbox("Select Flat Number to Remove",
                               [demand["flat_no"] for demand in demand_data],
                               key="security_flat_no")

        if st.button("Remove Demand", key="security_remove_demand_btn"):
            try:
                delete_parking_demand(flat_no)
                st.success(f"Removed parking demand for flat {flat_no}")
                # Refresh demand and parking tables
                demand_data = get_parking_demand()
                parking_data = get_available_parking()
                demand_df.dataframe(demand_data)
                parking_df.dataframe(parking_data)
            except Exception as e:
                st.error(f"Error removing parking demand: {str(e)}")

from backend import get_facilities, get_facility_demand, get_instructors, get_managers, get_management_committee, create_user, delete_user

import streamlit as st


def supervisor_page():
    st.title("Supervisor Dashboard")

    # Display Facilities Available table
    st.subheader("Facilities Available")
    facilities_data = get_facilities()
    facilities_df = st.dataframe(facilities_data)

    # Display Facility Demand table
    st.subheader("Facility Demand")
    facility_demand_data = get_facility_demand()
    facility_demand_df = st.dataframe(facility_demand_data)

    # Display Instructors table
    st.subheader("Instructors")
    instructors_data = get_instructors()
    instructors_df = st.dataframe(instructors_data)

    # Display Management Committee table
    st.subheader("Management Committee")
    management_committee_data = get_management_committee()
    management_df = st.dataframe(management_committee_data)

    # Add New User Section
    st.subheader("Add New User")
    col1, col2, col3 = st.columns(3)
    with col1:
        new_name = st.text_input("Name", key="new_user_name")
    with col2:
        new_role = st.selectbox("Role",
                                ["Activities", "Facilities", "Security", "User"],
                                key="new_user_role")
    with col3:
        new_password = st.text_input("Password", type="password", key="new_user_password")

    if st.button("Add User", key="add_user_btn"):
        try:
            create_user(new_name, new_role, new_password)
            st.success(f"User {new_name} created successfully!")
            # Refresh management committee table
            management_committee_data = get_management_committee()
            management_df.dataframe(management_committee_data)
        except Exception as e:
            st.error(f"Error adding user: {str(e)}")

    # Delete User Section
    st.subheader("Delete User")
    non_supervisors = [row["name"] for row in management_committee_data
                       if row["role"] != "Supervisor"]

    if non_supervisors:  # Only show delete section if there are users to delete
        col1, col2 = st.columns([3, 1])
        with col1:
            user_to_delete = st.selectbox("Select User to Delete",
                                          non_supervisors,
                                          key="delete_user_select")
        with col2:
            if st.button("Delete User", key="delete_user_btn"):
                try:
                    delete_user(user_to_delete)
                    st.success(f"User {user_to_delete} deleted successfully!")
                    # Refresh management committee table
                    management_committee_data = get_management_committee()
                    management_df.dataframe(management_committee_data)
                except Exception as e:
                    st.error(f"Error deleting user: {str(e)}")

    # Parking Management Section
    st.subheader("Parking Management")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Parking Demand")
        parking_demand_data = get_parking_demand()
        parking_demand_df = st.dataframe(parking_demand_data)

    with col2:
        st.subheader("Available Parking")
        parking_availability_data = get_available_parking()
        parking_availability_df = st.dataframe(parking_availability_data)

    # Dashboard Summary
    st.subheader("Dashboard Summary")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_users = len(management_committee_data)
        st.metric("Total Users", total_users)

    with col2:
        total_facilities = len(facilities_data)
        st.metric("Total Facilities", total_facilities)

    with col3:
        total_instructors = len(instructors_data)
        st.metric("Total Instructors", total_instructors)

    with col4:
        available_parking = sum(1 for spot in parking_availability_data
                                if spot["availability"] == "Available")
        st.metric("Available Parking", available_parking)
# Main app logic
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "create_user":
        create_user_page()
else:
    main_page()

