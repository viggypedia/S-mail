import datetime
import pymysql



#****************************************************************************************************************
#
# Function: User Registration
# Description: This function is to register new users into the SMAIL system
#               takes input from the user and validates for duplicates and
#                creates new users into the system
#****************************************************************************************************************


def user_registration():
    usr_cnt=0
    print ('WELCOME, we are glad that you are interested in our application')
    name = input('Enter your name:')
    flag=1
    while (flag!=0):
        user_ID=input('Please Enter an User ID :')

        # Check if user already exists

        user_cnt=check_user_exist(user_ID)
            
        if(user_cnt== -1):
            print('Üser Id already Exists.Choose another')
                          
        elif(user_cnt==0):
            con1=input('Confirm User id: ' )
           
            while (flag!=0):
                if user_ID!=con1:
                    print ('Reconfirm UserID ')
                    con1=input('Reconfirm UserID=')
                elif (user_ID==con1):
                  #  print ("Inside equal")
                    flag=0
                    
        
    user_ID=user_ID+'@smail.com'

    dob=(input('Enter Date of birth Format YYYY/MM/DD'))
    Alt_emailId= input ("Please provide an alternate id :" )   
    sex=input('Gender (if Press M for MALE, F for FEMALE and O for Others :')        
    User_type="U"
    status='U'
        
    print ('Now this is the most important as you are going to fill the password , remember it as you would not be able to access it later')
    passwd=input('Enter Password :')
    con2=input ('Confirm Password:')

    while True:
        if (passwd != con2):
            print ('Passwords do not match')
            print ('Please re enter the password correctly ')
            con2=input('confirm your password=')
        elif (passwd==con2):
            break

    register_new_user(user_ID,name, dob,Alt_emailId,sex,passwd,User_type)


#****************************************************************************************************************
#
# Function: Adding New user into database
# Description: This function is used to connect to the database and creates new users into the database
#
#
#****************************************************************************************************************

def register_new_user(user_id,user_name,dob,alt_email,sex,passwd,user_type):
             
    # connecting mysql to python 
    mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
    mycur=mydb.cursor()

    status="U"
    
    sql = "INSERT INTO user_info  (id,name,dob,alternate_id,gender,passwd,user_type, status) VALUES (%s ,%s,%s,%s,%s,%s,%s,%s)"

    val= (user_id,user_name, dob,alt_email,sex,passwd,user_type, status)

    mycur.execute(sql,val)
    
    mydb.commit()

    print("Üser Registered Successfully")
    mydb.close()

#****************************************************************************************************************
#
# Function: Validating user logging 
# Description: This function is used to check and validate user logging into the system
#
#
#****************************************************************************************************************
def validate_status(user_id):
    mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
    mycur=mydb.cursor(pymysql.cursors.DictCursor)
    sql=("select status from user_info where id="+"'"+user_id+"@smail.com'")
    mycur.execute(sql)
    row1=mycur.fetchall()

    x=str(row1[0])      
    row=str(x[12:13])

    if (row=='U'):
        return(0)
    elif(row=='S'):
        return(-1)
    elif(row=='D'):
        return(-2)

def validate_login(user_id,pwd):

 # connecting mysql to python 
    mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
    mycur=mydb.cursor()
    get_status=validate_status(user_id)
    if(get_status==-1 or get_status==-2):
        print('Account Suspended or Deleted')
    elif(get_status==0):
        sql=("select id,passwd from user_info where id="+"'"+user_id+"@smail.com' and passwd="+"'"+pwd+"'")
        mycur.execute(sql)
        mycur.fetchall()
        cnt=mycur.rowcount
        mydb.close();
        if(cnt==1):
            return 0
        else:
            return -1

#****************************************************************************************************************
#
# Function: Check for User existence 
# Description: This function is used to check if the user already exists in the system and to prevent duplicate user registrations
#
#
#****************************************************************************************************************
def check_user_exist(user_id):
    mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
    mycur=mydb.cursor()

    sql="select id from user_info where id="+"'"+user_id+"@smail.com'"
    #print(sql)
    mycur.execute(sql)
    mycur.fetchall()
    cnt=mycur.rowcount

    if(cnt==0):
        return 0
    else:
        return -1

        
