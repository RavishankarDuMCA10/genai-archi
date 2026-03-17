from dotenv import load_dotenv
import logging
import os
import asyncio
import sqlite3
import hashlib
import secrets
from cryptography.fernet import Fernet

from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# SQLite database setup (simulated)
# === Application Layer: SQLite database setup (Simulates storing users and feedback)

conn = sqlite3.connect(":memory:")  # In-memory database for simulation
cursor = conn.cursor()

cursor.execute("""CREATE TABLE users (username TEXT,password TEXT, role TEXT)""")
cursor.execute("""CREATE TABLE feedback (username TEXT, feedback TEXT)""")

# Add sample users to the database
cursor.execute(
    'INSERT INTO users VALUES ("user1", ?, "free")',
    (hashlib.sha256("password1".encode()).hexdigest(),),
)
cursor.execute(
    'INSERT INTO users VALUES ("user2", ?, "premium")',
    (hashlib.sha256("password2".encode()).hexdigest(),),
)
conn.commit()

# Simulated cloud storage (Infrastructure Layer)
# === Infrastructure Layer: Simulated cloud storage for documents
cloud_storage = {
    "documents": [],
}

# Generate and store the encrypted key (should be stored securely )
key = Fernet.generate_key()
cipher_suite = Fernet(key)


# Encrypt a document
# ==== Infrastructure Layer: Encrypting documents before storing in cloud storage
def encrypt_document(document):
    print("Encrypting document...")
    encrypted_doc = cipher_suite.encrypt(document.encode())
    return encrypted_doc


# Decrypt a document
# ==== Infrastructure Layer: Decrypting documents when retrieving from cloud storage
def decrypt_document(encrypted_doc):
    print("Decrypting document...")
    decrypted_doc = cipher_suite.decrypt(encrypted_doc).decode()
    return decrypted_doc


# GPT-4o Summarization Function
# === Model Layer: GPT-4o Summarization Function using OpenAI API
def gpt4o_summarization(text):
    print("Summarizing document with GPT-4o...")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Please summarize the following text:"},
            {"role": "user", "content": text},
        ],
        max_tokens=150,
        temperature=0.7,
    )
    summary = response.choices[0].message.content.strip()
    return summary


# User login with token-based authentication (Authentication Layer)
# === Authentication Layer: User login with token-based authentication
async def login():
    username = input("Enter username: ")
    password = hashlib.sha256(input("Enter password: ").encode()).hexdigest()

    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?", (username, password)
    )
    result = cursor.fetchone()

    if result:
        role = result[0]
        token = secrets.token_hex(16)  # Generate a simple token
        print(f"Login successful! Your role: {role}, Token: {token}")
        return username, role, token
    else:
        print("Invalid credentials!")
        return None, None, None


# Document upload with file size valiadation gate (Gate)
# === Gate: Document upload with file size validation and encryption


async def upload_document(role, token):
    print("\nUpload a document")
    file_path = "./data/i-have-a-dream.txt"  # Simulated file path

    try:
        # Get the file size
        # === Gate: Get the file size to validate based on the user role
        document_size = os.path.getsize(file_path)
        logging.info(f"Document size: {document_size} bytes")
    except FileNotFoundError:
        logging.error(
            f"File {file_path} not found. Please ensure the file exists at the specified path."
        )
        return
    except Exception as e:
        logging.error(f"An error occurred while getting the file size: {e}")
        return

    size_limit = 10240  # 10 KB size limit for the free users

    if role == "free" and document_size > size_limit:
        logging.error("Document size exceeds limit for free users.")
        raise PermissionError("Document size exceeds limit for free users.")
    else:
        # Read and encrypt the content of the file
        # === Infrastructure Layer: Read and encrypt the content of the file

        with open(file_path, "r") as file:
            document = file.read()
            encrypted_document = encrypt_document(document)

        if role == "free":
            # Real-time processing (Pipeline)
            # === Pipeline: Real-time processing for free user
            print("Document uploded for real-time processing...")
            await summarize_document(encrypt_document)
        else:
            # Batch processing (Pipeline)
            # === Pipeline: Batch processing for premium user
            print("Document uploded for batch processing...")
            cloud_storage["documents"].append(encrypted_document)
            logging.info("Document uploaded for batch processing.")


# Document summarization using GPT-4o (Model Layer)
# === # Model Layer: Document summarization using GPT-4o for batch processing


async def summarize_document(encrypted_document):
    # Decrypt document before summarization
    document = decrypt_document(encrypted_document)

    # Use GPT-4o to summarize the document
    summary = gpt4o_summarization(document)
    logging.info(f"Summary: {summary}")

    # Simulate feedback loop (Feedback Loop)
    await gather_feedback(summary)


# Feedback loop for user feedback on summaries (Feedback Loop)
# === Feedback Loop: Collecting user feedback on summaries to improve the model
async def gather_feedback(summary):
    print("\nHow was the summary")
    feedback = input("Enter feedback (good/bad): ").lower()
    if feedback not in ["good", "bad"]:
        logging.error("Invalid feedback. Please enter 'good' or 'bad'.")
    else:
        cursor.execute("INSERT INTO feedback VALUES (?, ?)", (summary, feedback))
        conn.commit()
        logging.info("Feedback recorded successfully. Feedback: " + feedback)


# Simulate user login and document upload process
async def start_simulation():
    username, user_role, token = await login()

    if user_role:
        while True:
            try:
                await upload_document(user_role, token)
            except PermissionError as e:
                logging.error(e)

            # Ask user if they want to continue or quit
            choice = input("Do you want to continue? (yes/no): ").lower()
            if choice == "no":
                logging.info("Exiting the simulation. Thanks for your feedback!")
                break
    else:
        logging.error("Login failed. Please try again.")


# Simulate batch processing for premium users (Infrastucture Layer)
async def batch_processing():
    if cloud_storage["documents"]:
        logging.info("Batch processing the following documents for premium users:")
        for encrypted_doc in cloud_storage["documents"]:
            await summarize_document(encrypted_doc)
        cloud_storage["documents"].clear()  # Clear after processing


# Start the simulation with asyncio concurrency
async def main():
    await start_simulation()
    await batch_processing()


# Run the simulation
asyncio.run(main())

# Print feedback data for debugging (Loop to improve model later)
cursor.execute("SELECT * FROM feedback")
logging.info("Feedback received so far: {cursor.fetchall()}")
