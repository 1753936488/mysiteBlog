import datetime
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.shortcuts import render
from django.utils import timezone
from django.core.cache import cache
from blog.models import Blog
from blog.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data


def get_7_days_hot_data():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    # 根据object_id分组求和
    blogs = Blog.objects\
                 .filter(read_details__date__lt=today, read_details__date__gte=date)\
                 .values('id', 'title')\
                 .annotate(read_num_sum=Sum('read_details__read_num'))\
                 .order_by('-read_num_sum')
    return blogs[:7]


def get_30_days_hot_data():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    # 根据object_id分组求和
    blogs = Blog.objects\
                 .filter(read_details__date__lt=today, read_details__date__gte=date)\
                 .values('id', 'title')\
                 .annotate(read_num_sum=Sum('read_details__read_num'))\
                 .order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    seven_days_hot_data = cache.get('7_days_hot_data')
    if seven_days_hot_data is None:
        seven_days_hot_data = get_7_days_hot_data()
        cache.set('7_days_hot_data', seven_days_hot_data, 3600)  # 有效期1小时

    one_month_hot_data = cache.get('30_days_hot_data')
    if one_month_hot_data is None:
        one_month_hot_data = get_30_days_hot_data()
        cache.set('30_days_hot_data', one_month_hot_data, 3600)  # 有效期1小时

    context = {
        'read_nums': read_nums,
        'dates': dates,
        'today_hot_data': get_today_hot_data(blog_content_type),
        'yesterday_hot_data': get_yesterday_hot_data(blog_content_type),
        '7_days_hot_data': seven_days_hot_data,
        '30_days_hot_data': one_month_hot_data,
    }
    return render(request, 'home.html', context)


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


def get_blog_list_common_data(request, search_blogs):
    search_blogs_count = search_blogs.count()
    current_page = request.GET.get('p', 1)
    paginator = CustomPaginator(current_page, 2, search_blogs, 6)
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

    context = {
        'search_blogs': page_of_blog.object_list,
        'page_of_blog': page_of_blog,
        'page_range': page_range,
        'search_blogs_count': search_blogs_count,
    }
    return context


def search(request):
    wd = request.GET.get('wd', '').strip()
    condition = None
    for word in wd.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)
    if condition is not None:
        search_blogs = Blog.objects.filter(condition)   # i忽略大小写
    context = get_blog_list_common_data(request, search_blogs)
    context['search_word'] = wd
    return render(request, 'search.html', context)
