#!/usr/bin/env python

# Import our facebook python SDK
import facebook
import json # Grab our JSON lib too
import requests
import os
import random
from time import sleep

# Define our Facebook Access Token
access_token = os.getenv('FB_ACCESS_TOKEN')

if not access_token:
    exit("""ERROR!: You must set an access token.
        Try setting the FB_ACCESS_TOKEN environment variable""")

# Define our "thank you" message
thankyou_messages = [
    'Thank you %s!! :D',
    'Thanks so much %s! :)',
    'Thanks a lot %s! :D',
    'Thank you very much %s! :)'
]

# Define our ridiculous "birthday" query
birthday_fql = ("SELECT post_id, actor_id, target_id, created_time, message, comments "
                "FROM stream "
                "WHERE source_id = me() "
                    "AND filter_key = 'others' "
                    "AND created_time > 1401647400"
                    "AND actor_id != me() "
                    "AND comments.count = 0 "
                    "AND comments.can_post = 1 "
                  #  "AND (strpos(message, 'birthday') >= 0 "
                  #      "OR strpos(message, 'Birthday') >= 0 "
                  #      "OR strpos(message, 'happy') >= 0 "
                  #      "OR strpos(message, 'Happy') >= 0) "
                "LIMIT 500")

# Create a new GraphAPI instance with our access token
graph = facebook.GraphAPI(access_token)

# Grab our birthday posts using our FQL query
query_result = graph.get_object('fql', q=birthday_fql)

# Grab the data from the response
birthday_posts = query_result['data']

# Report how many posts we found...
print 'Query returned', len(birthday_posts), 'results'
print

# Create a counter, because why not?
posts_responded_to = 0;

# Let's loop through all of our returned posts
for post in birthday_posts:
    # Grab the post's ID
    post_id = post['post_id']
    r = requests.get('https://graph.facebook.com/%s' % post['actor_id']) 
    user = json.loads(r.text) 

    print user['first_name'], ". ", user['last_name'] ,": ",  post['message']
    
    var = input("Respond? (0/1/2): ")
    if var > 0:
	print 'Posting'	
        # Get a random message from the list
        rand_message = random.choice(thankyou_messages)
	
 	if var is 1:  # Don't include the name
		rand_message = rand_message % ' ' 
        
	if var is 2:  # Include their first name
		rand_message = rand_message % user['first_name'] 
	
	if var is 3: # Enter custom name
		name = raw_input('Enter name: ')
		rand_message = rand_message % name	
	# "Like" the post
    	graph.put_object(post_id, 'likes')

	print rand_message

    	# Post the comment on the post
    	graph.put_object(post_id, 'comments', message=rand_message)

    	# Increment our counter..
    	posts_responded_to += 1

    	# Print to keep track
    	print 'The like/comment should have posted for post', post_id
    else: # 0 - Do not respond
    	print 'Ignoring ', post_id
    # Sleep for a bit to try and keep from getting rate limited
    #sleep(0.1) # Sleep for a tenth of a second

# Let's get this "likes" steez going

# Report how many we've operated on..
print
print 'Responded to', posts_responded_to, 'posts'

# Fin
print 'Done.'