#****************************************************************************************************************
#
# Function: Viewing Mail box of a user
# Description: This function is used to view th email box of the user
#
#
#****************************************************************************************************************
def view_inbox(user_id):
  # connecting mysql to python 
    mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
    mycur=mydb.cursor()
    receiver_id=user_id
    sql="select sender_id,sub,body, receiver_id, attachment,date from mail_box where receiver_id="+"'"+user_id+"@smail.com'"
    #print(sql)
    mycur.execute(sql)
    myresult=mycur.fetchall()
    cnt=mycur.rowcount
    #print(cnt)
    if (cnt==0):
        print("No records Exist!!")
    else:
       # print ('Listing Mails')
        print("--------------------------------------------------------------------------------------------------------------------")
        print("Sender Id\t\t Subject\t\tBody\t\t Receiver Id\t\t Attachment\t\tDate")
        print("--------------------------------------------------------------------------------------------------------------------")
        for x in myresult:
            print (x)

        
#****************************************************************************************************************
#
# Function: Viewing Outbox of a user
# Description: This function is used to view th email box of the user
#
#
#****************************************************************************************************************

def view_outbox(user_id):
  # connecting mysql to python 
    mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
    mycur=mydb.cursor()
   # receiver_id=user_id
    sql="select sender_id,sub,body, receiver_id, attachment,date from mail_box where sender_id="+"'"+user_id+"'"
#    print(sql)
    mycur.execute(sql)
    myresult=mycur.fetchall()
    cnt=mycur.rowcount
 #   print(cnt)
    if (cnt==0):
        print("No records Exist!!")
    else:
       # print ('Listing Mails')
        print("--------------------------------------------------------------------------------------------------------------------")
        print("Sender Id\t\t Subject\t\tBody\t\t Receiver Id\t\t Attachment\t\tDate")
        print("--------------------------------------------------------------------------------------------------------------------")
        for x in myresult:
            print (x)


                    
#****************************************************************************************************************
#
# Function: Compose New Mail
# Description: This function is used to compose new mails
#
#
#****************************************************************************************************************

          
def compose_mail (user_id):
    to=input("To :")
    user_id=user_id+'@smail.com'
    sub=input("Subject :")
    body=input("Mail Body: ( upto to 200 words):-")
    d=str(datetime.datetime.today())
    
    mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
    mycur=mydb.cursor()
    sql='insert into mail_box (sender_id,date,sub, body, receiver_id) values(%s,%s,%s,%s,%s)'
    mycur.execute(sql,(user_id, d,sub,body,to))
    mydb.commit()
    print ('Your mail has been sent')
    mydb.close()


                    
#****************************************************************************************************************
#
# Function: Search from existing mails in the Mail box
# Description: This function is search from existing mails
#             This search is based on the search criterion chosen by the user.
#             This function allows the user to search based on (a)email id of the sender, (b)date and (c)search based on keywords from body or from subject 
#
#
#****************************************************************************************************************


def search_mail(user_id):
    mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
    mycur=mydb.cursor()
    print('TO SEARCH MAIL SELECT DO THE FOLLOWING')
    print('ENTER 1 TO SEARCH BY ID')
    print('ENTER 2 TO SEARCH BY DATE(DATE FORMAT=YYYY-MM-DD)')
    print('ENTER 3 TO SEARCH BY BODY CONTENT')
    c=int(input('ENTER YOUE CHOICE:-'))
    while True:
        if c==1:
            s=input('Sender ID:-')
            sql="select sender_id, sub,body,receiver_id, attachment,date from  mail_box where receiver_id="+"'"+ user_id+ "@smail.com'"+ " and sender_id = %s"
            mycur.execute(sql,s)
            break
        elif c==2:
            s=input('Chose DATE :-')
            sql="select sender_id, sub,body,receiver_id, attachment,date from  mail_box where receiver_id="+"'"+ user_id+ "@smail.com'"+ " and date = %s"
            mycur.execute(sql,s)
            break
        elif c==3:
            s=input('ENTER Keyword for Search:-')
            symbol="%"
            sql="select sender_id, sub,body,receiver_id, attachment,date from  mail_box where receiver_id="+"'"+ user_id+ "@smail.com'"+ " and sub like '"+symbol+ s + symbol+" ' or body like '"+ symbol+ s + symbol+ "'"
            mycur.execute(sql)
            break
        else:
            print('PLEASE ENTER A VALID OPTION')
            search_mail(user_id)
         
    #print(mycur._last_executed)
    myresult=mycur.fetchall()
    cnt=mycur.rowcount
    print(cnt)
    if (cnt==0):
        print("No records Exist!!")
    else:
        #print ('Listing Mails')
        print("--------------------------------------------------------------------------------------------------------------------")
        print("Sender Id\t\t Subject\t\tBody\t\t Receiver Id\t\t Attachment\t\tDate")
        print("--------------------------------------------------------------------------------------------------------------------")
        for x in myresult:
            print (x)
          
    mydb.close()

                    
