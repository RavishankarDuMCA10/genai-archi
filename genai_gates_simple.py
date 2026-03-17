# Simulated user data
user_data = {
    "user1": {"password": "password1", "role": "free"},
    "user2": {"password": "password2", "role": "premium"},
}


# User login simulation
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in user_data and user_data[username]["password"] == password:
        print(f"Login successful for {username}. Role: {user_data[username]['role']}")
        return user_data[username]["role"]
    else:
        print("Login failed. Invalid username or password.")
        return None


# Document upload gate with user-input document size
def upload_document(role):
    try:
        document_size = int(input("Enter document size in bytes: "))
    except ValueError:
        print("Invalid input. Please enter a numeric value for document size.")
        return

    size_limit = 10240  # 10 KB size limit for free users
    print(f"Document size: {document_size} bytes")

    if role == "free" and document_size > size_limit:
        raise PermissionError("Document size exceeds the limit for free users.")
    else:
        summarize_document()


# Document summarization simulation
def summarize_document():
    print("Document summarized successfully.")


# Simulate user login and document upload
user_role = login()

if user_role:
    try:
        upload_document(user_role)
    except PermissionError as e:
        print(e)
