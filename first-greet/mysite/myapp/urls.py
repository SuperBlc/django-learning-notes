from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    # url(r'^(\d+)/$', views.detail),
    path('<int:num>', views.detail),
    path('grade/', views.grade),
    path('grade/<int:num>', views.gradeStu),
    path('grade/ftest', views.F_test),
    path('student/all',views.student),
    path('student/create', views.createStu),
    path('student/page<int:num>',views.limit_student),
    path('student/page<int:num>',views.limit_student2),
    path('student/search', views.lookup_stu),
    path('attribute', views.attribute),
    path('getone', views.get_one),
    path('getmany', views.get_many),
    path('register', views.register),
    path('register_info', views.register_info),
    path('logout',views.myapp_logout), 
    path('cookies/create', views.cookies_demo),
    path('redirect',views.redirect), 
    path('verifycode', views.verifycode),
    path('upload', views.upload),
    path('savefile', views.savefile),
    ## API
    path('student/api/all',views.api_students),
    path('student/api/grade<int:num>',views.api_grade),
]