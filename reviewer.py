import os
import mysql.connector
# getting info from the .env file
from dotenv import load_dotenv
load_dotenv()
Password = os.getenv('MYSQL_ROOT_PASSWORD')


# Create a connection
cnx = mysql.connector.connect(
    user='root',
    password=os.getenv(Password, Password),
    host='127.0.0.1',
    database='sakila'
)

# Create a cursor
cursor = cnx.cursor()
cnx.autocommit = True


# OUR CODE


#This function checks if a table with a given name exists in an SQL database.
#It does this by executing a SELECT statement on the INFORMATION_SCHEMA.
#TABLES table and counting the number of rows returned.

def is_table_exists(table_name):

    statement = '''select *
                        from INFORMATION_SCHEMA.TABLES
                        WHERE TABLE_NAME = "'''+table_name +'";'
    cursor.execute(statement)
    isExist = len(cursor.fetchall())
    return isExist

# This function creates a reviewer table in an SQL database.
def create_reviewer_table():
        cursor.execute("""
        CREATE TABLE reviewer (
        reviewer_id INT NOT NULL ,
        first_name VARCHAR(45) NOT NULL,
        last_name VARCHAR(45) NOT NULL,
        PRIMARY KEY(reviewer_id));""")

# This function creates a rating table in an SQL database.
def create_rating_table():
        cursor.execute("""
        CREATE TABLE rating (
        film_id SMALLINT UNSIGNED NOT NULL,
        reviewer_id INT NOT NULL,
        rating  DECIMAL(2,1) NOT NULL CHECK(RATING>=0.0 AND RATING<=9.9) ,
        FOREIGN KEY(film_id) REFERENCES film(film_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY(reviewer_id) REFERENCES reviewer(reviewer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE);""")


#This function checks if a reviewer with the given ID exists in the reviewer table of an SQL database.
#If the reviewer exists, the function returns without doing anything.
#Otherwise, if the reviewer does not exist, it prints a message and calls the step2()
#function to create a new reviewer account.

def step1(reviewer_id):
    cursor.execute("SELECT * FROM reviewer WHERE reviewer_id = "+str(reviewer_id)+";")
    result = cursor.fetchall()
    if(len(result)):
        return
    print("ID not in DataBase, Creating new reviewer Account\n")
    step2(reviewer_id)


#This function prompts the user for their first and last name,
#then inserts a new row into the reviewer table in an SQL database
#with the given reviewer_id and the user's first and last name.
def step2(reviewer_id):

    f_name = input("input you first name\n")
    l_name = input("input you last name\n")
    value = str((reviewer_id,f_name,l_name))
    insert_statement = "INSERT INTO reviewer (reviewer_id, first_name, last_name) VALUES " + value + ";"
    cursor.execute(insert_statement)
    return

#This function retrieves the film_id and release_year for a movie with a given name from an SQL database.
def get_movies_by_name(film_name):
        statement = """SELECT film_id,release_year
                    FROM sakila.film
                    where title = '"""+film_name+"""';"""
        cursor.execute(statement)
        result = cursor.fetchall()
        return result

#This function allows a reviewer to rate a film in a database.
#It prompts the reviewer for their name and the name of the film they want to rate,
#then checks if the film exists in the database and, if it does,
#calls the "step4" function to handle the rating process.
#If the film does not exist or if multiple films with the same name are found,
#the user is prompted to enter the film name again until a unique film is found.
def step3(reviewer_id):
    statement = """SELECT first_name,last_name
                            FROM reviewer
                            where reviewer_id = """ +str(reviewer_id) +";"
    cursor.execute(statement)
    reviewer_name = cursor.fetchone()

    print("Hello, "+reviewer_name[0] + " "+ reviewer_name[1]+"\n")
    
    film_name = input("please insert the name of the film you want to rate\n")
    results = get_movies_by_name(film_name)
    while(len(results)!=1):
        if(len(results) == 0):
            film_name = input("film does not exist. input the name of the film again\n")
            results = get_movies_by_name(film_name)    
        else:
            print("There are multiple films with this name:\n")
            for result in results:
                print(result)
            chosen_film_id = int(input("please choose specific id:\n"))
            
            for result in results:
                if(result[0] == chosen_film_id):
                    step4(reviewer_id,result[0])
                    return

            film_name = input("film does not exist. input the name of the film again\n")
            results = get_movies_by_name(film_name)
            

    step4(reviewer_id,results[0][0])

