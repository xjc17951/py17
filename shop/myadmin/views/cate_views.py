from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .. import models
from django.core.paginator import Paginator
def tab():
    cates = models.Cates.objects.extra(select = {'newpath':'concat(paths,id)'}).order_by('newpath')
    for i in cates:
        num = i.paths.count(',')-1
        i.newname=num*'→'
    return cates    

def addcate(request):
    if request.method=='GET':
        # 将所有的类型返回
        cates = tab()

        return render(request,'myadmin/cate/addcate.html',{'cates':cates})
    elif request.method=='POST':
        # 接受pid 通过pid来判断是不是顶级分类
        pid = request.POST.get('pid')
        name = request.POST.get('name')
        print(pid)
        print(name)
        if pid=='0':
            cate = models.Cates()
            cate.name=name
            cate.upid=int(pid)
            cate.paths='0,'
            cate.save()
        else:
            # 根据pid找父级 paths
            pobj = models.Cates.objects.get(id=pid)
            c = models.Cates()
            c.name=name
            c.upid=pobj.id
            c.paths=pobj.paths+pid+','
            c.save()
           
            
        # 接受数据添加数据
        return HttpResponse("<script>alert('添加成功');location.href=''</script>")

def catelist(request):
    # 查询所有的分类
    # cates = models.Cates.objects.all()
    # select *,concat(paths,id) as newpath  from myadmin_cates order by newpath;
    # 模型提供 extra
    # cates = models.Cates.objects.extra(select = {'newpath':'concat(paths,id)'}).order_by('newpath')

    # for i in cates:
    #     num = i.paths.count(',')-1
    #     i.newname=num*'|----'
    cates = tab()
    cates = models.Cates.objects.all()
    print(cates)
    # 接受类型
    types = request.GET.get('type')
    print(types)
    # 接受关键字
    search = request.GET.get('search')
    print(search)
    # 判断用是否搜索内容
    if types:
        from django.db.models import Q
        if types=='all':
            #根据id username phone
            # select * from myadmin_users where id like %search% or username like %search% or phone like %search%
            # from django.db.models import Q
            cates = models.Cates.objects.filter(Q(name__contains=search)|Q(id__contains=search)|Q(paths__contains=search))
        elif types=='a':
            cates = models.Cates.objects.filter(Q(paths__contains='0,1,')&Q(name__contains=search))
        elif types=='b':
            cates = models.Cates.objects.filter(Q(paths__contains='0,4,')&Q(name__contains=search))
        elif types=='c':
            cates = models.Cates.objects.filter(Q(paths__contains='0,8,')&Q(name__contains=search))
    for i in cates:
        num = i.paths.count(',')-1
        i.newname=num*'→'
    # 实例化分页对象
    p = Paginator(cates,6)

    #一共可以分多少页
    sumpage=p.num_pages
    print(sumpage)

    # 取第几页的数据
     # 接受用户的页码
    page = int(request.GET.get('p',1))
    # 第几页的数据
    page1 = p.page(page)

    # 判断 如果用输入的页码<=3 显示前五个页码
    if page<=3:
        # 页码的迭代序列  [1,2,3,4,5,6,7]
        prange = p.page_range[:5]
    elif page+2>=sumpage:
        prange = p.page_range[-5:]
    else:
        prange = p.page_range[page-3:page+2]

    return render(request,'myadmin/cate/catelist.html',{'cates':page1,'prange':prange,'page':page,'sumpage':sumpage})
    #http://192.168.116.129:8000/admin/listcate/?type=all&search=0%2C1%2C
def delcate(request):
    # 接受id
    pid = int(request.GET.get('pid'))
    # 判断有没有子分类
    cnum = models.Cates.objects.filter(upid=pid).count()
    if cnum:
        return JsonResponse({'msg':0})
    else:
        c = models.Cates.objects.get(id=pid)
        c.delete()
        return JsonResponse({'msg':1})

# 修改
def editcate(request):
    # 接受id和name
    cid = int(request.GET.get('id'))
    cname = request.GET.get('name')
    try:
        cate = models.Cates.objects.get(id=cid)
        cate.name=cname
        cate.save()
        return JsonResponse({'msg':1})
    except :
        return JsonResponse({'msg':0})
    
        
