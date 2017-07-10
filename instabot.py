#importing libraries
import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#acessing app token and store it in a variable
my_token = '4408952527.60abb0c.8a35373099984d50aa35a93d64317764'
#store base url in a variable
base_url = 'https://api.instagram.com/v1/'

#declaring the function to get our own information
def self_info():
   #using endpoint documentation get the url
    request_url = (base_url + 'users/self/?access_token=%s') % (my_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

     #to know about the no. of followers, following, posts, bio, & website from the received data
     # but first we have to check if the status code is 200 or not
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'username: %s' %(user_info['data']['username'])
            print 'no. of followers: %s' %(user_info['data']['counts']['followed_by'])
            print 'no. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'no. of posts: %s' % (user_info['data']['counts']['media'])
            print 'Bio: %s' % (user_info['data']['bio'])
            print 'websites: %s' % (user_info['data']['website'])

        else:
            print 'user does not exist'

    else:
        print 'status code other than 200 received!'

#create a function to get the ID of the user by username

def get_user_id(insta_username):

    #through endpoints get the url
    request_url = (base_url + 'users/search?q=%s&access_token=%s') % (insta_username, my_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    #to check if the user we searched does exist or not
    #but first check the status code to be 200 , if yes then fetch the data
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None

    else:
        print 'status code other than 200 received'
        exit()

 #create a function to get the infornation about the user by taking instagram username as its input
#also check that user Id should not be none
def get_user_info(insta_username):
     user_id = get_user_id(insta_username)
     if user_id == None:
         print 'user does not exist!'
         exit()
     #user_info = requests.get((base_url + 'users/%s?&access_token=%s') % (user_id, my_token)).json()

     request_url = (base_url + 'users/%s?access_token=%s') % (user_id, my_token)
     print 'GET request url : %s' % (request_url)
     user_info = requests.get(request_url).json()

     #from the received response we can fetch the data about the user like no. of followers, following and post
     if user_info['meta']['code']== 200:
         if len(user_info['data']):
             print 'username: %s' % (user_info['data']['username'])
             print 'fullname: %s' % (user_info['data']['full_name'])
             print 'no. of followers: %s' % (user_info['data']['counts']['followed_by'])
             print 'no. of people following: %s' % (user_info['data']['counts']['follows'])
             print 'no. of posts: %s' % (user_info['data']['counts']['media'])
             print 'BIO: %s' % (user_info['data']['bio'])
         else:
             print 'there is no data available for this user'

     else:
         print 'status code other than 200 received'


#define a function to check or own recent post
def get_own_post():
    request_url = (base_url + 'users/self/media/recent/?access_token=%s') % (my_token)
    print 'GET request url: %s' % (request_url)
    own_media = requests.get(request_url).json()

    #to check the status code of the get request
    if own_media['meta']['code']== 200:
        if len(own_media['data']) :
            image_name = own_media['data'][0]['id'] + 'owner.jpg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print 'image has been downloaded'
        else:
            print 'post does not exist'

    else:
        print 'status code other than 200 received'



#define a function to check the the recent post of the user by username
def get_users_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'user does not exist!'
        exit()
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, my_token)
    print 'GET request url : %s' %(request_url)
    user_media = requests.get(request_url).json()

    #to check the status code
    #urllib library helps to fetch the data
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id']+ 'pic.jpg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print 'image has been downloaded'
        else:
            print 'there is no recent post'
    else:
        print 'status code other than 200 received'


#declare a function to get the Id of the recent post of the user
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'user does not exist!'
        exit()
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, my_token)
    print 'GET request url: %s' % (request_url)
    user_media = requests.get(request_url).json()

    #check the status code
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'ther is no recent post of the user'

    else:
        print 'status code other than 200 received'

        exit()

#defining function to like the post of the user
#access token is sent in payload to make post request (to like the post)
def like_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (base_url + 'media/%s/likes') % (media_id)
    payload ={"access_token": my_token}
    print 'POST request url: %s' % (request_url)
    post_a_like = requests.post(request_url,payload).json()

    #to check if like was successful by checking the status code
    if post_a_like['meta']['code'] == 200:
        print 'the like was successful'

    else:
        print 'your like was unsuccessful. try again!'

