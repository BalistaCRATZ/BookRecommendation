import pandas as pd
import requests
import csv
import requests
import xml.etree.ElementTree as ET

class Recommender():
    
    def __init__(self):
        
        self.tag_names = {}
        self.books = {}
        self.tags_to_remove = ["30574", "8717", "11557", "5207", "22743", "22753", "4949", "11590", "17213", "18045", "30521", "10197", "10210", "20849", "15169", "32586"]

    def load_data(self):
    
        print("Loading data...")
        
        #Loading the names and ids of the tags
        with open("C:/Users/Sunaabh/.spyder-py3/Books/tags.csv", encoding="utf-8") as f:
            
            reader = csv.DictReader(f)
            
            for row in reader:
                
                if row["tag_id"] not in self.tags_to_remove:
                
                    self.tag_names[row["tag_id"]] = row["tag_name"]
        
        #Loading info about the books
        with open("C:/Users/Sunaabh/.spyder-py3/Books/books.csv", encoding="utf=8") as f:
            
            reader = csv.DictReader(f)
            
            for row in reader:
                
                self.books[row["goodreads_book_id"]] = {"title": row["title"], 
                                                    "author": row["authors"],
                                                    "year": row["original_publication_year"],
                                                    "isbn": row["isbn"],
                                                    "tags": {}}
        #Loading the tags for each book
        with open("C:/Users/Sunaabh/.spyder-py3/Books/book_tags.csv", encoding="utf-8") as f:
            
            reader = csv.DictReader(f)
            
            for row in reader:
                
                if row["tag_id"] not in self.tags_to_remove:
                
                    self.books[row["goodreads_book_id"]]["tags"][row["tag_id"]] = row["count"]
            
        
        print("Data loaded.")
    
    def get_score(self, tags, sample_tags):
    
        score = 0
        
        for tag in tags:
            
            if tag in sample_tags:
                
                score += 1
        
        return score
    
    def get_recommendation(self, book_id):
    
        score = 0
        res_book_id = None
        
        #Check first tag in book
        
        master_key = next(iter(self.books[book_id]["tags"]))
        
        #Loop through all books with first tag being same, and calculate score
        
        for book in self.books:
            
            key = next(iter(self.books[book]["tags"]))
            
            if key == master_key:
                
                v = self.get_score(self.books[book]["tags"], self.books[book_id]["tags"])
                    
                if v > score and book != book_id:
                    
                    score = v
                    res_book_id = book
                
                else:
                    
                    pass
              
        return res_book_id

def main():
    
    recommender = Recommender()
    
    key = "76XbzJQBNBFcQZHH2IVeaA"
    
    recommender.load_data()

    book_name = input("Enter name of book you would like a recommendation for: ")
    
    url = f"https://www.goodreads.com/search/index.xml?key={key}&q={book_name}"
    response = requests.get(url).text
    
    tree = ET.fromstring(response)
    
    book_id = tree.findall("./search/results/work/best_book/id")[0].text
    
    res_id = recommender.get_recommendation(book_id)
    
    title = recommender.books[res_id]["title"]
    author = recommender.books[res_id]["author"]
    
    print(f"You might like {title} by {author}")

main()
    