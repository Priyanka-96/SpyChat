#importing packages
import os

from spy_details import *
from steganography.steganography import Steganography
from datetime import datetime
import ntpath



#this function tells if we have added the valid name without numeric and special symbols etc
def name_validation(name):
    name=name.strip()
    name1=name.split(" ")
    a=0
    b=0
    for i in name1:
        if(i.isalpha()):
            a +=1
        else:
            b+=1
    if (b>0):
        return False
    elif(b==0):
        return True

#age validation check
def age_validation(age):
    if age > 12 and age <50:
        return True
    else:
        return False
#friend age validation
def friend_age_validation(age):
    if age > 12:
        return True
    else:
        return False



STATUS_MESSAGE=['busy','Available','Cant talk! message only.']
print 'lets get started with the software of hidding text inside an image'
question=raw_input('do you want to continue as %s %s  ? Y/N'  % (spy.salutation,spy.name))



#now the below function named add_status helps user to add the status or choose the old status

def add_status(current_status_message):

    updated_status_message = None
    if current_status_message != None:
        print 'Your current status message is %s \n' % (current_status_message)
    else:
        print "No current status!"
    que = raw_input("Do you want to select from the older status (y/n)? ")
    if que.upper() == "N":
        new_status_message = raw_input("What status message do you want to set? ")
        if len(new_status_message) > 0:
            STATUS_MESSAGE.append(new_status_message)
            updated_status_message = new_status_message
            print "your new status added is %s"%(updated_status_message)
    elif que.upper() == 'Y':
        item_position = 1
        for message in STATUS_MESSAGE:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1
        message_selection = int(raw_input("\nChoose from the above messages "))
        if len(STATUS_MESSAGE) >= message_selection:
            updated_status_message = STATUS_MESSAGE[message_selection - 1]
            print "current status is %s" % updated_status_message
        else:
            print "You didn't choose the correct status"
    else:
        print 'The option you chose is not valid! Press either Y or N.'
    if current_status_message:
        print 'Your updated status message is: %s' % (current_status_message)
    else:
        print 'You don\'t have any current status update'
    return updated_status_message

# now we are creating a fucntion called add friends with which we can add new friends which whom we want to communicate using hidden msgs.
#the values  will be stored in list created in spy_details file.

def add_friend():
    new_friend = Spy('','',0,0.0)

    new_friend.name = raw_input("Please add your friend's name: ")
    if name_validation(new_friend.name):
        new_friend.salutation= raw_input("What are they? MS. or MR.? ")
        if new_friend.salutation:
            new_friend.name = new_friend.salutation + " " + new_friend.name
            new_friend.age = raw_input("Age?")
            new_friend.age = int(new_friend.age)
            if friend_age_validation(new_friend.age):

                new_friend.rating= raw_input("Spy rating?")
                new_friend.rating = float(new_friend.rating)
                if new_friend.rating >= spy.rating:
                    friends.append(new_friend)
                    print 'Friend Added!'
                else:
                    print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'

            else:
                print "enter valid age of friend"
        else:
            print "write salutation of friend"
    else:
        print "enter valid name of friend!  "

    return len(friends)

#funtion below is used to select the friend with whom we wana send and recieve secret messages

def select_a_friend():
    item_number = 0
    for friend in friends:
        print '%d. %s aged %d with rating %.2f is online' % (item_number +1, friend.name, friend.age,friend.rating)
        item_number = item_number + 1

    friend_choice =( raw_input("Choose from your friends"))
    if len(friend_choice) >0 and friend_choice.isdigit() :
        friend_choice=int(friend_choice)
        if friend_choice>0 and friend_choice< item_number+1:
            friend_choice_position = int(friend_choice) - 1
            return friend_choice_position
        else:
            print "Choose friends between (1 - %d)"%item_number
            return False
    else:
        print "Choose number between (1 - %d)" % item_number
        return False



#below is the function which will help in encoding the message inside an image and sending it to friend choosen using select_a_friend function

def send_message():
    friend_choice = select_a_friend()
    if friend_choice==False:
        print "Try again :("
    else:

        original_image = raw_input("What is the name of the image?")
        if os.path.exists(original_image):
            output_path = "output.jpg"
            text = raw_input("What do you want to say? ")
            if len(text)>0 and text.isspace()==False:
                Steganography.encode(original_image, output_path, text)
                new_chat= Chat(text,True)
                friends[friend_choice].chats.append(new_chat)
                print "Your secret message image is ready!"
            else:
                print "Enter the text which you want to send"
        else:
            print "No such file present!"
#below is fucntion used for reading secret message

def read_message():
    sender = select_a_friend()
    if sender==False:
        print "Try again :("
    else:

        output_path = raw_input("What is the name of the file?")

        if os.path.isfile(output_path)==1:
            secret_text = Steganography.decode(output_path)
            if len(secret_text)>0:
                new_chat= Chat(secret_text,False)
                friends[sender].chats.append(new_chat)
                print "Your secret message has been saved!"
            else:
                print "Enter the message you want to send"
        else :
            print "No such file present !"

#below is the function showing the chats

def read_chat_history():
  read_for = select_a_friend()
  if read_for== False:
      print "Try again :("
  else:

      for chat in friends[read_for].chats:
        if chat.sent_by_me:
          print '[%s] %s %s' % (chat.time.strftime("%d %B %Y"), 'You said:', chat.message)
        else:
          print '[%s] %s said: %s' % (chat.time.strftime("%d %b %y"), friends[read_for].name, chat.message)




#below is a function which will the first one to execute. it contain the menu from where user choose what he want to do in the steganography.


def start_chat(spy):
    current_status_message=None
    spy.name= spy.salutation + " " + spy.name
    if age_validation(spy.age):
        print "Authentication complete. Welcome " + spy.name + " age: " + str(spy.age) + " and rating of: " + str(spy.rating)
        show_menu = True
        while show_menu:
            menu_choices = "What do you want to do? \n 1. Add a status update \n 2. Add a friend \n 3. Send a secret message \n 4. Read a secret message \n 5. Read Chats from a user \n 6. Close Application \n"
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)

                if menu_choice == 1:
                    current_status_message = add_status(current_status_message)
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'Currently You have %d friends' % (number_of_friends)
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                     read_message()
                elif menu_choice ==5:
                     read_chat_history()
                elif menu_choice==6:
                     show_menu = False
                else:
                    print "Please enter a valid number from menu!"

    else:
        print 'Sorry you are not of the correct age to be a spy'


#first code to implement



if question.upper()=='Y':
    start_chat(spy)
elif question.upper()=='N':
   spy =Spy('','',0,0.0)
   name=raw_input("Welcome! write your name!")
   spy.name=name
   if name_validation(spy.name):
       spy.saluation=raw_input("what do we call you 'MS.' or 'MR.' ")
       if spy.salutation:
           spy.name=spy.saluation + " " + spy.name
           spy.age=int(raw_input("whats your age?"))
           if age_validation(spy.age):
               spy.rating=float(raw_input("Whats your rating"))
               spy.is_online=True
               print "sucessfully registered"
               start_chat(spy)
           else:
               print "enter valid age!"
       else:
           print "Enter salutation!"
   else:
       print "enter valid name"
else:
    print "enter either Y or N! "







