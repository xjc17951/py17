from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from . import models
import time,os
# Create your views here.
# 首页
def index(request):
	return render(request,'myadmin/index.html')

# 用户列表
def vipuser(request):
	# 查询库里的所有数据
	# 进行数据分配 通过 模板语法将数据展示到模板当中
	return render(request,'myadmin/table-list.html')

# add user
def adduser(request):
	if request.method=='GET':
		return render(request,'myadmin/adduser.html')
	elif request.method=='POST':
		userinfo = request.POST.dict()
		userinfo.pop('csrfmiddlewaretoken')
		myfile = request.FILES.get("head_url",None)
		if not myfile:
			return HttpResponse("<script>alert('请选择头像');location.href=''</script>")
		userinfo['head_url']=upload(myfile)
		userinfo['password'] = make_password(userinfo['password'],None, 'pbkdf2_sha256')

		try:
			# 写入数据
			user=models.Users(**userinfo)
			print(user)
			user.save()
			return HttpResponse("<script>alert('添加成功!');location.href='"+reverse('myadmin_vipuser')+"'</script>")

		except:	
			return HttpResponse("<script>alert('添加失败!');location.href=''</script>")

def upload(myfile):
	# 新名字
	filename=str(time.time())+"."+myfile.name.split('.').pop()
	destination=open("./static/pics/"+filename,"wb+")
	for chunk in myfile.chunks():
		destination.write(chunk)
	destination.close()
	# /static/pics/filename
	return '/static/pics/'+filename