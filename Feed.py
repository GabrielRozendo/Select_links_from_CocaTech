import  feedparser
import time

url='http://feeds.cocatech.com.br/cocatechpodcast'
feed = feedparser.parse(url)
#print(feed['feed']['title'])

#
# function to get the current time
#
current_time_millis = lambda: int(round(time.time() * 1000))
current_timestamp = current_time_millis()

posts_to_print = []
posts_to_skip = []
posts_apps = []
posts_news = []

for post in feed.entries:
    title = post.title
    tags = post.tags
    if 'news' in tags:
        posts_news.append(title)
    elif 'apps' in tags:
        posts_apps.append(title)
    
    link = post.link
    data = post.published
    #print(title)
    #if post_is_in_db_with_old_timestamp(title):
        #posts_to_skip.append(title)
    #else:
    posts_to_print.append(title)
    
print("------------NEWS---------------------\n")
for post in posts_news:
    print(post + "|" + str(current_timestamp) + "\n")
    print("\n" + time.strftime("%a, %b %d %I:%M %p"))
    print("-----------------------------------------\n")

print("------------APPS---------------------\n")
for post in posts_apps:
    print(post + "|" + str(current_timestamp) + "\n")
    print("\n" + time.strftime("%a, %b %d %I:%M %p"))
    print("-----------------------------------------\n")        

for post in posts_to_print:
    print(post + "|" + str(current_timestamp) + "\n")
    print("\n" + time.strftime("%a, %b %d %I:%M %p"))
    print("-----------------------------------------\n")
        