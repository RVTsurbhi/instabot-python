#importing libraries
import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from termcolor import colored

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
            print 'username: %s' % colored(user_info['data']['username'], 'red')
            print 'no. of followers: %s' % colored(user_info['data']['counts']['followed_by'], 'red')
            print 'no. of people you are following: %s' % colored(user_info['data']['counts']['follows'], 'red')
            print 'no. of posts: %s' % colored(user_info['data']['counts']['media'], 'red')
            print 'Bio: %s' % colored(user_info['data']['bio'], 'red')
            print 'websites: %s' % colored(user_info['data']['website'], 'red')

        else:
            print colored('user does not exist', 'blue')

    else:
        print ('status code other than 200 received!')

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
        print ('status code other than 200 received', )
        exit()

 #create a function to get the infornation about the user by taking instagram username as its input
#also check that user Id should not be none
def get_user_info(insta_username):
     user_id = get_user_id(insta_username)
     if user_id == None:
         print 'user does not exist!'
         exit()

      #taking the endpoints in the url
     request_url = (base_url + 'users/%s?access_token=%s') % (user_id, my_token)
     print 'GET request url : %s' % (request_url)
     user_info = requests.get(request_url).json()

     #from the received response we can fetch the data about the user like no. of followers, following and post
     if user_info['meta']['code']== 200:
         if len(user_info['data']):
             print 'username: %s' % colored(user_info['data']['username'], 'green')
             print 'fullname: %s' % colored(user_info['data']['full_name'], 'green')
             print 'no. of followers: %s' % colored(user_info['data']['counts']['followed_by'], 'green')
             print 'no. of people following: %s' % colored(user_info['data']['counts']['follows'], 'green')
             print 'no. of posts: %s' % colored(user_info['data']['counts']['media'], 'green')
             print 'BIO: %s' % colored(user_info['data']['bio'], 'green')
             print 'websites: %s' % colored(user_info['data']['website'], 'green')
         else:
             print colored('there is no data available for this user', 'blue')

     else:
         print 'status code other than 200 received'


#declare a function to check our own recent post
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
            print colored('image has been downloaded', 'red')
        else:
            print colored('post does not exist', 'blue')

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
            print colored('image has been downloaded', 'blue')
        else:
            print colored('there is no recent post', 'red')
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
            print colored('there is no recent post of the user', 'green')

    else:
        print 'status code other than 200 received'

        exit()

#declaring the function to get the list of likes on a post
def get_likes_list(insta_username):
    media_id = get_post_id(insta_username)
    if media_id == None:
        print 'invalid media id'
        exit()
     #taking the endpoints for get request
    request_url = (base_url + 'media/%s/likes?access_token=%s') % (media_id, my_token)
    print 'GET request url: %s' % (request_url)
    likes_list = requests.get(request_url).json()

     #check the status code, if comes 200 then show the people who likes the post
    if likes_list['meta']['code'] == 200:
        if len(likes_list['data']):
            print 'people who likes this post'
            for i in range(len(likes_list['data'])):
                print colored('likes : ' + likes_list['data'][i]['username'], 'blue')
        else:
            print colored('no likes on the post', 'red')

    else:
        print 'status code other than 200'


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
        print colored('you successfully like the post!', 'red')

    else:
        print colored('your like was unsuccessful. try again!', 'blue')


#function declaration to get the recent media liked by the user.
def recent_media():
    #including the endpoints to get the url
    basic_url = (base_url + 'users/self/media/liked?access_token=%s') % (my_token)
    print 'GET request url: %s' % (basic_url)
    liked_recent_media = requests.get(basic_url).json()

    #check the status code, if comes 200 then show the list of recent post liked by us
    if liked_recent_media['meta']['code'] == 200:
        if len(liked_recent_media['data']):
            for x in range(len(liked_recent_media['data'])):
                print 'recent posts liked by you : %s ' % colored(liked_recent_media['data'][x]['id'], 'red')

        else:
            print colored('recently you liked no posts', 'blue')

    else:
        print 'status code other than 200'


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
            print colored("No comments on this post", 'red')
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
        print colored('your new comment is added successfully!', 'blue')
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
                        print colored('successfully deleted the comment!', 'green')
                    else:
                        print 'unable to delete the comment!'

                 #if the intent of comment is positive then print the comment
                else:
                    print 'positive comment :%s' % (comment_text)

        else:
            print colored('there are no existing comments on the post', 'blue')
    else:
        print 'status code other than 200'




 #options available -what you want to do with the access token
def start_bot():
     while True:
         print '\n'
         print colored('hello, welcome to instabot!', 'green')
         print colored('your menu options are as follows:', 'green')

         print "1.get your own details\n"
         print "2.get details of a user by username\n"
         print "3.get your own recent post\n"
         print "4.get the recent post of the user by username\n"
         print "5.get the list of likes\n"
         print "6.like the recent post of the user\n"
         print "7.make a comment on the recent post of the user\n"
         print "8.getting the list of comments\n"
         print "9.delete negative comment from the post\n"
         print "10.get the recent media liked by user\n"


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
             get_likes_list(insta_username)
         elif choice == "6":
             insta_username = raw_input("enter the username : ")
             like_post(insta_username)
         elif choice == "7":
             insta_username = raw_input("enter the username : ")
             get_comments_list(insta_username)
         elif choice == "8":
             insta_username = raw_input("enter the username : ")
             post_a_comment(insta_username)
         elif choice == "9":
             insta_username = raw_input("enter the username : ")
             del_neg_comments(insta_username)
         elif choice == "10":
            recent_media()

         elif choice == "x":
             exit()

         else:
            print 'invalid choice'

#calling the main function
start_bot()

#users in the sanbox mode
# 1. rvt_surbhi
# 2. mudrasrivastava
# 3. indian.bloke
# 4. amitrawat5188
# 5. dil_bole_aggarwals








