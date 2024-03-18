# Movie Rating System

This project is a movie rating system that allows reviewers to rate movies and displays the top 100 rated movies along with the reviewers' names. It uses Python to interact with a MySQL database and includes functions for checking if tables exist, creating tables, inserting data, and retrieving data.

## Installation

1. Clone the repository: `git clone https://github.com/your_username/movie-rating-system.git`
2. Install the required dependencies: `pip install mysql-connector-python python-dotenv`

## Usage

1. Create a `.env` file in the root directory with your MySQL root password: `MYSQL_ROOT_PASSWORD=your_password`
2. Run the main Python script: `python main.py`
3. Follow the prompts to input your reviewer ID and rate movies.

## Functions

- `is_table_exists(table_name)`: Checks if a table exists in the database.
- `create_reviewer_table()`: Creates a reviewer table in the database.
- `create_rating_table()`: Creates a rating table in the database.
- `step1(reviewer_id)`: Checks if a reviewer exists in the database and creates a new reviewer account if not.
- `step2(reviewer_id)`: Prompts the user for their first and last name and inserts a new row into the reviewer table.
- `step3(reviewer_id)`: Allows a reviewer to rate a film by entering the film name and rating.
- `step4(reviewer_id,film_id)`: Collects a user's rating for a film, checks if the input is valid, and updates or adds the rating to the database.
- `step5()`: Retrieves and displays the top 100 rated movies along with the reviewers' names.


