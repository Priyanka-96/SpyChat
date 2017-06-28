#importing packages

import os
from spy_details import *
from steganography.steganography import Steganography
from datetime import datetime
import ntpath
from termcolor import colored



#this function tells if we have added the valid name without numeric and special symbols
def name_validation(name):
    name=name.strip()    #strip() returns a copy of the string in which all chars have been stripped from the beginning and the end of the string
    name1=name.split(" ")  #spilt the string wherever we confront any space in string
    a=0
    b=0
    for i in name1: #checking i in list name1
        if(i.isalpha()):  #isalpha means the name1 should contain only alphabets
            a +=1
        else:
            b+=1
    if (b>0):
        return False  #false when there is number or any special char in name1
    elif(b==0):
        return True #true means there is no number or special char in name1


#this fucntion check the validity of spy age
def age_validation(age):
    if age > 12 and age <50: #age of spy should be in between 12 and 50
        return True     #if conditon statisfied return TRUE
    else:
        return False  #return false if no condition satisfied


#function for checking age of friend
def friend_age_validation(age):
    if age > 12: #age of added friend should be greater than 12
        return True     #if conditon statisfied return TRUE
    else:
        return False       #return false if no condition satisfied


#It checks the rating of spy and print the particular message corresponding rating
def spy_rating_check(rating):

    if (rating >5):   #if rating greater than 5 then this spy should not be accepted
        print colored("Enter rating between 1-5","red")
        return None
    elif (rating >4.5 and rating <=5):      #if rating between 4.5 and 5 print specific messgae
        print colored("You are the best spy","green")
        return rating           #returning the rating of spy
    elif(rating>4 and rating<=4.5):          #if rating between 4 and 4.5 print specific messgae
        print colored("You are a great spy","green")
        return rating        #returning the rating of spy
    elif (rating >3.5 and rating<=4):       #if rating between 3.5 and 4 print specific messgae
        print colored("You are a good spy","green")
        return rating        #returning the rating of spy
    elif (rating >3 and rating<=3.5):       #if rating between 3 and 3.5 print specific messgae
        print colored("You are a average spy","green")
        return rating        #returning the rating of spy
    elif(rating>2.5 and rating<=3):     #if rating between 2.5 and 3 print specific messgae
        print colored("You can a improve yourself","green")
        return rating        #returning the rating of spy
    elif(rating>=1 and rating <=2.5):       #if rating between 1.5 and 2.5 print specific messgae
        print colored("try to work on your skills","green")
        return rating         #returning the rating of spy



#fucntion getting the details of new spy
def details():
    spy = Spy('', '', 0, 0.0)       #object of Spy class created in spy_details.py file
    name = raw_input("Welcome! write your name!")
    spy.name = name
    if name_validation(spy.name):       #calling name_validation function to check if the entered name is valid or not
        spy.salutation = raw_input("what do we call you 'MS.' or 'MR.' or 'DR.' or 'ER.'or 'MRS.'")
        list = ["DR.", "MR.", "MS.","ER.","MRS."]       #storing salutations for spy

        if spy.salutation.upper() in list:        #checking if the entered salutation lies in list or not
            spy.name = spy.salutation + " " + spy.name
            spy.age = int(raw_input("whats your age?"))
            if age_validation(spy.age):     #calling age validation functiion n see if correct age is entered or not
                print colored("NOTE :) THE RATING SHOULD BE IN BETWEEN 1-5 ", "blue")
                spy.rating = float(raw_input("Whats your rating?"))
                rate = spy_rating_check(spy.rating)         #calling spy_rating_check method to see if rating in between 1-5
                if rate == None:                #rate not valid then error print
                    print colored("Try again!:(","red")
                else:
                    spy.is_online = True
                    print colored("Sucessfully registered", "green")
                    start_chat(spy)                      #authorization complete n now spy cn go to start_chat functiion
            else:
                print colored("enter valid age!", "red")
                start()             #when age not valid calling start function n asking if you want to continue with old spy

        else:
            print colored("Enter valid salutation!", 'red')
            start()      #when salutation not valid calling start function n asking if you want to continue with old spy

    else:
        print colored("enter valid name", "red")
        start()      #when name not valid calling start function n asking if you want to continue with old spy



#the below function named add_status helps user to add the status or choose the old status
def add_status(current_status_message):

    updated_status_message = None
    if current_status_message != None:
        print colored('Your current status message is %s \n',"green") % (current_status_message)   #if there is current_status_mesggage present then print the status
    else:
        print colored("No current status!","red")       #this print when no current status
    que = raw_input("Do you want to select from the older status (y/n)? ")   #ask if spy want to update the old status or addd  new status
    if que.upper() == "N":      #execute if spy enter "N"
        new_status_message = raw_input("What status message do you want to set? ") #take new status as input from spy
        if len(new_status_message) > 0:     #check if length of new status is more than 0
            STATUS_MESSAGE.append(new_status_message)
            updated_status_message = new_status_message     #updating the status message
            print "your new status added is %s"%(updated_status_message)        #print new status
    elif que.upper() == 'Y':         #execute if spy enter "Y" that is spy want to get old status as updated current status
        item_position = 1
        for message in STATUS_MESSAGE:  #checks the message status_message list
            print '%d. %s' % (item_position, message)       #print old status in list
            item_position = item_position + 1
        message_selection = int(raw_input("\nChoose from the above messages "))
        if len(STATUS_MESSAGE) >= message_selection:        #true if length of list is greater than the mesggae selected by the spy
            updated_status_message = STATUS_MESSAGE[message_selection - 1]
            print colored("current status is %s","green") % updated_status_message  #status updated
        else:
            print colored("You didn't choose the correct status","red")
    else:
        print colored('The option you chose is not valid! Press either Y or N.',"red")
    if current_status_message:          #check if curren message is true
        print colored('Your updated status message is: %s',"green") % (current_status_message)  #print updated message
    else:
        print colored('You don\'t have any current status update',"red")
    return updated_status_message     #return updated_status_messgae



