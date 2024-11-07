# Fake User Database Generator

A Python application that generates a SQLite database populated with realistic fake user data. The tool provides both GUI and CLI interfaces for easy data generation.

## Features

- Generate SQLite database with fake user data
- Customizable number of entries
- GUI and CLI interfaces
- Comprehensive user information including:
  - Personal details (name, email, age)
  - Location information (address, city, country)
  - Professional information (job, company)
- Option to add or replace existing data
- Configurable database location

## Prerequisites

- Python 3.6+
- Required Python packages (install using `pip install -r requirements.txt`):
  - faker
  - sqlite3 (usually comes with Python)
  - tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Arthur469/fpyez-fakedb.git
cd pyez-fakedb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI

1. Run the application without arguments to launch the GUI interface:
```bash
python main.py
```

### CLI Mode

Use command-line arguments to generate data without the GUI:
```bash
python main.py -n 100 -d my_database -f /path/to/folder
```

#### CLI Arguments

- `-n, --num_entries`: Number of fake entries to generate
- `-d, --database_name`: Name of the database file (default: test_database)
- `-f, --folder_path`: Path to store the database (default: db)

## Database Schema

The generated SQLite database includes a `users` table with the following fields:

- `id` (Primary Key)
- `user_id` (Unique)
- `first_name`
- `last_name`
- `email` (Unique)
- `password`
- `age`
- `birth_year`
- `city`
- `zip_code`
- `country`
- `phone_number`
- `address`
- `job`
- `company`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details
