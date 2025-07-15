# Streamlit SQL App

This project is a Streamlit application that allows users to input questions about students and generates corresponding SQL queries. The application interacts with a database to execute these queries and return results.

## Project Structure

```
streamlit-sql-app
├── src
│   ├── app.py          # Main entry point for the Streamlit application
│   ├── db.py           # Handles database connections and operations
│   └── llm.py          # Interacts with the language model API to generate SQL queries
├── requirements.txt     # Lists necessary Python packages
└── README.md            # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd streamlit-sql-app
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your database:**
   Ensure you have a database set up and update the connection details in `src/db.py`.

5. **Run the application:**
   ```bash
   streamlit run src/app.py
   ```

## Usage Guidelines

- Open the application in your web browser.
- Enter your question about students in the input field.
- Click the "Generate SQL Query" button to see the generated SQL query and its results.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.