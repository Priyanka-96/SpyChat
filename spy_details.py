from datetime import datetime

class Spy:

    def __init__(self, name, salutation, age, rating):
        self.name = name
        self.salutation = salutation
        self.age = age
        self.rating = rating
        self.is_online = True
        self.chats = []
        self.current_status_message = None


class Chat:
    def __init__(self,message,sent_by_me):
        self.message= message
        self.time=datetime.now()
        self.sent_by_me= sent_by_me



spy = Spy('priyanka verma', 'Miss.', 20, 4.7)

friend_one = Spy('Simran', 'Miss.',  21,4.9)
friend_two = Spy('Isha kansal', 'Miss.', 20,5)
friend_three = Spy('Saksham mahajan', 'Mr.' ,19,5.1)


friends = [friend_one, friend_two, friend_three]

