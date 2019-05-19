from django.db import models


class DishType(models.Model):
    type = models.CharField(max_length=20, verbose_name='菜系')

    class Meta:
        verbose_name_plural = "菜系"

    def __str__(self):
        return self.type


class DishCategory(models.Model):
    category = models.CharField(max_length=20, verbose_name='菜型')

    class Meta:
        verbose_name_plural = "菜型"

    def __str__(self):
        return self.category


class PackageTheme(models.Model):
    themeName = models.CharField(max_length=20, verbose_name='套餐主题名', null=True)

    class Meta:
        verbose_name_plural = "套餐主题"

    def __str__(self):
        return self.themeName


class Dish(models.Model):
    DishName = models.CharField(max_length=20, verbose_name='菜名')
    CostPrice = models.FloatField(verbose_name='成本价')
    Price = models.FloatField(verbose_name='标价')
    Sales = models.IntegerField(verbose_name='销量')
    Moral = models.CharField(max_length=100, verbose_name='寓意', blank=True, default='')
    img = models.CharField(max_length=500, verbose_name='图片地址', blank=True, default='')
    type = models.ForeignKey(DishType, on_delete=models.CASCADE, verbose_name='菜系')
    category = models.ForeignKey(DishCategory, on_delete=models.CASCADE, default='')
    # IntegerField(default=0, choices=((0, ''), (1, '天上飞的'),
    #                                                (2, '地上跑的'), (3, '水里游的'), (4, '凉菜'),), verbose_name='菜型')

    class Meta:
        verbose_name_plural = "单菜详情"

    def __str__(self):
        return self.DishName


class Package(models.Model):
    PackageName = models.CharField(max_length=20, verbose_name='套餐名', default=None)
    PackageTheme = models.ForeignKey(PackageTheme, on_delete=models.CASCADE)
    Dish = models.ManyToManyField(Dish)
    CostPrice = models.FloatField(verbose_name='成本价')
    Price = models.FloatField(verbose_name='标价')
    Sales = models.IntegerField(verbose_name='销量')
    img = models.CharField(max_length=500, verbose_name='图片地址', blank=True, null=True)

    class Meta:
        verbose_name_plural = "套餐详情"

    def __str__(self):
        return self.PackageName


class OrderList(models.Model):
    # Customer = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    customer = models.CharField(max_length=15, null=True)
    CreateTime = models.DateTimeField(auto_now_add=True)
    Dish = models.ManyToManyField(Dish, blank=True, null=True)
    Package = models.ManyToManyField(Package, blank=True, null=True)

    class Meta:
        verbose_name_plural = "订单信息"




