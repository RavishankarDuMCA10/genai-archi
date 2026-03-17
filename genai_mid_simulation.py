user_data = {
    "user1": {"password": "password1", "role": "free"},
    "user2": {"password": "password2", "role": "premium"},
}


# Simulated feedback storage (Loop for model improvement)
feedback_data = {}


# Simulate a simple AI model that adjust its "quality" based on feedback
def adjust_model_based_on_feedback():
    good_feedback_count = sum(i for f in feedback_data.values() if f == "good")
    return 100 - (
        5 * good_feedback_count
    )  # Reduce summary length by 5 chars for each feedback


# User login simulation (Application layer)
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in user_data and user_data[username]["password"] == password:
        print(f"Login successful for {username}. Role: {user_data[username]['role']}")
        return username, user_data[username]["role"]
    else:
        print("Login failed. Invalid username or password.")
        return None, None


# Data validation gate and access control (Gate)
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
        # Document processing pipeline (Pipeline)
        document = "This is a sample document for GenAI summarization. " * 5
        summarize_document(document)


# Document summarization simulation (Model layer)
def summarize_document(document):
    # Adjust summary based on feedback (Model Layer)
    summary_length = adjust_model_based_on_feedback()
    summary = document[
        :summary_length
    ]  # Truncate document based on "model adjustments"
    print(f"Summary: {summary}...\nSummary")

    # Simulate user feedback
    gather_feedback(summary)


# Simulate feedback loop (Loop)
def gather_feedback(summary):
    print("\nHow was the summary?")
    feedback = input("Enter feedback (good/bad): ")
    if feedback not in ["good", "bad"]:
        print("Invalid feedback. Please enter 'good' or 'bad'.")
        return
    else:
        # Simulate storing feedback for future model improvement
        feedback_data[summary] = feedback
        print(f"Feedback stored. {feedback}")


# Pipeline: Simulation user login and document upload process
def start_simulation():
    username, user_role = login()

    if user_role:
        while True:
            try:
                # Pipeline: Simulate document upload and summarization
                upload_document(user_role)
            except PermissionError as e:
                print(e)

            # Ask the user if they want to continue or quit
            choice = input("Do you want to continue? (yes/no): ")
            if choice.lower() == "no":
                print("Exiting simulation. Thanks for your feedback!")
                break
    else:
        print("Login failed. Please try again.")


# Start the simulation
start_simulation()

# Print feedback data (Loop to improve model later)
print("\nFeedback received so far:", feedback_data)