# now we are creating a fucntion called add friends with which we can add new friends which whom we want to communicate using hidden msgs.
#the values  will be stored in list created in spy_details file.
def add_friend():
    new_friend = Spy('','',0,0.0)       #object of Spy class created in spy_details.py file

    new_friend.name = raw_input("Please add your friend's name: ")
    if name_validation(new_friend.name):        #calling name_validation function to check if the entered name is valid or not
        new_friend.salutation= raw_input("What are they? MS. or MR. or DR. or ER. or MRS.? ")
        list = ["DR.", "MR.", "MS.","ER.","MRS."]       #storing salutations for friend

        if new_friend.salutation.upper() in list:       #checking if the entered salutation lies in list or not
            new_friend.name = new_friend.salutation + " " + new_friend.name
            new_friend.age = raw_input("Age?")
            new_friend.age = int(new_friend.age)
            if friend_age_validation(new_friend.age):       #calling friend age validation functiion n see if correct age is entered or not
                print "friend rating should be greater than spy rating"
                new_friend.rating= raw_input("Spy's Friend rating?")
                new_friend.rating = float(new_friend.rating)
                rate = spy_rating_check(new_friend.rating)            #calling spy_rating_check method to see if rating in between 1-5
                if rate == None:
                    print colored("Try again!:(","red")

                else:
                    if new_friend.rating >= spy.rating :            #if rating of friend added is more than rating of spy only  then the friend should be accepted
                        friends.append(new_friend)      #append the new friend in friends list created in spy_details
                        print colored('Friend Added!',"green")
                    else:
                        print colored('Sorry! Invalid entry. We can\'t add spy with the details you provided',"red")   #print when details of friend is not correct

            else:
                print colored("enter valid age of friend","red")   #print when age of friend is not correct
        else:
            print colored("write salutation of friend","red")        #print when salutation of friend is not in list
    else:
        print colored("enter valid name of friend!  ","red")         #print when name of friend is not correct

    return len(friends)         #returning the no of friends in friend list



#funtion below is used to select the friend with whom you wannna send and recieve secret messages
def select_a_friend():
    item_number = 0
    for friend in friends:      #fetching friends from friends list created in spy_details
        print '%d. %s aged %d with rating %.2f is online' % (item_number +1, friend.name, friend.age,friend.rating)
        item_number = item_number + 1

    friend_choice =( raw_input("Choose from your friends"))
    if len(friend_choice) >0 and friend_choice.isdigit() :      #check if the length if friend choosen is greater than zero and it should be digit
        friend_choice=int(friend_choice)            #converting string to int
        if friend_choice>0 and friend_choice< item_number+1:        #check if the choosen friend lie in the list
            friend_choice_position = int(friend_choice) - 1         #index of friend_choice stored in friend_choice_position
            return friend_choice_position       #returned index
        else:
            print "Choose friends between (1 - %d)"%item_number #tells that the friend choosen should be in between range
            return None
    else:
        print "Choose number between (1 - %d)" % item_number    #tells that the friend choosen should be in between range
        return None



#below is the function which will help in encoding the message inside an image and sending it to friend choosen using select_a_friend function
def send_message():
    friend_choice = select_a_friend()       #calling the select_a_friend() fucntion and getting the choosen friend
    if friend_choice==None:  #if wrong friend choosen then display try again
        print "Try again :("
    else:       #if correct friend choosen then else part run of this function

        original_image = raw_input("What is the name of the image?")     #ask name of file
        if os.path.exists(original_image):  #if file exist in os then true
            output_path = "output.jpg"      #giving the path to encoded image
            text = raw_input("What do you want to say? ")   #getting msg to be send
            list=['SOS','SAVE ME','HELP ME!']   #creating list for emergency msgs
            if text in list:    #check if text entered is in list
                text= colored("Its an emergency.Reach me as soon as possible","red")
                Steganography.encode(original_image, output_path, text)     #encoding the image with text
            if len(text)>0 and len(text)<100 and text.isspace()==False:  #check if len of text between 1 to 100 and it shouldnt be only spaces
                Steganography.encode(original_image, output_path, text)  #encoding the image with text
                new_chat= Chat(text,True)       #calling Chat class
                friends[friend_choice].chats.append(new_chat)  #appending in chats in friends list
                print "Your secret message image is ready!"
            else:
                if len(text)>100:  #check if spy is talkitive by seeing if he speak more tha 100 words
                    print colored(" You are speaking alot! We are removing you from chat list","red")
                    del(friends[friend_choice])     #delete the garrulous friend
        else:
            print colored("No such file present!","red")        #print when file name dont exist



