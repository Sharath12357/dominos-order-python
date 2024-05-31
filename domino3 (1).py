import sqlite3
conn=sqlite3.connect('Dom.db')
b=conn.cursor()
#b.execute('create table Domuser(name char,phno number,email char)')
#print('completed')
#b.execute('create table cart(phno number,cartvalues char)')

d={
    'veg':{'margerita':129,'cheese_and_corn':169,'peppi panner':260,'veg_loaded':210,'tomato_tangi':170},
    'non_veg':{'pepper_barbeque':199,'non_veg_loaded':169,'chicken_sausage':200},
    'snacks':{'garlic_bread':120,'zingy':59,'c_cheese_balls':170},
    'desserts':{'choco_lava':100,'mousse_cake':169},
    'drinks':{'coke':90,'pepsi':78,'sprite':50}
}

login_status=False
cart={}
pnum=''
mode=0

def valid_phno(phno):
    s=str(phno)
    return len(s)==10 and '6'<=s[0]<='9' and s.isnumeric()

def check_phno(phno):
    l=list(b.execute('select phno from Domuser'))
    return (phno,)in l

def valid_email(e):
    s=e[-10:]
    return s in ['@gmail.com','@yahoo.com'] and 'a'<=e[0]<='z' and e[0:-10].isalnum()

def check_email(e):
    l=list(b.execute('select email from Domuser'))
    return(e,)in l

def Dominos():
    print('enter 1: signup')
    print('enter 2: login')
    ch=int(input('enter your choice:'))
    if ch==1:
        while True:
            print('please fill details')
            name=input('enter name:')
            while True:
                phno=int(input('enter phno:'))
                if valid_phno(phno):
                    break
                else:
                    print('invalid phno')
            while True:
                email=input('enter email:')
                if valid_email(email):
                    break
                else:
                    print('invalid email')
            m,n=check_email(email),check_phno(phno)
            if m==False and n==False:
                b.execute(f'insert into Domuser values("{name}","{phno}","{email}")')
                conn.commit()
                print('signup successful')
                break
            elif m==True:
                print('email already exists')
            else:
                print('phno already exists')
    else:
        login()
def get_otp(a):
    global login_status
    import random
    while True:
        otp=random.randint(100000,999999)
        print('your otp is:',otp)
        print('an otp has sent to ur',a)
        tp=int(input('enter OTP:'))
        if tp==otp:
            print('logged in successfully')
            login_status=True
            break
        else:
            print('incorrect OTP')

def login():
    global pnum,login_status
    if login_status==True:
        return 'already logged in'
    print('enter 1:login with phno')
    print('enter 2:login with email')
    c=int(input('enter your choice:'))
    if c==1:
        pnum=int(input('enter phno:'))
        if check_phno(pnum):
            get_otp(pnum)
        else:
            print('phno doesnt exist')
    else:
        email=input('enter email:')
        pnum=list(b.execute(f'select phno from Domusers where email="{email}"'))[0][0]
        if check_email(email):
            get_otp(email)
        else:
            print('email doesnt exist')
def logout():
    global login_status
    login_status=False
    print('logged out successfully')
def order(new=0):
    global mode
    if login_status==True:
        print('enter 1:dine in')
        print('enter 2:take away')
        print('enter 3:home delivery')
        ch=int(input('enter choice:'))
        mode=ch
        out={}
        di=list(d)
        while True:
            print('enter 1:veg')
            print('enter 2:non-veg')
            print('enter 3:snacks')
            print('enter 4:desserts')
            print('enter 5:drinks')
            print('enter 6:end')
            c=int(input('enter your item:'))
            if 1<=c<=6:
                if c==6:
                    break
                m=list(d)[c-1]
                m=list(d[m])
                for i in range(1,len(m)+1):
                    print(f'enter {i}:{m[i-1]}')
                choice=int(input('enter choice:'))
                q=int(input('enter quantity:'))
                if 1<=choice<=len(m):
                    out[m[choice-1]]=[q,q*d[di[c-1]][m[choice-1]]]
                    print('item added')
                else:
                    print('invalid choice')
            else:
                print('invalid choice')
        cart.update(out)
        if cart!={} and new==0:
            b.execute(f'insert into cart values("{pnum}","{cart}")')
            conn.commit
    else:
        print('login required')

def disp_bill():
    if login_status==True:
        if mode==1:
            total_amt=0
        elif mode==2:
            print('parcel charges of 25rs. will be included')
            total_amt=25
        elif mode==3:
            print('parcel charges of 25rs and delivery chanrges of 50rs. will be included')
            total_amt=75
        print('item','quantity','price')
        for i in cart:
            print(i,' '*(20-len(i)),cart[i][0],cart[i][1])
            total_amt+=cart[i][1]
    
        print('total bill:',total_amt)
    else:
        print('login is required')
        
    

















