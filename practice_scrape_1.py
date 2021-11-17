import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="ResultsContainer")
# you have to define the initial results, because below, the job elements is based on a configuration of the results here 
# the results Container is the section with only the job listings, so you're taking out the header / footer etc. 



job_elements = results.find_all("div", class_="card-content")
# within the results you've siphoned off, there's still a ton of HTML, so now you want to narrow in on the subsections that have an id of class-content 
# how you want to work with the results and select only job postings
   

# can pick out child elements from each posting by doing this below
# within each card-content class, there is an h2, h3, and p. 

for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()

# all job titles on the page are kept within <h2> elements. to filter, you can use string argument
python_jobs = results.find_all("h2", string=lambda text: "python" in text.lower())

python_job_elements = [h2_element.parent.parent.parent for h2_element in python_jobs]

for job_element in python_job_elements:
    links = job_element.find_all("a")
    # start by fetching the <a> elements in a job card, then extract h ref attributes 
    print(type(links))
    # type is a result set, not a result tag 
    for link in links:
        link_url = link["href"]
        print(f"Apply here: {link_url}\n") 

# this will find all H2 elements with string matches Python
# if you were to print this, the console will be empty because you'read
# directly calling this method on your first results variable 