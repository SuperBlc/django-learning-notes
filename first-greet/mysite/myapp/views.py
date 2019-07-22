from django.shortcuts import render
from .models import Grade, Student
# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is my first view")

def detail(request, num):
    return HttpResponse("detail-%s"%num)

def grade(request):
    # 模型中取数据
    grade_list = Grade.objects.all()
    # 将取出的数据交给模板，渲染
    return render(request, 'myapp/grade.html',{'grades':grade_list})

def student(request):
    students = Student.stu.all()
    # render 常用参数顺序
    # request 模板位置 模板中参数列表
    info = "共有%d名学生，信息如下"%(len(students))
    return render(request, 'myapp/student_all.html',{'students':students,'info':info})

# 限制查询集
def limit_student(request,num):
    """
        在新建的查询集中，缓存首次为空，第一次对查询集求值，会发生数据缓存，django会将
        查询出来的数据做一次缓存，并返回查询结果
    """
    students = Student.stu.all()[(num-1)*10:num*10]
    
    num = 1 if num < 1 else num
    prev = num - 1 if num - 1 > 0 else 1
    back = 1 if (len(students) < 10) else (num + 1)

    info = "共有%d名学生，信息如下"%(len(students))
    return render(request, "myapp/student.html", \
        {"students":students,"num":num,"info":info, "prev":prev,"back":back})

from django.core.paginator import Paginator
NUM_IN_PAGE = 10
def limit_student2(request,num):
    """
        使用Paginator进行分页
    """
    studentsList = Student.stu.all()
    pInator = Paginator(studentsList, NUM_IN_PAGE)

    page = pInator.get_page(num)

    if num - 1 > 0:
        prev = num - 1
    elif num == 1:
        prev = pInator.page_range[-1]
    else:
        prev = pInator.page_range[0]
    back = 1 if (len(page.object_list) < NUM_IN_PAGE) else (num + 1)

    info = "共有%d名学生，信息如下"%(page.number)
    return render(request, "myapp/student2.html", \
        {"students":page,"num":num,"info":info, "prev":prev,"back":back, "page":pInator.page_range})


def gradeStu(request, num):
    grade = Grade.objects.get(pk=num)
    stu = grade.student_set.all()
    info = "班级%d,有%d名学生，名单如下"%(num,len(stu))
    return render(request, 'myapp/student_all.html', {'students':stu,'info':info})

def createStu(request):
    grade = Grade.objects.get(pk=4)
    stu = Student.createStu("肖玉", 16, grade, "大家好我是肖玉，请多多关照")
    stu.save()
    return HttpResponse("肖玉已经进入班级4啦")

def lookup_stu(request):
    stu = Student.stu.filter(name__contains="陈")
    info = "陈姓的学生共有%d名"%len(stu)
    return render(request, "myapp/student_all.html", {"students":stu,"info":info})

from django.db.models import F
def F_test(request):
    grade = Grade.objects.filter(girlNum__gte=F('boyNum'))
    s = ""
    for g in grade:
        s += g.name + "--"
    return HttpResponse(s)

def attribute(request):
    print(request.path)
    print(request.method)
    print(request.encoding)
    print(request.GET)
    print(request.POST)
    print(request.FILES)
    print(request.COOKIES)
    print(request.session)
    '''
    /myapp/student/attribute
    GET
    None
    <QueryDict: {}>
    <QueryDict: {}>
    <MultiValueDict: {}>
    {'csrftoken': 'zmF5WXqt93i3X45bs9tOU13yuqLiq7NsE9NWpMdsO0vvAuB4POlWSXmrWXzY2FH6'}
    <django.contrib.sessions.backends.db.SessionStore object at 0x000001FDE90CA128>
    '''
    return HttpResponse("Get all request attributes")

