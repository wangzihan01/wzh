from django.shortcuts import render
from .models import Banner
from .models import Post, Comment, BlogCategory, FriendlyLink,Tags
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import PageNotAnInteger, EmptyPage, Paginator


# Create your views here.


class SearchView(View):
    # 搜索框
    def post(self, request):
        kw = request.POST.get('keyword')
        post_list = Post.objects.filter(Q(title__icontains=kw) | Q(content__icontains=kw))

        ctx = {
            'post_list': post_list
        }
        return render(request, 'list.html', ctx)

    # 分页



def list(request,tid=-1,cid=-1):
    #　点击标签获取博客
    if tid != -1:
        cat = Tags.objects.get(id=tid)
        post_list = cat.post_set.all()
    # 用分类查询博客
    elif cid != -1:
        cat = BlogCategory.objects.get(id=cid)
        post_list = cat.post_set.all()
    else:
        post_list = Post.objects.order_by('-pub_date')

    # 标签云
    tags = Tags.objects.all()
    # 取出所有便签放入一个列表中
    tag_message_list = []
    for t in tags:
        count = len(t.post_set.all())
        tag_message_list.append({'name':t.name,'id':t.id,'count':count})



    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
        p = Paginator(post_list, per_page=1, request=request)
        post_list = p.page(page)


    ctx = {
        'post_list': post_list,
        'tag_message_list' : tag_message_list,

}
    return render(request, 'list.html', ctx)


def index(request):
    banner_list = Banner.objects.all()
    # 去数据库里面去除所有　推荐的文章
    recommit_list = Post.objects.filter(is_recomment=True)
    for recommit in recommit_list:
        recommit.content = recommit.content[:100] + '......'

    # 取出所有文章　按照时间倒序
    post_list = Post.objects.order_by('-pub_date')
    for post in post_list:
        post.content = post.content[:160] + '......'

    # 　博客分类
    blogcategory_list = BlogCategory.objects.all()

    # 最新评论博客列表
    commit_list = Comment.objects.order_by('-pub_date')
    new_commit_list = []
    for commit in commit_list:
        if commit.post not in new_commit_list:
            new_commit_list.append(commit.post)

    # 友情链接
    friendlylink_list = FriendlyLink.objects.all()



    ctx = {
        'banner_list': banner_list,
        'recommit_list': recommit_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
        'new_commit_list': new_commit_list,
        'friendlylink_list': friendlylink_list,

    }
    return render(request, 'index.html', ctx)


#  详 情
def blog_detail(request,bid):
    post = Post.objects.get(id = bid)
    post.views = post.views + 1
    post.save()

    # 标签
    tag_list = post.tags.all()
    ctx = {
        'post':post,
        'tag_list':tag_list,
    }
    return render(request,'show.html',ctx)

# def list(request):
#     list_list = Post.objects.all()
#
#     # 　评论
#    # new_list_list = Comment.objects.order_by('-pub_date').all()
#     #new_commit_list = []
#     #for ss in new_list_list:
#     #    if ss.post not in new_commit_list:
#       #      new_commit_list.append(ss.post)

# li = {
#     'list_list': list_list,
#   #  'new_commit_list': new_commit_list,
# }
# return render(request, 'list.html', li)


# def blog_list(request, tid=-1):
#    # tid=-1时候 代表的是  从列表过来
#    tid = int(tid)
#    post_list = None
#   if tid != -1:
#        post_list = Post.objects.filter(tags=tid)
#   else:
#       post_list = Post.objects.order_by('-pub_date')
#
#   try:
#      page = request.GET.get('page', 1)
#   except PageNotAnInteger:
#      page = 1

#  p = Paginator(post_list, per_page=10, request=request)
#  post_list = p.page(page)
#
#  ctx = {
#    'post_list': post_list,

# }

# return render(request, 'list.html', ctx)
