import requests
from bs4 import BeautifulSoup



url = "https://pythonjobs.github.io/"
page = requests.get(url)


soup = BeautifulSoup(page.content, "html.parser")
#print(soup.prettify())


#---------------------we're narrowing in on the body of the content that we care about 

results = soup.find(class_="job_list")
 

#---------------------this part is to look up the job description itself 

job_elements = results.find_all('h1')
# narrow in on all sections with h1 tag 

for job_element in job_elements:
    desc_element = job_element.find("a")
    # within the <h1> tag, there is another subtag <a> which we want to pull out 
    print(desc_element.text)

#----------------------this part is to look up the location of the job 

location_elements = results.find_all("i", class_="i-globe")
print(location_elements)

# what we did here is narrowed down to the smallest class we could find, and then took the text of the parent 
# we wanted to narrow down to </i> specifically, but why did this not work when we used results.find_all("/i") ??? 

for location_element in location_elements:
    print(location_element.parent.text)

# all locations are found in the <span class="info">

# can we make this even more clever by now prompting us to put in what we want the search keys to be? say you want to search based on 'new york' or 'australia'

desired_location=input("What location do you want to search for? ")

desired_jobs = results.find_all('span')
for desired_job in desired_jobs:
    if desired_location in desired_job.text.lower():
        print(desired_job.text)
        # ok here we printed the desired job's location itself, but instead of the desired location, we want to return the actual job and the entire job description 
        # remember, the desired_job is a TAG. let's see waht happens when we print desired_job.parent.text
        print(desired_job.parent.text)
        # perfect -- this is exactly what we're looking for 

# what was strange about trying to copy/paste the example from the first webscrape was that here the object was not iteratable, why is that the case? 

#------------------====now let's look up if something is part-time or full-time 

duration_elements = results.find_all("i", class_="i-chair")
print(duration_elements)

for duration_element in duration_elements:
    print(duration_element.parent.text)
    
#------------------------ok now that we have some basic functionality of these items, let's come back to this exercise and decide how to search for something specific in the text
# example -- you want to search for the results that are permanent, in New York City, etc. 

# in the earlier example, 

# all job titles on the page are kept within <h2> elements. to filter, you can use string argument
##python_jobs = results.find_all("h2", string=lambda text: "python" in text.lower())

##python_job_elements = [h2_element.parent.parent.parent for h2_element in python_jobs]