#declaring the function to get the list of comments on the post
def get_comments_list(insta_username):
    media_id = get_post_id(insta_username)
    if media_id is None:
        print "There is no media"
    else:
        request_url = base_url + "media/%s/comments/?access_token=%s" % (media_id, my_token)
        print "Get request url:%s" % request_url
        comment_list = requests.get(request_url).json()

     #check the status code, if comes 200 then show the list of comments
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            print "The comments on the post :"
            for x in range(len(comment_list['data'])):
                comment_text= comment_list['data'][x]['text']
                print "comment: %s" % (comment_text)

        else:
            print "No comments on this post"
    else:
        print "Status code other than 200"

#defining function to post a comment on the recent post of the user
def post_a_comment(insta_username):
    # call the function get_post_id to get the id of the post in which we need to make a comment
    media_id = get_post_id(insta_username)
    #use the media-id to make a post request. payload will consists of the access token and the comment to be added
    comment_text = raw_input("your comment: ")
    payload = {"access_token": my_token,"text": comment_text}
    request_url = (base_url + 'media/%s/comments') % (media_id)
    print 'POST request url: %s'% (request_url)

    make_comment = requests.post(request_url,payload).json()

    #to check if comment was successful or not, while checking the status code
    if make_comment['meta']['code'] == 200:
        print 'your new comment is added successfully!'
    else:
        print 'unable to add the comment. Try Again!'

#declaring the function to delete the negative comments from the users post

def del_neg_comments(inst_username):
    media_id = get_post_id(inst_username)
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, my_token)
    print 'GET request url: %s' %(request_url)
    comment_info = requests.get(request_url).json()

    # check the status code, if comes 200 then proceed
    if comment_info['meta']['code']== 200:
        if len(comment_info['data']):

            # the naive implementation tells us how to delete the negative comment
            for x in range(0,len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                # implementing sentiment analysis using TextBlob library
                blob = TextBlob(comment_text, analyzer= NaiveBayesAnalyzer())

                #check the intent of positivity and negativity in the comments through sentiments
                #if the intent of the negative comment is greater then function will make a delete call to delete the comment
                if(blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'NEGATIVE comment :%s' % (comment_text)
                    #to delete the comment using the endpoints
                    delete_url = (base_url + 'media/%s/comments/%s/?access_token=%s') % (media_id,comment_id,my_token)
                    print 'DELETE request url :%s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    #check if the status code is 200 then, then show the success of deleting the comment
                    if delete_info['meta']['code'] == 200:
                        print 'successfully deleted the comment!'
                    else:
                        print 'unable to delete the comment!'

                 #if the intent of comment is positive then print the comment
                else:
                    print 'positive comment :%s' % (comment_text)

        else:
            print 'there are no existing comments on the post'
    else:
        print 'status code other than 200'



 #options available -what you want to do with the access token
def start_bot():
     while True:
         print '\n'
         print 'hello, welcome to instabot!'
         print 'your menu options are as follows:'
         print "1.get your own details\n"
         print "2.get details of a user by username\n"
         print "3.get your own recent post\n"
         print "4.get the recent post of the user by username\n"
         print "5.like the recent post of the user\n"
         print "6.make a comment on the recent post of the user\n"
         print "7.delete negative comment from the post\n"
         print "8.getting the list of comments\n"

         print 'x.EXIT'

         choice = raw_input("enter your choice: ")
         if choice == "1":
             self_info()
         elif choice== "2":
             insta_username = raw_input("enter the username: ")
             get_user_info(insta_username)
         elif choice == "3":
             get_own_post()
         elif choice == "4":
             insta_username = raw_input("enter the username : ")
             get_users_post(insta_username)
         elif choice == "5":
             insta_username = raw_input("enter the username : ")
             like_post(insta_username)
         elif choice == "6":
             insta_username = raw_input("enter the username : ")
             post_a_comment(insta_username)
         elif choice == "7":
             insta_username = raw_input("enter the username : ")
             del_neg_comments(insta_username)
         elif choice == "8":
             insta_username = raw_input("enter the username : ")
             get_comments_list(insta_username)


         elif choice == "x":
             exit()

         else:
            print 'invalid choice'

start_bot()










