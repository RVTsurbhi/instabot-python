#importing libraries
import requests
import urllib

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
             print 'no. of followers: %s' % (user_info['data']['counts']['followed_by'])
             print 'no. of people following: %s' % (user_info['data']['counts']['follows'])
             print 'no. of posts: %s' % (user_info['data']['counts']['media'])
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


 #options available -what you want to do with the access token
def start_bot():
     while True:
         print '\n'
         print 'hello, welcome to instabot!'
         print 'your menu options are as follows:'
         print "a.get your own details\n"
         print "b.get details of a user by username\n"
         print "c.get your own recent post\n"
         print "d.get the recent post of the user by username\n"
         print 'x.EXIT'

         choice = raw_input("enter your choice: ")
         if choice == "a":
             self_info()
         elif choice== "b":
             insta_username = raw_input('enter the username of the user: ')
             get_user_info(insta_username)
         elif choice == "c":
             get_own_post()
         elif choice == "d":
             insta_username = raw_input("enter the username of the user: ")
             get_users_post(insta_username)

         elif choice == "x":
             exit()

         else:
            print 'invalid choice'

start_bot()










