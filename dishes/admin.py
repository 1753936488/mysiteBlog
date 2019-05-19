from django.contrib import admin
from . import models


@admin.register(models.Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'DishName', 'CostPrice', 'Price', 'Sales', 'Moral', 'img', 'type', 'category')


@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):

    def show_all_dishName(self, obj):
        return [a.DishName for a in obj.Dish.all()]

    list_display = ('id', 'PackageName', 'PackageTheme', 'show_all_dishName', 'CostPrice', 'Price', 'Sales', 'img')


@admin.register(models.DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')


@admin.register(models.OrderList)
class OrderListAdmin(admin.ModelAdmin):

    def show_all_dishName(self, obj):
        return [a.DishName for a in obj.Dish.all()]

    def show_all_packageName(self, obj):
        return [a.PackageName for a in obj.Package.all()]

    list_display = ('id', 'customer', 'CreateTime', 'show_all_dishName', 'show_all_packageName')


@admin.register(models.PackageTheme)
class PackageThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'themeName')


# @admin.register(models.UserInfo)
# class UserInfoThemeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'userName', 'userNum', 'userAge', 'userSex')


@admin.register(models.DishCategory)
class DishCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
