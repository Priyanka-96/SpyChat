#importing packages
import os

from spy_details import *
from steganography.steganography import Steganography
from datetime import datetime
import ntpath
from termcolor import colored



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

#spy ratinG
def spy_rating_check(rating):

    if (rating >5):
        print colored("Enter rating between 1-5","red")
        return None
    elif (rating >4.5 and rating <=5):
        print colored("You are the best spy","green")
        return rating
    elif(rating>4 and rating<=4.5):
        print colored("You are a great spy","green")
        return rating
    elif (rating >3.5 and rating<=4):
        print colored("You are a good spy","green")
        return rating
    elif (rating >3 and rating<=3.5):
        print colored("You are a average spy","green")
        return rating
    elif(rating>2.5 and rating<=3):
        print colored("You can a improve yourself","green")
        return rating
    elif(rating>=1 and rating <=2.5):
        print colored("try to work on your skills","green")









#now the below function named add_status helps user to add the status or choose the old status

def add_status(current_status_message):

    updated_status_message = None
    if current_status_message != None:
        print colored('Your current status message is %s \n',"green") % (current_status_message)
    else:
        print colored("No current status!","red")
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
            print colored("current status is %s","green") % updated_status_message
        else:
            print colored("You didn't choose the correct status","red")
    else:
        print colored('The option you chose is not valid! Press either Y or N.',"red")
    if current_status_message:
        print colored('Your updated status message is: %s',"green") % (current_status_message)
    else:
        print colored('You don\'t have any current status update',"red")
    return updated_status_message

# now we are creating a fucntion called add friends with which we can add new friends which whom we want to communicate using hidden msgs.
#the values  will be stored in list created in spy_details file.

def add_friend():
    new_friend = Spy('','',0,0.0)

    new_friend.name = raw_input("Please add your friend's name: ")
    if name_validation(new_friend.name):
        new_friend.salutation= raw_input("What are they? MS. or MR. or DR.? ")
        list = ["DR.", "MR.", "MS."]

        if new_friend.salutation in list:
            new_friend.name = new_friend.salutation + " " + new_friend.name
            new_friend.age = raw_input("Age?")
            new_friend.age = int(new_friend.age)
            if friend_age_validation(new_friend.age):
                print "friend rating should be greater than spy rating"
                new_friend.rating= raw_input("Spy's Friend rating?")
                new_friend.rating = float(new_friend.rating)
                rate = spy_rating_check(new_friend.rating)
                if rate == None:
                    print "Try again!:("

                else:
                    if new_friend.rating >= spy.rating :
                        friends.append(new_friend)
                        print colored('Friend Added!',"green")
                    else:
                        print colored('Sorry! Invalid entry. We can\'t add spy with the details you provided',"red")

            else:
                print colored("enter valid age of friend","red")
        else:
            print colored("write salutation of friend","red")
    else:
        print colored("enter valid name of friend!  ","red")

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
            return None
    else:
        print "Choose number between (1 - %d)" % item_number
        return None



#below is the function which will help in encoding the message inside an image and sending it to friend choosen using select_a_friend function

def send_message():
    friend_choice = select_a_friend()
    if friend_choice==None:
        print "Try again :("
    else:

        original_image = raw_input("What is the name of the image?")
        if os.path.exists(original_image):
            output_path = "output.jpg"
            text = raw_input("What do you want to say? ")
            list=['SOS','SAVE ME']
            if text in list:
                text= colored("Its an emergency.HELP ME","red")
                Steganography.encode(original_image, output_path, text)
            if len(text)>0 and len(text)<100 and text.isspace()==False:
                Steganography.encode(original_image, output_path, text)
                new_chat= Chat(text,True)
                friends[friend_choice].chats.append(new_chat)
                print "Your secret message image is ready!"
            else:
                if len(text)>100:
                    print colored(" You are speaking alot! We are removing you from chat list","red")
                    del(friends[friend_choice])
        else:
            print colored("No such file present!","red")
#below is fucntion used for reading secret message

def read_message():
    sender = select_a_friend()
    if sender==None:
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
                print colored("there is no secret message in this image","red")
        else :
            print colored("No such file present !","red")

#below is the function showing the chats

def read_chat_history():
  read_for = select_a_friend()
  if read_for== None:
      print "Try again :("
  else:
    if len(friends[read_for].chats)>0:
      for chat in friends[read_for].chats:
        if chat.sent_by_me:
          print colored('[%s] %s %s',"blue") % (chat.time.strftime("%d %B %Y"), colored('You said:','red'), chat.message)
        else:
          print colored('[%s] %s said: %s','blue') % (chat.time.strftime("%d %B %Y"), colored(friends[read_for].name,"red"), chat.message)





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
                    print colored("Please enter a valid number from menu!","red")

    else:
        print colored('Sorry you are not of the correct age to be a spy',"red")


#first code to implement


STATUS_MESSAGE=['busy','Available','Cant talk! message only.']
print 'lets get started with the software of hidding text inside an image'


valid = True
while valid:

    question = raw_input('do you want to continue as %s %s  ? Y/N' % (spy.salutation, spy.name))
    if question.upper()=='Y':
        valid=False
        start_chat(spy)

    elif question.upper()=='N':
       valid=False
       spy =Spy('','',0,0.0)
       name=raw_input("Welcome! write your name!")
       spy.name=name
       if name_validation(spy.name):
           spy.salutation=raw_input("what do we call you 'MS.' or 'MR.' or 'DR.'")
           list=["DR.","MR.","MS."]

           if spy.salutation in list:
               spy.name=spy.salutation + " " + spy.name
               spy.age=int(raw_input("whats your age?"))
               if age_validation(spy.age):
                   print colored("The rating should be in 1-5","red")
                   spy.rating=float(raw_input("Whats your rating"))
                   rate = spy_rating_check(spy.rating)
                   if rate == None:
                       print "Try again!:("
                   else:
                       spy.is_online=True
                       print colored("sucessfully registered","green")
                       start_chat(spy)
               else:
                   print colored("enter valid age!","red")
           else:
               print colored("Enter valid salutation!",'red')
       else:
           print colored("enter valid name","red")
    else:
        print colored("enter either Y or N! ","red")







