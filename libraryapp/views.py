
from datetime import date
import os
from . import forms,models
from django.contrib.auth.models import User
from libraryapp.forms import categoryform, userform
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from libraryapp.models import Usermember,Category,book,requestbook,issuebook
from django.contrib.auth.decorators import login_required

# Create your views here.
def load_home(request):
    return render(request,'home.html')

def load_signup(request):
    return render(request,'signup.html')

def load_signin(request):
    return render(request,'signin.html')

def load_login(request):
    form=userform()
    return render(request,'login.html',{'form':form})


def load_adminhome(request):
    if not request.user.is_staff:
        return redirect('load_login')
    return render(request,'admin/adminhome.html')

@login_required(login_url='login')
def load_category(request):
    form=categoryform()
    return render(request,'admin/category.html',{'form':form})  


def addcategory(request):
    print("kuiiii")
    if request.method=='POST':
        form=categoryform(request.POST)
        if form.is_valid():
            form.save()
            print("helloooo")
            return redirect('load_adminhome')
    form=categoryform()
    return render(request,'admin/category.html',{'form':form})

def viewcategory(request):
    if not request.user.is_staff:
        return redirect('load_login')
    catgry=models.Category.objects.all()
    return render(request,'admin/viewcategory.html',{'catgry':catgry})   

def load_book(request):
    categorys=Category.objects.all()
    
    context={'categorys':categorys}
    return render(request,'admin/addbook.html',context)   

def userhomepage(request):
    return render(request,'userhome.html')

def signup(request):
    if request.method =='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        email=request.POST.get('email')
        uname=request.POST.get('uname')
        pswd=request.POST.get('pswd')
        cfpswd=request.POST.get('cfpswd')
        gender=request.POST.get('gender')
        des=request.POST.get('designation')
        
        if request.FILES.get('file') is not None:
            photo=request.FILES.get('file')
        else:
            photo="/static/images/default.png"
            
        if cfpswd==pswd:
            if User.objects.filter(username=uname).exists():
                
                print("username not available")
                messages.info(request, 'Username not available..' )
                return redirect('signup')

                      
            

            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=pswd,email=email)
                user.save()
                u=User.objects.get(id=user.id)
                member=Usermember(user_address=address,user_gender=gender,user_mobile=mobile,user_designation=des,user=u,user_photo=photo)
                member.save()
                return redirect('load_home')
    return render(request,'signup.html')


def userlogin(request):
    if request.method=='POST':
        try:
            username=request.POST['uname']
            password=request.POST['pswd']
            user=auth.authenticate(username=username,password=password)
            request.session["uid"]=user.id
            if user is not None:
                if user.is_staff:
                    login(request,user)
                    print('hi')
                    messages.success(request,f'Welcome.. { username }')
                    return redirect('load_adminhome')
                else: 
                    login(request,user)
                    auth.login(request,user)
                    messages.success(request,f'Hii.. { username }')
                    
                    print("logged in")
                    return redirect('userhomepage')
               
            else:
                messages.success(request,'Invalid username or password')
                print("invalid username")
                return redirect(request,'userlogin')
        except:

            messages.info(request,'Invalid username or password')
            return render(request,'signin.html')

    else:
        return render(request,'login.html')


def user_logout(request):
    request.session['uid']=""
    auth.logout(request)
    return redirect('load_home')


def viewuser(request):
    if not request.user.is_staff:
        return redirect('load_login')
    user=Usermember.objects.all()  
    return render(request,'admin/userview.html',{'user':user})


@login_required(login_url='login')
def add_book(request):
    if request.method=='POST':
        bname=request.POST['bname']
        des=request.POST['description']
        author=request.POST['author']
        publication=request.POST['publication']
        price=request.POST['price']
        quantity=request.POST['quantity']
        sel1=request.POST['select']
        cat1=Category.objects.get(id=sel1)
        if request.FILES.get('file') is not None:
            image=request.FILES.get('file')
        else:
            image="/static/images/default.png"
        books=book(book_name=bname,description=des,author=author,publication=publication,price=price,quantity=quantity,category=cat1,book_image=image)
        books.save()
        print(cat1)
        return redirect('bookview')
    return render(request,'admin/addbook.html')

@login_required(login_url='login')
def bookview(request):
    
    if 'uid' in request.session:
        books=None
        categorys=Category.objects.all()
        categoryid=(request.GET.get('category'))
        if categoryid:
            books=book.objects.filter(category_id=categoryid)
        else:
            books=book.objects.all()
        data={}
        data['books']=books
        data['categorys']=categorys
        return render(request,'admin/viewbook.html',data)
    return redirect('load_adminhome')


def load_editbook(request,pk):
    print("hii")
    categorys=Category.objects.all()
    books=book.objects.get(id=pk)
    data={}
    data['books']=books
    data['categorys']=categorys
    return render(request,'admin/editbook.html',data)

def editbookdetails(request,pk):

    ##################################
    if request.method=='POST':
        books=book.objects.get(id=pk)
        print(books.id)
        books.book_name=request.POST['bname']
        books.description=request.POST['description']
        books.author=request.POST['author']
        books.publication=request.POST['publication']
        books.price=request.POST['price']
        books.quantity=request.POST['quantity']
        sel1=request.POST['select']
        cat1=Category.objects.get(id=sel1)
        if request.FILES.get('file') is not None:
        #    if not books.book_image=="/media/image/default.png":
        #        os.remove(books.book_image.path)
        #        books.book_image==request.FILES['file']
                print("hi")
        #    else:
                books.book_image=request.FILES.get('file')
                print("kuii")
        else:
            os.remove(books.book_image.path)
            books.book_image="/static/images/default.png"
        
        books.save()
        print(cat1)
        return redirect('load_book')
    return render(request,'admin/viewbook.html')