#below is fucntion used for reading secret message
def read_message():
    sender = select_a_friend()      #calling the select_a_friend() fucntion and getting the choosen friend
    if sender==None:
        print "Try again :("        #if wrong friend choosen then display try again
    else:           #if correct friend choosen then else part run of this function

        output_path = raw_input("What is the name of the file?")     #ask name of file

        if os.path.isfile(output_path)==1:   #if given name is file in os then true
            secret_text = Steganography.decode(output_path)  #decode the txt from image
            if len(secret_text)>0:      #if there is secret msg in image only then this if true
                new_chat= Chat(secret_text,False)   #Chat class called and secret text stored
                friends[sender].chats.append(new_chat)      #append the message
                words = secret_text.split(" ")
                num=len(words)
                print num
                print colored("Your secret message has been saved!","green")    #print when msg saved
            else:
                print colored("there is no secret message in this image","red") #print when len of secret msg < 0
        else :
            print colored("No such file present !","red")   #print when no file present  by the name given by spy


#below is the function showing the history of chats
def read_chat_history():
  read_for = select_a_friend()      #calling the select_a_friend() fucntion and getting the choosen friend
  if read_for== None:
      print "Try again :("          #if wrong friend choosen then display try again
  else:             #if correct friend choosen then else part run of this function
    if len(friends[read_for].chats)>0:      #will work if there is any message in chats
      for chat in friends[read_for].chats:      #fetcing chats from friends
        if chat.sent_by_me:         #check if send_by_me is true
          print colored('[%s] %s %s',"blue") % (chat.time.strftime("%d %B %Y"), colored('You said:','red'), chat.message)     #printing time and chat emssage send by you
        else:       #check if send_by_me is tru
          print colored('[%s] %s said: %s','blue') % (chat.time.strftime("%d %B %Y"), colored(friends[read_for].name,"red"), chat.message)      #printing time and chat emssage send by spy



#below is a function which iontain the menu from where user choose what he want to do in chatting app.
def start_chat(spy):
    current_status_message=None
    spy.name= spy.salutation + " " + spy.name  #concating the name of spy and its salutation into name
    if age_validation(spy.age):  #age_validation fucntion is called to see id spy age is valid or not
        print "Authentication complete. Welcome " + spy.name + " age: " + str(spy.age) + " and rating of: " + str(spy.rating)  #printing welcome message
        show_menu = True  #taking a variable and setting it to true
        while show_menu:
            #putting the menu item which we want to use in chatApp
            menu_choices = "What do you want to do? \n 1. Add a status update \n 2. Add a friend \n 3. Send a secret message \n 4. Read a secret message \n 5. Read Chats from a user \n 6. Close Application \n "
            #letting spy decide which menu item to choose
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:        #if len of menu choice is greater than 0 then only it will work
                menu_choice = int(menu_choice)      #converting the menu choice to int

                if menu_choice == 1:        #if menu choice is 1 then spy will be able to add or update status
                    current_status_message = add_status(current_status_message)  #calling add_status function and adding or updating a status
                elif menu_choice == 2:            #if menu choice is 2 then spy will be able to add new friends
                    number_of_friends = add_friend()      #calling the add_friend() function and storing the no od freinds returned by function
                    print 'Currently You have %d friends' % (number_of_friends)     #prining no of friends
                elif menu_choice == 3:        #if menu choice is 3 then spy will be able to send encoded message
                    send_message()          #calling send_message() function
                elif menu_choice == 4:    #if menu choice is 4 then spy will be able to decrypt and read the encoded message
                     read_message()     #calling read_message() function
                elif menu_choice ==5:    #if menu choice is 5 then spy will be able to read chat history
                     read_chat_history()        #calling read_chat_history() fucntion
                elif menu_choice==6:          #if menu choice is 1 then spy will be able to exit application
                     show_menu = False          #changing the value of show_menu from True to False
                else:
                    print colored("Please enter a valid number from menu!","red")       #enter valid choice of menu

    else:
        print colored('Sorry you are not of the correct age to be a spy',"red")  #enter correct age


#function which will ask if you want to continue with the same name or you want new spy to acess thhis chatting app
def start():
    question = raw_input('do you want to continue as %s %s  ? Y/N' % (spy.salutation, spy.name))  #asking if spy want to continue or he want to add new spy?
    if question.upper()=='Y':
        start_chat(spy)  #if spy want to continue then start_chat() function will be called to show menu of chatApp

    elif question.upper()=='N':
        details()       #if spy want to add new spy the details() is called and details of new spy is input in that function
    else:
        print colored("enter either Y or N! ","red")  #if spy enter anything except Y or N then it print this



STATUS_MESSAGE=['busy','Available','Cant talk! message only.']          #listing containing initial status messages
print colored('lets get started with the software of hidding text inside an image',"green")
start()  #calling start function