# 获取get传递的数据
def get_one(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    c = request.GET.get('c')
    s = "a=%s,b=%s,c=%s"%(a,b,c)
    return HttpResponse(s)

def get_many(request):
    a = request.GET.getlist('a')
    b = request.GET.getlist('b')
    c = request.GET.getlist('c')
    s = "a={},b={},c={}".format(a,b,c)
    return HttpResponse(s)

def register(request):
    if "checkOk" in request.session:
        message ="您输入的验证码有误" if not request.session["checkOk"] else ""
    else:
        message = ""
    return render(request, 'myapp/register.html',{"message":message})

def register_info(request):
    name=request.POST.get('name')
    # age=request.POST.get('age')
    # gender=request.POST.get('gender')
    # s = "name={},age={},gender={}".format(name,age,gender)
    
    # 存储session
    request.session['name']=name

    vcode = request.POST.get('verifycode').upper()
    server_vcode = request.session['verifycode']

    if vcode == server_vcode:
        if 'checkOk' in request.session:
            request.session['checkOk'].clear()
        return HttpResponseRedirect("/")
    else:
        request.session['checkOk']=False
        return HttpResponseRedirect("/myapp/register")

def myapp_logout(request):
    # 清除session
    # 方法1
    request.session.clear()
    # 方法2
    # request.session.flush()
    # 方法3
    # from django.contrib.auth import logout
    # logout(request)
    return HttpResponseRedirect("/")

import hashlib
def cookies_demo(request):
    res = HttpResponse()
    my_cookies = request.COOKIES
    if "D_D" not in my_cookies:
        message = "this is a cookie demo"
        hl = hashlib.md5()
        hl.update(message.encode(encoding="utf-8"))
        res.set_cookie("D_D", hl.hexdigest())
        res.write("cookies has saved.")
    else:
        res.write("<h1>D_D:"+ my_cookies["D_D"] +"</h1>")
    return res

# 重定向
from django.http import HttpResponseRedirect
def redirect(request):
    return HttpResponseRedirect("/myapp")

def verifycode(request):
    # 导入依赖的包
    import random
    from PIL import ImageDraw, ImageFont, Image

    # 随机生成背景颜色
    bgcolor = (random.randrange(20, 120), 255,
    random.randrange(20, 120))
    # 设定图片的宽高
    width = 100
    height = 50
    # 创建一个Image对象
    img = Image.new('RGB', (width, height), bgcolor)
    # 创建一个在img上绘图的Draw对象
    draw = ImageDraw.Draw(img)
    # 在图片上随机画30条线
    for i in range(0, 30):
        xy = [(random.randrange(0, width), random.randrange(0, height)),
            (random.randrange(0, width), random.randrange(0, height))]
        fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        draw.line(xy, fill=fill, width=1)
    # 候选字符串，包含数字、大小写字母
    candidate = [str(i) for i in range(10)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
	
    # 从候选字符串中，随机选择4个字符作为验证码的内容
    rand_str = ""
    for i in range(0,4):
        rand_str += candidate[random.randrange(0, len(candidate)-1)]

    # 字体
    text_font = ImageFont.truetype("consola.ttf", 40)
    for i in range(4):
        text_fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        draw.text((i*20+10,2), rand_str[i], font=text_font, fill=text_fill)

    for i in range(0, 300):
        xy = (random.randrange(0, width), random.randrange(0, height))	
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    print(rand_str)

    del draw

    request.session['verifycode']=rand_str.upper()

    import io
    buf = io.BytesIO()
    img.save(buf, 'png')

    return HttpResponse(buf.getvalue(), 'image/png')


def upload(request):
    return render(request, "myapp/upload.html")

from os.path import join
from django.conf import settings
def savefile(request):
    if request.method == "POST":
        f = request.FILES["file"]
        file_path = join(settings.MEDIA_ROOT, f.name)

        with open(file_path, 'wb') as file:
            for info in f.chunks():
                file.write(info)
        return HttpResponse("上传成功：%s"%file_path)
    else:
        return HttpResponse("上传失败")

### API
from django.http import JsonResponse
def api_students(request):
    student = Student.stu.all()
    l = []
    for s in student:
        l.append({"id":s.id,"name":s.name, "age":s.age, "introduction":s.intro})
    return JsonResponse({"students":l})

from django.http import JsonResponse
def api_grade(request, num):
    if num > 0 and num < 6:
        grade = Grade.objects.get(pk=num)
        stu = grade.student_set.all()
        l = []
        for s in stu:
            l.append({"id":s.id,"name":s.name, "age":s.age, "introduction":s.intro})
        return JsonResponse({"status":200,"students":l})
    else:
        return JsonResponse({"status":404,"students":[]})