@login_required(login_url='login')
def profile(request):
    if 'uid' in request.session:
        user=Usermember.objects.filter(user=request.user)
        context={'user':user}
        return render(request,'user/userprofile.html',context)

def search(request):
    if request.method=='GET':
        query=request.GET.get('query')
        print(query)
        print("query")
        if query:
            books=book.objects.filter(book_name__contains=query)
            return render(request,'user/search.html',{'books':books})
        else:
            print("No information to show")
            return render(request,'user/search.html',{})

def userbookview(request):
    if 'uid' in request.session:
        books=None
        categorys=Category.objects.all()
        categoryid=(request.GET.get('category'))
        if categoryid:
            books=book.objects.filter(category_id=categoryid)
        else:
            books=book.objects.all()
        data={}
        data['books']=books
        data['categorys']=categorys
        return render(request,'user/viewbook.html',data)
    return redirect('profile')

    
def deletepage(request,pk):
    books=book.objects.get(id=pk)
    return render(request,'admin/deletebook.html',{'books':books})

def delete_book(request,pk):
    books=book.objects.get(id=pk)
    books.delete()
    return redirect('bookview')


def deleteuser(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect('/viewuser')


def load_editprofile(request):
#    user=usermember.objects.filter(user=request.user)
#    print(user.id)
    print("load editprofile")
    if 'uid' in request.session:
        uid = User.objects.get(id=request.session["uid"])
        user=User.objects.get(username=uid)
        usr=Usermember.objects.get(user_id=user.id)
        return render(request,'user/editprofile.html',{'usr':usr})


def editprofile(request):
    if request.method=='POST':
        umember=Usermember.objects.get(user=request.user)
        umember.user.first_name=request.POST.get('fname')
        umember.user.last_name=request.POST.get('lname')
        umember.user.username=request.POST.get('uname')
        umember.user.email=request.POST.get('email')
        umember.user_address=request.POST.get('address')
        umember.user_mobile=request.POST.get('mobile')
       

        if request.FILES.get('file') is not None:
            if not umember.user_photo == "/static/images/default.png":
                os.remove(umember.user_photo.path)
                umember.user_photo = request.FILES['file']
                print('hii')
            else:
                umember.user_photo = request.FILES['file']
                print("hello")
        else:
            os.remove(umember.user_photo.path)
            umember.user_photo = "/static/images/default.png" 
            print("work")
        
        umember.save()
        return redirect('profile')
    return render(request,'user/userprofile.html')
        
        
def requstbook(request):


#    if request.method=='POST':

    #    user=User.objects.get(user=request.user)
    #    print(user.id)
        books=request.POST.get('book')
        print("book=",books)
        uid = User.objects.get(id=request.session["uid"])
        user=User.objects.get(username=uid)
        
        reqbook=requestbook(book_id=books,user_id=user.id)
        reqbook.save()
       
        return redirect('userbookview')
    

def load_issuebook(request):
    
    reqbook=requestbook.objects.all()
    
    return render(request,'admin/issuebook.html',{'reqbook':reqbook})
        
def load_approve(request,pk):
    reqbook=requestbook.objects.get(id=pk)
    user=User.objects.get(id=reqbook.user_id)
    data={}
    data['reqbook']=reqbook
    data['user']=user
    print(data)
    return render(request,'admin/approvebook.html',data)

def approvebook(request,pk):
    if request.method=='POST':
        reqbooks=requestbook.objects.get(id=pk)
        print(reqbooks.book_id)
        print(reqbooks.user_id)
    #    books=book.objects.get(id=reqbooks.book_id)
    #    user=User.objects.get(user=reqbooks.user_id)
        isdate=request.POST['isdate']
        rdate=request.POST['rdate']
        issuebooks=issuebook(issuedate=isdate,
                             expirydate=rdate,
                             book_id=reqbooks.book_id,
                             user_id=reqbooks.user_id)
        issuebooks.save()
        reqbooks.delete()
        return redirect('load_issuedbook')
    return render(request,'admin/viewissuebook.html')

def load_issuedbook(request):
#    issuebooks=issuebook.objects.all()
#    return render(request,'admin/viewissuebook.html',{'issuebooks':issuebooks})
    issuedbooks=issuebook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>30:
            day=d-30
            fine=day*10


        books=list(book.objects.filter(id=ib.book_id))
        user=list(User.objects.filter(id=ib.user_id))
        i=0
        for l in books:
            t=(user[i].first_name,user[i].id,books[i].book_name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'admin/viewissuebook.html',{'li':li}) 




def load_userissuedbook(request):
#    if 'uid' in request.session:   
#        issuebooks=issuebook.objects.filter(user=request.user)
#        return render(request,'user/issuedbook.html',{'issuebooks':issuebooks})
    issuedbooks=issuebook.objects.filter(user=request.user)
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>30:
            day=d-30
            fine=day*10


        books=list(book.objects.filter(id=ib.book_id))
        user=list(User.objects.filter(id=ib.user_id))
        i=0
        for l in books:
            t=(user[i].first_name,user[i].id,books[i].book_name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'issuedbook.html',{'li':li}) 




##############################################################
    issuedbooks=issuebook.objects.filter(user=request.user)
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>30:
            day=d-30
            fine=day*10


        books=list(book.objects.filter(id=ib.book_id))
        user=list(User.objects.filter(id=ib.user_id))
        i=0
        for l in books:
            t=(user[i].first_name,user[i].id,books[i].book_name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'issuedbook.html',{'li':li}) 


def returnbook(request,pk):
    
    isbooks=issuebook.objects.get(user_id=pk)
    isbooks.delete()
    return redirect('load_issuedbook')

#########################
