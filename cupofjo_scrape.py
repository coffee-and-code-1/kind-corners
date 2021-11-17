import requests
from bs4 import BeautifulSoup

url = "https://cupofjo.com/"
page = requests.get(url)


soup = BeautifulSoup(page.content, "html.parser")
#print(soup.prettify())


# in this first exercise, we're going to study the website to see where the content we want to narrow in on is located
# in the future, it owuld be ideal if there's a way to search the entire body for the text more quickly (without needing to narrow down) 

results = soup.find("div",class_="most-pop-slider")
# we'll slide into the "most popular" content here to make it easy and do a quick skim if there's kindness trending here 

article_titles = results.find_all("h2")
# narrow in on h2 tags which is where the name of the articles are located 

## -------(optional)------- use this if you want to print a list of articles 
#for article_title in article_titles:
    #print(article_title.text)
        
# now let's look to how we can pull the exact url associated with the article 
# in cup of jo, it's the 'a' within the h2. you already found h2 -- article_titles, so now you want to find the a. 

#for article_title in article_titles:
    # for each of the titles, find the link which can be found at "a" 
    #links = article_title.find_all("a")
    # when you do .find(a) it yields a result tag, when you do .find_all(a) it yields a result set, why is that? 
    #for link in links:
        #link_url = link["href"]
        #print(f"The article can be directly found at: {link_url}\n") 
        # what is the purpose of the f? if you take it out, then it will print out the literal {link_url} words. if you put 'f' back in, it will substitute the actual link

# now that we have the right syntax to pull the url to the story, let's find a way to search the articles for specific key words 

desired_word = input("What word do you want to search the articles for? ")

for article_title in article_titles:
    if desired_word in article_title.text.lower():
        desired_article = article_title
        desired_article_text = desired_article.text
        print(desired_article_text)
        link = desired_article.find("a")
        # in this case you did not need to use find_all because there is only one instance of it. 
        link_url = link["href"]
        print(f"This article can be directly found at: {link_url}\n")
        # this will give us the title of the article 
        # now let's pull the URL for it 
        # remember, we are at the level of "article_title" 
        
# then finally, we want to complete this scrape by saying something like 
# 'The article, "[article_title]", focusing on [desired_word] is trending on [URL -- cup of jo]. The original story can be found here at [URL -- not cup of jo]'

print(f"We think that based on your keyword '{desired_word}', you would enjoy the article, {desired_article_text}, that is currently trending on {url}. The original story can be found at {link_url}")
