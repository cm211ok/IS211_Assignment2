import argparse
import urllib.request
import logging
import datetime
import csv  

# Configure logging
logger = logging.getLogger("assignment2")
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def downloadData(url):
    """Downloads CSV data from a given URL and returns it as text."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')  # Decode file content
    except Exception as e:
        logging.error(f"ERROR: Failed to download data. Reason: {e}")
        print("Error downloading data. Exiting program.")
        return None

def processData(file_content):
    personData = {}
    reader = csv.reader(file_content.splitlines())  
    next(reader, None)  
    for row in reader:
        if not row or len(row) < 3:  
            logging.error(f"Skipping invalid row: {row}")
            continue
        try:
            person_id = int(row[0])  
            name = row[1]
            birthdate = datetime.datetime.strptime(row[2], "%d/%m/%Y").date()  
            personData[person_id] = (name, birthdate)
        except ValueError as e:
            logging.error(f"Error processing row {row}: {e}")
    return personData

def displayPerson(person_id, personData):
    """Displays a person's data given their ID."""
    if person_id in personData:
        name, birthdate = personData[person_id]
        print(f"Person {person_id} is {name} with a birthday of {birthdate}")
    else:
        print(f"No record found for ID {person_id}")

def main(url):
    print(f"Running main with URL = {url}...")
    csvData = downloadData(url)
    if not csvData:
        return  
    personData = processData(csvData)
    if not personData:
        return  

    while True:
        try:
            user_input = input("Enter an ID to look up (or a number <= 0 to exit): ").strip()
            person_id = int(user_input)

            if person_id <= 0:
                print("Exiting program.")
                break

            displayPerson(person_id, personData)
        except ValueError:
            print("Invalid input. Please enter a valid numerical ID.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
