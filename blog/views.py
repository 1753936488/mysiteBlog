from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from blog.models import Blog
from django.db.models import Count
from blog.models import BlogType
from blog.utils import read_once
# from user.forms import LoginForm


class CustomPaginator(Paginator):
    def __init__(self, current_page, max_pager_num, *args, **kwargs):
        """
        :param current_page: 当前页
        :param max_pager_num:最多显示的页码个数
        :param args:
        :param kwargs:
        :return:
        """
        self.current_page = int(current_page)
        self.max_pager_num = max_pager_num
        super(CustomPaginator, self).__init__(*args, **kwargs)

    def page_num_range(self):
        # 当前页面
        # self.current_page
        # 总页数
        # self.num_pages
        # 最多显示的页码个数
        # self.max_pager_num

        if self.num_pages < self.max_pager_num:
            return range(1, self.num_pages + 1)

        part = int(self.max_pager_num / 2)
        if self.current_page - part < 1:
            return range(1, self.max_pager_num + 1)

        if self.current_page + part > self.num_pages:
            return range(self.num_pages + 1 - self.max_pager_num, self.num_pages + 1)

        return range(self.current_page - part, self.current_page + part + 1)


def get_blog_list_common_data(request, blogs_all_list):
    current_page = request.GET.get('p', 1)
    paginator = CustomPaginator(current_page, 2, blogs_all_list, 6)
    page_of_blog = paginator.get_page(current_page)
    page_range = list(paginator.page_num_range())
    # 加上省略页码表级
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=date.year, created_time__month=date.month).count()
        blog_dates_dict[date] = blog_count

    context = {
        'blogs': page_of_blog.object_list,
        'blog_all': blogs_all_list,
        'page_of_blog': page_of_blog,
        'page_range': page_range,
        # 'blog_types': BlogType.objects.all(),
        'blog_types': BlogType.objects.annotate(blog_count=Count('blog')),
        'blog_dates_dict': blog_dates_dict,

    }
    return context


def blog_list(request):
    # 获取到所有的博客信息列表
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    # 得到单条博客的详细信息
    blog = get_object_or_404(Blog, pk=blog_pk)
    key = read_once(request, blog)
    previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context = {
        'blog': blog,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
        # 'login_form': LoginForm(),
    }
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(key, 'true')  # 默认关闭浏览器失效 max_age=60设置60s失效
    return response


def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)


def blog_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blog_with_date.html', context)
