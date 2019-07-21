from django.contrib import admin

# Register your models here.
from .models import Grade, Student

class StudentInline(admin.TabularInline):
    model = Student
    extra = 3

# 自定义Admin
class GradeAdmin(admin.ModelAdmin):
    inlines = [
        StudentInline,
    ]

    # 列表页属性
    list_display = ('name', 'date', 'girlNum', \
    'boyNum', 'teacherNum', 'isDeleted')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 5

    # 添加、修改页属性
    # fields = []
    fieldsets = (
        ('Base Information',{'fields':('name', 'date')}),
        ('Grade Infomaiton',{'fields':('girlNum', 'boyNum','teacherNum')}),
        ('Advanced option',{'classes':('collapse',),'fields':('isDeleted',)})
        )

class StudentAdmin(admin.ModelAdmin):
    def gender(obj):
        return 'M' if obj.gender else 'F'
    gender.short_description='Gender'
    
    list_display = ('name', 'age', gender, 'height', 'weight' , \
    'intro', 'grade', 'isDeleted')
    list_filter = ['grade']
    search_fields = ['name']
    list_per_page = 20

    fieldsets = (
    ('Base Information',{'fields':('name', 'age', 'gender', 'grade')}),
    ('Others',{'fields':('weight', 'height','intro')}),
    ('Advanced option',{'classes':('collapse',),'fields':('isDeleted',)})
    )

# 模型注册
admin.site.register(Grade, GradeAdmin)
admin.site.register(Student, StudentAdmin)