#****************************************************************************************************************
#
# Function: Delete from existing mails in the Mail box
# Description: This function is Delete from existing mails based on the search criterion chosen by the user.
#             This function allows the user to search based on (a)email id of the sender, (b)date and (c)search based on keywords from body or from subject 
#
#
#****************************************************************************************************************
          
def del_msg (user_id):
     mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
     mycur=mydb.cursor()
     print('TO SEARCH MAIL SELECT DO THE FOLLOWING')
     print('ENTER 1 TO DELETE BY ID')
     print('ENTER 2 TO DELETE BY DATE(DATE FORMAT=YYYY-MM-DD)')
     print('ENTER 3 TO DELETE BY BODY CONTENT')
     c=int(input('ENTER YOUE CHOICE:-'))
     while True:
         if c==1:
             s=input('Sender ID:-')
             sql="delete from  mail_box where receiver_id="+"'"+ user_id+ "@smail.com'"+ " and sender_id = %s"
             mycur.execute(sql,s)
             mydb.commit()
             mydb.close()
      
             print('THE MAIL IS DELETED SUCCESFULLY')
             break
         elif c==2:
             s=input('Choose DATE :-')
             sql="delete from  mail_box where receiver_id="+"'"+ user_id+ "@smail.com'"+ " and date = %s"
             mycur.execute(sql,s)
             print('THE MAIL IS DELETED SUCCESFULLY')
             mydb.commit()
             mydb.close()
     
             break
         elif c==3:
             s=input('ENTER Keyword to delete:-')
             symbol="%"
             sql="delete from  mail_box where receiver_id="+"'"+ user_id+ "@smail.com'"+ " and sub like '"+symbol+ s + symbol+" ' or body like '"+ symbol+ s + symbol+ "'"
             mycur.execute(sql)
             print('THE MAIL IS DELETED SUCCESFULLY')
             mydb.commit()
             mydb.close()
     
             break
         else:
             print('PLEASE ENTER A VALID OPTION')
             del_msg(user_id)

                   
#****************************************************************************************************************
#
# Function: Delete Account of a selected User
# Description: This function is Delete a particular as selected
#
#****************************************************************************************************************
 
def del_user ():
    user_id=input('Enter User Id you want to Delete')
    user_cnt=validate_status(user_id)
   # print(user_cnt)
    if (user_cnt==0 or user_cnt==-1):
        a=input('Are you sure . Do you want to delete your account(Y/N)')

        if (a=='Y'):
            mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
            mycur=mydb.cursor()
##            sql1=('delete from mail_box where receiver_id='+a + "@smail.com'")
##            mycur.execute(sql1)
            status='D'
            sql2=("update user_info set status='"+status+"' where id='"+user_id+ "@smail.com'")
  #          print(sql2)
            mycur.execute(sql2)
           
            mydb.commit()
            mydb.close()
            print("User Deleted Successfully !!!")
    elif (user_cnt==-2):
        print("Account Already Deleted")

                  
#****************************************************************************************************************
#
# Function: Suspend Account of a selected User
# Description: This function is to suspend a particular account as selected
#
#****************************************************************************************************************
   
def suspend_user ():
    mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
    mycur=mydb.cursor()
           
    user_id=input('Enter User Id you want to suspend')
    user_cnt=validate_status(user_id)
    print(user_cnt)
    if(user_cnt==0):
        a=input('Are you sure . Do you want to suspend this account(Y/N)')
    
        if (a=='Y' or a=='ý'):
            sql2=("update user_info set status='"+'S'+"' where id='"+user_id+ "@smail.com'")
 #           print(sql2)
            mycur.execute(sql2)
            mydb.commit()
            mydb.close()
            print("Account Suspended Successfully !!!")   
    elif(user_cnt==-1 or user_cnt==-2):
        print("Account Alredy Deleted or Suspended")

                 
#****************************************************************************************************************
#
# Function: ReActivate A Suspend Account of a selected User
# Description: This function is to Reactivate a suspended account #
#
#****************************************************************************************************************
 
def release_supension_user ():
    user_id=input('Enter User Id you want to Reactivate')
    user_cnt=validate_status(user_id)
    if(user_cnt==-1):
        a=input('Are you sure . Do you want Reactivate this account(Y/N)')
    
        if (a=='Y'):
            mydb=pymysql.connect(host="localhost",user="root",passwd="root123",database= "email")
            mycur=mydb.cursor()
            
            sql2=("update user_info set status='"+'U'+"' where id='"+user_id+ "@smail.com'")
            mycur.execute(sql2)
           
            mydb.commit()
            mydb.close()
            print("Account Restored Successfully !!!")
    elif (user_cnt==0):
        print("Account is Already Active")
    elif (user_cnt==-2):
            print("Account is Already Deleted")
