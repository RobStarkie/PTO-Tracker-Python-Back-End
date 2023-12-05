# PTO Tracker | Python Backend

This repository has been created to work with our React front end for a PTO Tracker. By following the steps below you can setup and run the backend of our application correctly.

## Prerequisites
- Python 3.x
- pip (Python package installer)
- MySQL Workbench
- Git

## Installation

### Cloning the Repository

1. Open your terminal.
2. Navigate to the directory where you want to clone the repository.
3. Clone the repository
   ```sh
   git clone https://github.com/RobStarkie/PTO-Tracker-Python-Back-End.git
   ```
4. Navigate into the cloned repository: 
    ```sh
    cd PTO-Tracker-Python-Back-End
    ```
### Creating the Virtual Environment
1. Create a virtual environment:
   - `python -m venv venv` (Windows)
   - `python3 -m venv venv` (macOS/Linux)
2. Activate the virtual environment:
   - `venv\Scripts\activate` (Windows)
   - `source venv/bin/activate` (macOS/Linux)
   
2. Install the requirements
   ```sh
   pip install requirements.txt
   ```
### Configuring MySQL
1. Install MySQL Workbench from the [official website](https://dev.mysql.com/downloads/workbench/).
2. Open MySQL Workbench and set up a new connection to the local MySQL server.

### Setup

1. Create test data in the backend
    ```sh
   pytest .\databaseTests.py
   ```
### Running the Flask Application

1. Ensure you are in the project's root directory.

2. Run the Flask application:
   - `flask run`
