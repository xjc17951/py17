from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .. import models
import time,os
from . import cate_views,user_views
from shop.settings import BASE_DIR
from django.core.paginator import Paginator

# 添加
def addgoods(request):
    # 查询所有的分类  进行返回
    types = cate_views.tab()
    return render(request,'myadmin/goods/addgoods.html',{'types':types})

# 添加数据
def goodsinsert(request):

     # 接受用户的信息
    ginfo = request.POST.dict()
    ginfo.pop('csrfmiddlewaretoken')
    # print(ginfo)


    file = request.FILES.get('g_url')
    # print(file)
    if not file:
        return HttpResponse('<script>alert("请选择图片");history.back(-1)</script>')


    # 调图片上传
    g_url=user_views.upload(file)
    # print(g_url)
    try:
        # 入库
        goods = models.Goods()
        goods.title=ginfo['title']
        goods.ordernum=ginfo['ordernum']
        goods.g_url=g_url
        goods.price=ginfo['price']
        goods.ginfo=ginfo['ginfo']
        goods.cateid=models.Cates.objects.get(id=ginfo['cateid'])
        goods.save()

        # 返回
        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_addgoods')+'"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");history.back(-1)</script>')

def goodslist(request):
    goods = models.Goods.objects.all().exclude(status=3)
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
            goods = models.Goods.objects.filter(Q(title__contains=search)|Q(id__contains=search)|Q(price__contains=search))
    # 实例化分页对象
    p = Paginator(goods,3)
    print(p)

    #一共可以分多少页
    sumpage=p.num_pages
    print(sumpage)

    # 取第几页的数据
     # 接受用户的页码
    page = int(request.GET.get('p',1))
    # print(page)
    # 第几页的数据
    page1 = p.page(page)
    # print(page1)

    # 判断 如果用输入的页码<=3 显示前五个页码
    if page<=3:
        # 页码的迭代序列  [1,2,3,4,5,6,7]
        prange = p.page_range[:5]
    elif page+2>=sumpage:
        prange = p.page_range[-5:]
    else:
        prange = p.page_range[page-3:page+2]

    return render(request,'myadmin/goods/list.html',{'goods':page1,'prange':prange,'page':page,'sumpage':sumpage})

#删除用户
def delgoods(request):
    uid = request.GET.get('uid')
    # print(uid)

    gl=models.Goods.objects.get(id=uid)
    # print(gl)
    gl.status=3
    # print(gl)
    gl.save()

    return redirect(reverse('myadmin_goodslist'))

# 修改商品
def editgoods(request):
    # get goods id
    uid = request.GET.get('uid')
    # print(uid)
    # 判断是get还是post
    if request.method=='GET':
        egs=models.Goods.objects.get(id=uid)
        types = cate_views.tab()
        return render(request,'myadmin/goods/edit.html',{'egs':egs,'types':types})
    elif request.method=='POST':
        # 获取用户的提交信息
        userinfo = request.POST.dict()
        # 更新数据
        uinfo = models.Goods.objects.get(id=uid)
        uinfo.title=userinfo['title']
        uinfo.price=userinfo['price']
        uinfo.ordernum=userinfo['ordernum']
        # 判断头像有没有上传
        file = request.FILES.get('g_url')
        if file:
            # 右头像上传，要吧旧投头像删除
            # /dajngo07/py17/shop    ./static/pics/1547686265.6370358.png
            os.remove('.'+uinfo.g_url)
            g_url=user_views.uuload(file)
            uinfo.g_url=g_url
        uinfo.save()
        return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_goodslist')+'"</script>')
