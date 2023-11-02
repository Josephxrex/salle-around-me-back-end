# SalleAroundMe Back-End

## Description
SalleAroundMe Back-End is an API that serves as the backbone for the SalleAroundMe project. It provides essential functionalities for user registration and authentication, allowing users to create accounts, log in securely, and access the features of the SalleAroundMe application. The API manages user data, ensuring a seamless and secure user experience.

## Project Structure
```bash
│
├── app/
│ ├── models/
│ │ ├── __init__.py
│ │ ├── user.py
│ ├── routes/
│ │ ├── __init__.py
│ │ ├── user.py
│ └── app.py
├── README.md

## Setting Up the Project

Before running the project, follow these steps to set up your development environment:

### 1. Create a Virtual Environment
```bash
# On Windows
python -m venv venv

# On macOS and Linux
python3 -m venv venv

## Setting Up the Project

### 2. Activate the Virtual Environment

**On Windows**
```bash
venv\Scripts\activate

source venv/bin/activate

### 3. Install Required Packages

While the virtual environment is active, install the project's dependencies using pip:

```bash
pip install -r requirements.txt

## Running the Project

To run the Flask application, execute the following command in your terminal from the project's root directory:

```bash
flask run 

After running the command, Flask will start, and your application will be available at http://127.0.0.1:5000/ by default. You can access your Flask application in a web browser by entering that address in the URL bar.
