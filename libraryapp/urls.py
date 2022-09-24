from django.urls import include, path
from .import views


urlpatterns = [
    path('',views.load_home,name='load_home'),
    path('load_signup',views.load_signup,name='load_signup'),
    path('load_login',views.load_login,name='load_login'),
    path('load_adminhome',views.load_adminhome,name='load_adminhome'),
    path('signup',views.signup,name='signup'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('load_signin',views.load_signin,name='load_signin'),
    path('load_category',views.load_category,name='load_category'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('viewcategory',views.viewcategory,name='viewcategory'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('viewuser',views.viewuser,name='viewuser'),
    path('load_book',views.load_book,name='load_book'),
    path('add_book',views.add_book,name='add_book'),
    path('bookview',views.bookview,name='bookview'),
    path('load_editbook/<int:pk>',views.load_editbook,name='load_editbook'),
    path('editbookdetails/<int:pk>',views.editbookdetails,name='editbookdetails'),
    path('profile',views.profile,name='profile'),
    path('search',views.search,name='search'),
    path('userbookview',views.userbookview,name='userbookview'),
    path('deletepage/<int:pk>',views.deletepage,name='deletepage'),
    path('delete_book/<int:pk>',views.delete_book,name='delete_book'),
    path('deleteuser/<int:id>',views.deleteuser,name='deleteuser'),
    path('load_editprofile',views.load_editprofile,name='load_editprofile'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('requstbook',views.requstbook,name='requstbook'),
    path('load_issuebook',views.load_issuebook,name='load_issuebook'),
    path('load_approve/<int:pk>',views.load_approve,name='load_approve'),
    path('approvebook/<int:pk>',views.approvebook,name='approvebook'),
    path('load_issuedbook',views.load_issuedbook,name='load_issuedbook'),
    path('load_userissuedbook',views.load_userissuedbook,name='load_userissuedbook'),
    path('returnbook<int:pk>',views.returnbook,name='returnbook'),
    path('userhomepage',views.userhomepage,name='userhomepage')
]