#This function checks if a given input is a valid numeric value between 0 and 10 (inclusive).
def check_if_valid_input(input):
    try:
        float(input)
    except ValueError:
        return False
    if(float(input)>=0 and float(input) <10):
        return True
    return False

#This function checks if a given reviewer has already reviewed a given film by
#executing a SELECT statement on the rating table and counting the number of rows returned.
def check_if_reviewer_already_reviewed_film(reviewer_id,film_id):
    statement = """SELECT *
                    FROM sakila.rating
                    WHERE film_id = """+str(film_id)+""" AND reviewer_id = """+str(reviewer_id)+";"
 
    cursor.execute(statement)
    result = cursor.fetchall()
    return(len(result))

#This function updates the rating of a film in an SQL database.
def update_rate(reviewer_id,film_id,rate):

    statement =   """UPDATE rating 
                        SET 
                        rating = """ + rate + """ WHERE 
                        film_id = """ + film_id +" AND reviewer_id = " + reviewer_id + ";"
    cursor.execute(statement)

#This function adds a rating of a film to the SQL database.    
def add_rating(reviewer_id,film_id,rating):
    statement = "INSERT INTO rating (film_id,reviewer_id,rating) VALUES ("+film_id+","+reviewer_id+","+rating+");"
    cursor.execute(statement)



# This function collects a user's rating for a film,
# checks if the input is valid, and either updates or adds the rating to the database.
def step4(reviewer_id,film_id):

    rating = input("Please rate the movie 0-10\n")
    isValid = check_if_valid_input(rating)

    while(not isValid):
        rating = input("Invalid input! Please rate the movie 0-10\n")
        isValid = check_if_valid_input(rating)
    
    if(check_if_reviewer_already_reviewed_film(reviewer_id,film_id)):
        update_rate(str(reviewer_id),str(film_id),str(rating))
        print("you rated this movie before. your rate has been updated!\n")
    else:
        add_rating(str(reviewer_id),str(film_id),str(rating))
        print("Your rate has been inserted! thank you darling!\n")


# This function executes an SQL SELECT statement that retrieves the title,
# reviewer's full name, and rating of the top 100 films from a database.
# It then formats and prints the results to the console.

def step5():
    statement = """ SELECT f.title,CONCAT(re.first_name, " ", re.last_name) as full_name, ra.rating 
                    FROM sakila.rating as ra, sakila.film as f, sakila.reviewer as re
                    WHERE ra.film_id = f.film_id AND
		            re.reviewer_id = ra.reviewer_id
                    LIMIT 100 """
    cursor.execute(statement)
    results = cursor.fetchall()

    print ("{:<30} {:<30} {:<30}".format('title','full name','rate'))
    print()
    for result in results:
        t = result[0]
        f = result[1]
        r = result[2]
        print ("{:<30} {:<30} {:<30}".format(t, f, r))
    print("\n\n\n\n\n\n")



# This code defines the main() function, which checks if the reviewer and rating tables exist in the database.
# If either table does not exist, it calls the appropriate function to create it.
# Then, the main() function enters an infinite loop that prompts the user for an ID,
# calls the step1() and step3() functions with the given ID, and finally calls the step5() function.
def main():
    if (not is_table_exists("reviewer")):
        create_reviewer_table()
    if (not is_table_exists("rating")):
        create_rating_table()
    while(True):
        id = int(input("please insert your ID\n"))
        step1(id)
        step3(id)
        step5()


if __name__ == '__main__':
    main()

# Close the connection
cnx.close()