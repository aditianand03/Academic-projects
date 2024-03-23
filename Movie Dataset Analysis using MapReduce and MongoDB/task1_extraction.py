from pymongo import MongoClient



# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["assignment_1"]  # Replace with your database name
collection = db["movies"]  # Replace with your collection name

# Create a text file
with open("year_and_company.txt", "w") as f:
    for doc in collection.find():
        # Split date and extract year
        day, month, year = doc['date'].split(' ')
        
        # Take only the top 3 companies
        companies = doc['companies'][:3]
        
        for company in companies:
            # Extract just the name of the company
            company_name = company['name']
            
            # Write only the year and the name of the company to the file
            f.write(f"{year}\t{company_name}\n")

