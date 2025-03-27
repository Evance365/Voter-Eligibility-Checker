import json
import csv

# Function to check voting eligibility
def check_voting_eligibility(age):
    return age >= 18

# Function to save user data
def save_user_data(users):
    with open("voter_data.json", "w") as file:
        json.dump(users, file, indent=4)
    print("\n User data saved successfully.\n")

# Function to load user data
def load_user_data():
    try:
        with open("voter_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to display previous users
def display_previous_users(users):
    if users:
        print("\n Previous Users Checked:")
        for user in users:
            print(f"🔹 {user['name']} ({user['age']} years old) - {user['status']}")
        print("\n")
    else:
        print("\nNo previous user data found.\n")

# Function to search for a user by name
def search_user(users, name):
    for user in users:
        if user["name"].lower() == name.lower():
            return user
    return None

# Function to delete a user
def delete_user(users):
    name = input("Enter the name of the user to delete: ").strip()
    user = search_user(users, name)
    if user:
        users.remove(user)
        print(f" {name} has been deleted from the system.\n")
    else:
        print(f" User '{name}' not found.\n")

# Function to update age
def update_age(users):
    name = input("Enter the name of the user to update: ").strip()
    user = search_user(users, name)
    if user:
        try:
            new_age = int(input(f"Enter the new age for {name}: "))
            if new_age < 0:
                raise ValueError("Age cannot be negative.")
            user["age"] = new_age
            user["status"] = "Eligible" if check_voting_eligibility(new_age) else "Not Eligible"
            print(f" Age updated successfully for {name}.\n")
        except ValueError as e:
            print(f" Invalid input: {e}")
    else:
        print(f" User '{name}' not found.\n")

# Function to export data to CSV
def export_to_csv(users):
    filename = "voter_data.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "age", "status"])
        writer.writeheader()
        writer.writerows(users)
    print(f"\n User data exported to {filename}\n")

# Main program
def main():
    users = load_user_data()
    
    # Display previous users before taking new input
    display_previous_users(users)

    while True:
        print("\nOptions:")
        print("1️⃣ Check voter eligibility")
        print("2️⃣ Delete a user")
        print("3️⃣ Update a user's age")
        print("4️⃣ Export data to CSV")
        print("5 Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":  # Check voter eligibility
            name = input("Enter your name: ").strip()
            existing_user = search_user(users, name)
            
            if existing_user:
                print(f" {name}, you have already been checked.")
                print(f" Status: {existing_user['status']} to vote.\n")
                continue  

            try:
                age = int(input("Enter your age: "))
                if age < 0:
                    raise ValueError("Age cannot be negative.")

                eligible = check_voting_eligibility(age)
                status = "Eligible" if eligible else "Not Eligible"
                print(f"{name}, you are {status} to vote.")

                # Store new user data
                users.append({"name": name, "age": age, "status": status})
            
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid age.")

        elif choice == "2":  # Delete user
            delete_user(users)

        elif choice == "3":  # Update user age
            update_age(users)

        elif choice == "4":  # Export to CSV
            export_to_csv(users)

        elif choice == "5":  # Exit
            save_user_data(users)
            print("Thank you for using the voter eligibility checker!")
            break

        else:
            print(" Invalid choice. Please select a valid option (1-5).")

# Run the program
if __name__ == "__main__":
    main()
