import mysql.connector
import hashlib
import streamlit as st


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="3214",
        database="dbmsfinalpromise"
    )


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(name, role, password):
    conn = create_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)  # Hash the password before storing

    query = """INSERT INTO management_committee (name, role, password_hash) VALUES (%s, %s, %s)"""
    cursor.execute(query, (name, role, password_hash))  # Use the hashed password
    conn.commit()
    cursor.close()
    conn.close()

def verify_user(name, password):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT role, password_hash FROM management_committee WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        role, password_hash = result
        if password_hash == hash_password(password):  # Compare hashed versions
            return role
    return None

def get_instructors():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM instructor")
    instructors = cursor.fetchall()
    cursor.close()
    conn.close()
    return instructors

def get_managers():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT manager_id, name FROM management_committee WHERE role = 'Activities'")
    managers = cursor.fetchall()
    cursor.close()
    conn.close()
    return managers
def get_valid_descriptions():
    return ["Basketball Coach", "Badminton Coach", "Tennis Coach", "Piano Tutor", "Guitar Tutor", "Kids Tuition"]

def create_instructor(name, description, salary, manager_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "INSERT INTO instructor (instructor_name, description, salary, manager_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, description, salary, manager_id))
    activity_ids = [row[0] for row in cursor.fetchall()]
    for i, id in enumerate(activity_ids, start=1):
        query = "UPDATE instructor SET activity_id = %s WHERE activity_id = %s"
        cursor.execute(query, (i, id))
    conn.commit()
    cursor.close()
    conn.close()

def update_instructor(instructor_id, new_name, new_description, new_salary, new_manager_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "UPDATE instructor SET instructor_name = %s, description = %s, salary = %s, manager_id = %s WHERE activity_id = %s"
    cursor.execute(query, (new_name, new_description, new_salary, new_manager_id, instructor_id))
    activity_ids = [row[0] for row in cursor.fetchall()]
    for i, id in enumerate(activity_ids, start=1):
        query = "UPDATE instructor SET activity_id = %s WHERE activity_id = %s"
        cursor.execute(query, (i, id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_instructor(instructor_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Delete the instructor
    query = "DELETE FROM instructor WHERE activity_id = %s"
    cursor.execute(query, (instructor_id,))

    # Renumber the activity_id values
    cursor.execute("SELECT activity_id FROM instructor ORDER BY activity_id")
    activity_ids = [row[0] for row in cursor.fetchall()]
    for i, id in enumerate(activity_ids, start=1):
        query = "UPDATE instructor SET activity_id = %s WHERE activity_id = %s"
        cursor.execute(query, (i, id))

    conn.commit()
    cursor.close()
    conn.close()
def calculate_total_cost_by_role():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT description, SUM(salary) AS total_cost
    FROM instructor
    GROUP BY description
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
def create_facility_demand(facility, flat_no):
    conn = create_connection()
    cursor = conn.cursor()
    query = "INSERT INTO facility_demand (facility, flat_no) VALUES (%s, %s)"
    cursor.execute(query, (facility, flat_no))
    conn.commit()
    cursor.close()
    conn.close()

def create_parking_demand(flat_no, num_vehicles):
    conn = create_connection()
    cursor = conn.cursor()
    query = "INSERT INTO parking_demand (flat_no, num_vehicles) VALUES (%s, %s)"
    cursor.execute(query, (flat_no, num_vehicles))
    conn.commit()
    cursor.close()
    conn.close()
def get_facilities():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM facilities_available")
    facilities = cursor.fetchall()
    cursor.close()
    conn.close()
    return facilities

def create_facility(name, availability_status, manager_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "INSERT INTO facilities_available (facility_name, availability_status, manager_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, availability_status, manager_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_facility(facility_id, new_name, new_status, new_manager_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "UPDATE facilities_available SET facility_name = %s, availability_status = %s, manager_id = %s WHERE facility_id = %s"
    cursor.execute(query, (new_name, new_status, new_manager_id, facility_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_facility(facility_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "DELETE FROM facilities_available WHERE facility_id = %s"
    cursor.execute(query, (facility_id,))
    conn.commit()
    cursor.close()
    conn.close()
# Fetch facility demand data from the database
def get_facility_demand():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM facility_demand")  # Replace with your actual table name and schema
    demand_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return demand_data


def compare_facility_demand_supply():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # Get demand counts
    cursor.execute("""
        SELECT facility, COUNT(*) as demand_count 
        FROM facility_demand 
        GROUP BY facility
    """)
    demand = {row['facility']: row['demand_count'] for row in cursor.fetchall()}

    # Get available counts
    cursor.execute("""
        SELECT facility_name, COUNT(*) as available_count 
        FROM facilities_available 
        WHERE availability_status = 'Available'
        GROUP BY facility_name
    """)
    available = {row['facility_name']: row['available_count'] for row in cursor.fetchall()}

    # Compare and create results
    facilities = ['Plumber', 'Electrician', 'Gardener', 'Painter']
    results = {}

    for facility in facilities:
        demand_count = demand.get(facility, 0)
        available_count = available.get(facility, 0)
        difference = available_count - demand_count

        if difference >= 0:
            results[facility] = {
                'status': 'Requirements met',
                'difference': difference,
                'demand': demand_count,
                'available': available_count
            }
        else:
            results[facility] = {
                'status': f'Need to recruit {abs(difference)} more',
                'difference': difference,
                'demand': demand_count,
                'available': available_count
            }

    cursor.close()
    conn.close()
    return results


def delete_facility_demand(facility, flat_no):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Delete the facility demand entry using composite key
        query = "DELETE FROM facility_demand WHERE facility = %s AND flat_no = %s"
        cursor.execute(query, (facility, flat_no))

        if cursor.rowcount == 0:
            raise Exception("No matching facility demand found")

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
def get_available_parking():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM available_parking")
    parking = cursor.fetchall()
    cursor.close()
    conn.close()
    return parking

def get_parking_demand():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM parking_demand")
    demand = cursor.fetchall()
    cursor.close()
    conn.close()
    return demand

def update_parking_availability(car_park_no, availability):
    conn = create_connection()
    cursor = conn.cursor()
    # Convert 'Occupied' to 'Unavailable' to match database enum
    availability = "Unavailable" if availability == "Occupied" else availability
    query = "UPDATE available_parking SET availability = %s WHERE car_park_no = %s"
    cursor.execute(query, (availability, car_park_no))
    conn.commit()
    cursor.close()
    conn.close()


def delete_parking_demand(flat_no):
    conn = create_connection()
    cursor = conn.cursor()
    query = "DELETE FROM parking_demand WHERE flat_no = %s"
    cursor.execute(query, (flat_no,))
    conn.commit()
    cursor.close()
    conn.close()
def get_parking_status_options():
    """Get the valid status options for parking availability"""
    return ["Available", "Unavailable"]  # Match exact values from database


def create_parking_demand(flat_no, num_vehicles):
    conn = create_connection()
    cursor = conn.cursor()

    # Insert parking demand
    demand_query = "INSERT INTO parking_demand (flat_no, num_vehicles) VALUES (%s, %s)"
    cursor.execute(demand_query, (flat_no, num_vehicles))

    # Reserve parking spots
    update_query = "UPDATE available_parking SET availability = 'Unavailable' WHERE availability = 'Available' LIMIT %s"
    cursor.execute(update_query, (num_vehicles,))

    conn.commit()
    cursor.close()
    conn.close()


def delete_parking_demand(flat_no):
    conn = create_connection()
    cursor = conn.cursor()

    # Get the number of vehicles from the demand being deleted
    cursor.execute("SELECT num_vehicles FROM parking_demand WHERE flat_no = %s", (flat_no,))
    num_vehicles = cursor.fetchone()

    if num_vehicles:
        num_vehicles = num_vehicles[0]

        # Delete the demand
        delete_query = "DELETE FROM parking_demand WHERE flat_no = %s"
        cursor.execute(delete_query, (flat_no,))

        # Release parking spots
        release_query = "UPDATE available_parking SET availability = 'Available' WHERE availability = 'Unavailable' LIMIT %s"
        cursor.execute(release_query, (num_vehicles,))

    conn.commit()
    cursor.close()
    conn.close()
def load_parking_demand():
    demand = get_parking_demand()
    return demand
def load_available_parking():
    available_parking = get_available_parking()
    return available_parking
def get_management_committee():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT manager_id, name, role FROM management_committee")
    management_committee = cursor.fetchall()
    cursor.close()
    conn.close()
    return management_committee

def delete_user(name):
    conn = create_connection()
    cursor = conn.cursor()
    query = "DELETE FROM management_committee WHERE name = %s"
    cursor.execute(query, (name,))
    conn.commit()
    cursor.close()
    conn.close()


def get_salary_statistics():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.callproc('CalculateAverageSalaryByRole')

        # Get results from the stored procedure
        for result in cursor.stored_results():
            statistics = result.fetchall()
            return statistics

    except Exception as e:
        st.error(f"Error getting salary statistics: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()
