import pymongo
from pymongo.errors import ConnectionFailure

def connect_to_db():
    """Establishes connection to the MongoDB server."""
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping') 
        
        db = client['student_management_db']
        collection = db['students']
        return collection
    except ConnectionFailure:
        print("\n[ERROR] Could not connect to MongoDB. Is the server running?")
        return None

def add_student(collection):
    print("\n--- ADD NEW STUDENT ---")
    reg_no = input("Enter Register Number: ").strip()
    
    if collection.find_one({"register_no": reg_no}):
        print(f"[WARNING] Student with Register Number {reg_no} already exists!")
        return

    name = input("Enter Full Name: ").strip()
    email = input("Enter Email: ").strip()
    department = input("Enter Department (e.g., CS, DS): ").strip().upper()
    status = input("Enter Status (ACTIVE/INACTIVE): ").strip().upper()

    student_data = {
        "register_no": reg_no,
        "name": name,
        "email": email,
        "department": department,
        "status": status
    }

    result = collection.insert_one(student_data)
    print(f"\n[SUCCESS] Student added with MongoDB ID: {result.inserted_id}")

def view_all_students(collection):
    print("\n--- ALL STUDENTS ---")
    students = collection.find()
    
    if collection.count_documents({}) == 0:
        print("No students found in the database.")
        return

    for student in students:
        print(f"Reg No: {student.get('register_no')} | Name: {student.get('name')} | Dept: {student.get('department')} | Status: {student.get('status')}")

def search_student(collection):
    print("\n--- SEARCH STUDENT ---")
    reg_no = input("Enter Register Number to search: ").strip()
    
    student = collection.find_one({"register_no": reg_no})
    
    if student:
        print("\n--- Student Found ---")
        print(f"Name: {student.get('name')}")
        print(f"Email: {student.get('email')}")
        print(f"Department: {student.get('department')}")
        print(f"Status: {student.get('status')}")
    else:
        print(f"\n[NOT FOUND] No student exists with Register Number: {reg_no}")

def update_student_status(collection):
    print("\n--- UPDATE STUDENT STATUS ---")
    reg_no = input("Enter Register Number to update: ").strip()
    
    student = collection.find_one({"register_no": reg_no})
    
    if student:
        print(f"Current Status is: {student.get('status')}")
        new_status = input("Enter New Status (ACTIVE/INACTIVE): ").strip().upper()
        
        collection.update_one(
            {"register_no": reg_no},
            {"$set": {"status": new_status}}
        )
        print(f"\n[SUCCESS] Status updated to {new_status} for {student.get('name')}.")
    else:
        print(f"\n[NOT FOUND] No student exists with Register Number: {reg_no}")

def delete_student(collection):
    print("\n--- DELETE STUDENT ---")
    reg_no = input("Enter Register Number to delete: ").strip()
    
    result = collection.delete_one({"register_no": reg_no})
    
    if result.deleted_count > 0:
        print(f"\n[SUCCESS] Student {reg_no} has been successfully deleted.")
    else:
        print(f"\n[NOT FOUND] No student exists with Register Number: {reg_no}")

def main():
    collection = connect_to_db()
    if collection is None:
        return

    while True:
        print("\n" + "="*35)
        print(" STUDENT MANAGEMENT SYSTEM (NoSQL)")
        print("="*35)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student by Register No")
        print("4. Update Student Status")
        print("5. Delete Student")
        print("6. Exit")
        print("="*35)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            add_student(collection)
        elif choice == '2':
            view_all_students(collection)
        elif choice == '3':
            search_student(collection)
        elif choice == '4':
            update_student_status(collection)
        elif choice == '5':
            delete_student(collection)
        elif choice == '6':
            print("\nExiting the system. Goodbye!")
            break
        else:
            print("\n[INVALID] Please select a valid option between 1 and 6.")

if __name__ == "__main__":
    main()