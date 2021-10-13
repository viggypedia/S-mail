import datetime
import pymysql
import new_email_mod as m1
import kivy
from kivy.app import App
from kivy.uix.label import Label

# connecting mysql to python 
mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
mycur=mydb.cursor()
# collecting user info
choice=0
#ENTRY TEXT
while (choice!=6):
    print('********************************************************************************************', end="\n")
    print('Welcome to SMAIL... STUDENT MAILING SYSTEM', end="\n")
    print('********************************************************************************************', end="\n")
    print('New Users Press 1 to Register', end="\n")
    print('Existing Users Press 2 to Login', end="\n")
    print('Press 3 to Delete Current account', end="\n")
    print('Press 4 to Suspend account', end="\n")
    print('Press 5 to Reactivate ACcount',end="\n")
    print('Press 6 to Exit')
    choice=int(input('Enter Your Choice: '))
    print('********************************************************************************************', end="\n")

    if (choice==1):
        # Calling User Registration 
        m1.user_registration()          
    elif(choice==2): # Existing User- for Logging in to the system
        user_id=input('Please Enter an User ID :')
        pwd=input( "Enter your Password:")
        #Validate User Login
        s=m1.validate_login(user_id,pwd)
        if(s==-1):
            print("User id or Password mismatch")
            break
        elif(s==0):
            print('********************************************************************************************', end="\n")
            print(user_id+'  You have logged in Successfully into Smail', end="\n")
            print('********************************************************************************************', end="\n")
            choice2=0
            while(choice2!=6):
                print('********************************************************************************************', end="\n")  

                print('Press 1 - View Inbox', end="\n")
                print('Press 2 - View Outbox', end="\n")
                print('Press 3 - Compose Mail', end="\n")
                print('Press 4 - Search Mail', end="\n")
                print('Press 5 - Delete Mail', end="\n")
                print('Press 6 - Go Back to Main Menu', end="\n")
                
                choice1=int(input('Enter Your Choice: '))   
                print('********************************************************************************************', end="\n")
                if (choice1==1): #View Inbox
                    m1.view_inbox(user_id)

                elif (choice1==2): # View Outbox
                    m1.view_outbox(user_id)
                    
                elif (choice1==3): # Composing Mails
                    m1.compose_mail(user_id)
                          
                elif (choice1==4): # Searching Mails
                    m1.search_mail(user_id)
                    
                elif (choice1==5): # Deleting Mails
                      print("Delete Mails")
                      m1.del_msg(user_id)
                else:
                    break
             
    elif(choice==3): # Deleting Existing Account
        m1.del_user()
           
    elif(choice==4):  #Suspending Existing Account
        m1.suspend_user()
        
    elif(choice==5):    #Account Reactivation
        m1.release_supension_user()
        
    elif(choice==6):  #Exit from Syem 
        print("Thank You for Using SMAIL \n ....Exiting Smail...........................")

 
