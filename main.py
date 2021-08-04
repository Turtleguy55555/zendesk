import json
import requests





#headers = {
#    'Content-Type': 'application/json',
#}

#data = open('tickets.json')
#r = requests.post('https://zccstudent.zendesk.com/api/v2/imports/tickets/create_many.json', headers=headers, data=data, auth=('david021301@gmail.com', 'Asmallturtle123!'))

def isPrev(page):
    if page > 1:
        return True
    else:
        return False
def isNext(page,count):
    maxPage = count/25
    if maxPage > page:
        return True
    return False

def authorize(user,password):
    try:
        r = requests.get('https://zccstudent.zendesk.com/api/v2/tickets.json', auth = (user, password))
        if r.status_code == 200:
            return 0
        else:
            return 1
    except Exception:
        return 2



def count(user,password):
    if(authorize(user,password) == 0):
        count = requests.get('https://zccstudent.zendesk.com/api/v2/tickets/count.json', auth=(user, password))
        count_json = count.json()
        return count_json["count"]["value"]

def isTicket(id,tiks_left,curr):
    if (tiks_left >= 25):
        flag = False
        for i in range(25):

            if curr["tickets"][i]["id"] == id:
                flag = True
                break
        if flag == True:
            return True


        else:
            return False
    else:
        flag = False
        for i in range(tiks_left):
            if curr["tickets"][i]["id"] == id:
                flag = True
                break
        if flag == True:
            return True
        else:
            return False

if __name__ == '__main__':
    user = ''
    password = ''
    while(True):
        print("Welcome to my ticket viewer. Enter your username and password.\n")
        user = input("Username: ")
        password = input("Password: ")
        if(authorize(user,password) == 0):
            break
        if (authorize(user, password) == 2):
            print("Couldn't connect to zendesk")
        else:
            print("Incorrect username or password.")
    while(True):
        print("Type c to see the current number of tickets\nType v to view all tickets\n Type q to exit")
        inputer = input("Enter command: ")
        if(inputer == "q"):
            print("Exiting the ticket viewer. Good bye.")
            break
        if(inputer == "c"):
            print("Current number of tickets: " , count(user,password))
            print()
        elif(inputer == "v"):



            count = requests.get('https://zccstudent.zendesk.com/api/v2/tickets/count.json',
                                 auth=(user, password))
            count_json = count.json()
            tiks_left = int(count_json["count"]["value"])
            allTic = requests.get('https://zccstudent.zendesk.com/api/v2/tickets.json?page[size]=25', auth=(user, password))
            allTic_json = allTic.json()
            if(tiks_left >= 25):
                for i in range(25):
                    print("Subject:", allTic_json["tickets"][i]["subject"], " ", "Id: ", allTic_json["tickets"][i]["id"])
            else:
                for i in range(tiks_left):
                    print("Subject:", allTic_json["tickets"][i]["subject"], " ", "Id: ", allTic_json["tickets"][i]["id"])
            curr = allTic_json
            page = 1
            while(True):
                print()
                inp = input('Type next to go to next page\nType prev to go to previous page\nType v, space, then a valid id number to view details of a certain ticket\nType q to go back to menu: ')
                if(inp == "next"):
                    #n = requests.get('https://zccstudent.zendesk.com/api/v2/tickets.json?page[size]=', auth=('david021301@gmail.com', 'Asmallturtle123!'))

                    next_json = curr
                    #print(curr)
                    if curr["meta"]["has_more"] == True and isNext(page,count_json["count"]["value"]) == True:
                        page+= 1
                        tiks_left -= 25
                        #n = requests.get('https://zccstudent.zendesk.com/api/v2/tickets.json?page%5Bafter%5D=eyJvIjoibmljZV9pZCIsInYiOiJhWWdBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=100',
                                     #auth=('david021301@gmail.com', 'Asmallturtle123!'))

                        c = requests.get(next_json["links"]["next"],
                                     auth=(user, password))

                        curr = c.json()

                        #print(curr[0])
                        if tiks_left >= 25:
                            for i in range(25):
                                print("Subject:", curr["tickets"][i]["subject"], " ", "Id: ",
                                      curr["tickets"][i]["id"])
                        else:
                            for i in range(tiks_left):
                                print("Subject:", curr["tickets"][i]["subject"], " ", "Id: ",
                                      curr["tickets"][i]["id"])
                    else:
                        print("no next page")



                elif(inp == "prev"):
                    next_json = curr
                    #print(curr)
                    if isPrev(page) == True:
                        tiks_left +=25
                        # n = requests.get('https://zccstudent.zendesk.com/api/v2/tickets.json?page%5Bafter%5D=eyJvIjoibmljZV9pZCIsInYiOiJhWWdBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=100',
                        # auth=('david021301@gmail.com', 'Asmallturtle123!'))

                        c = requests.get(next_json["links"]["prev"],
                                         auth=(user, password))

                        curr = c.json()
                        if tiks_left >= 25:
                            for i in range(25):
                                print("Subject:", curr["tickets"][i]["subject"], " ", "Id: ",
                                      curr["tickets"][i]["id"])
                        else:
                            for i in range(tiks_left):
                                print("Subject:", curr["tickets"][i]["subject"], " ", "Id: ",
                                      curr["tickets"][i]["id"])
                        page -=1
                    else:
                        print("No previous page")
                elif(inp == "q"):
                    print()
                    break
                elif(inp[0:2] == "v "):
                    try:
                        id = int(inp[2:])

                        index = -1
                        if (tiks_left >= 25):
                            flag = False
                            for i in range(25):

                                if curr["tickets"][i]["id"] == id:
                                    index = i
                                    flag = True
                                    break
                            if flag == True:
                                print()
                                print("Ticket details: ")
                                print("Subject: ", curr["tickets"][index]["subject"])
                                print("Id: ", curr["tickets"][index]["id"])
                                print("Created at: ", curr["tickets"][index]["created_at"])
                                print("Description: ", curr["tickets"][index]["description"])


                            else:
                                print("Invalid id. Id doesn't exist in this page of entries")
                        else:
                            flag = False
                            for i in range(tiks_left):
                                if curr["tickets"][i]["id"] == id:
                                    index = i
                                    flag = True
                                    break
                            if flag == True:
                                print()
                                print("Ticket details: ")
                                print("Subject: ", curr["tickets"][index]["subject"])
                                print("Id: ", curr["tickets"][index]["id"])
                                print("Created at: ", curr["tickets"][index]["created_at"])
                                print("Description: ", curr["tickets"][index]["description"])
                            else:
                                print("Invalid id. Id doesn't exist in this page of entries")
                    except ValueError:
                        print("Error: Id must be an integer")
                else:
                    print("invalid command")
        else:
            print("invalid command")
