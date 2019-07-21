from django.db import models

# Create your models here.
class Grade(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    girlNum = models.IntegerField()
    boyNum = models.IntegerField()
    teacherNum = models.IntegerField()
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.m_name

    class Meta:
        db_table = "grade"

class StudentManager(models.Manager):
    def get_queryset(self):
        return super(StudentManager,self).get_queryset().filter(isDeleted=False)

class Student(models.Model):
    # 自定义模型管理器后，django不再生成默认的objects管理器
    # 模型管理器是模型与数据库进行交互的接口，一个模型可以有多个接口
    # 作用：向管理器类中添加额外的方法、修改管理器返回的原始查询集合    
    # stu = models.Manager()
    stu = StudentManager()
    # 字段
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.BooleanField(default=True)
    intro = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()
    isDeleted = models.BooleanField(default=False)

    # m_createTime = models.DateField(auto_now_add=True)
    # m_updateTime = models.DateField(auto_now=True)

    # 关联外键
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "student"

    @classmethod
    def createStu(cls, _name, _age, _grade, _intro, _gender=False, _height=154.6, _weight=44.6, _isDeleted=False):
        stu = cls(
            name=_name, age=_age, gender=_gender, grade=_grade,\
            intro=_intro, height=_height, weight=_weight,\
            isDeleted=_isDeleted)

        return stu