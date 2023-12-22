import requests
from bs4 import BeautifulSoup
import pandas as pd

i = 1

# Initialize lists to store data
blog_titles = []
blog_dates = []
blog_image = []
blog_likes_counts = []
#itarating through pages until hits error
while True:
    url = "https://rategain.com/blog/page/" + str(i)
    # header means browsing server header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }

    try:
        if i == 1:
            #for first page url defining
            url = "https://rategain.com/blog/"

        r = requests.get(url, headers=headers)
        r.raise_for_status()
        link = BeautifulSoup(r.text, "lxml") #to get current page data
        next_button = link.find("a", class_="next").get("href") # to get next page button
        blog_posts = link.find_all('body', class_='page-template-default') #targeting each post in page
        # Iterate through each blog post
        for post in blog_posts:
            dates = link.find_all("div", class_="bd-item")  # date tag targeting
            images = link.find_all("div", class_="wrap")  # image url's targeting
            likes = link.find_all("a", class_="zilla-likes") #likes link tag targeting
            titles = link.find_all("div", class_="content") #titles tag targeting

            for k in dates:    #loop for each date
                a_tag = k.find("span").text.strip()
                if "blog" not in a_tag.lower():  # Case-insensitive check
                    blog_dates.append(a_tag)

            for image in images:    #loop for each image
                if image.find("div", class_="img") is not None:
                    img_div = image.find("div", class_="img")
                    if img_div:
                        tag = img_div.find("a")
                        if tag:
                            href_value = tag.get("data-bg")
                            blog_image.append(href_value)
                else:
                    blog_image.append("empty")
            
            for like in likes:  #loop for each likes
                tag = like.find("span").text.strip()
                if tag:
                    blog_likes_counts.append(tag)

            for item in titles: #loop for each titles
                title = item.find("a").text.strip()
                blog_titles.append(title)

        i += 1  # Increment the page number
    #to break code when pages end and results error
    except AttributeError as e:
        break
#sending data to csv format
df = pd.DataFrame({"Title": blog_titles, "Image URL": blog_image, "Date": blog_dates, "Like count": blog_likes_counts})
df.to_csv('Scrapped data.csv', index=False)