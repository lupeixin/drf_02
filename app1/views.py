from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render

# Create your views here.

# FBV: 函数视图 基于函数定义的逻辑视图函数
# CBV: 类视图 基于类定义的视图函数
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# @csrf_protect  #为某个视图单独开启csrf认证
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app1.models import User


@csrf_exempt  # 免除csrf认证
def user(request):
    if request.method == "GET":
        print(request.GET.get("username"))
        # TODO 查询用户相关的操作
        return HttpResponse("GET 访问成功")

    if request.method == "POST":
        print(request.POST.get("username"))
        # TODO 新增用户相关的操作
        return HttpResponse("POST 访问成功")

    if request.method == "PUT":
        print("PUT 更新成功")
        # TODO 更新用户相关的操作
        return HttpResponse("PUT 更新成功")

    if request.method == "DELETE":
        print("DELETE 删除成功")
        # TODO 删除用户相关的操作
        return HttpResponse("DELETE 删除成功")


@method_decorator(csrf_exempt, name='dispatch')  # 让类视图免除csrf认证
class UserView(View):

    def get(self, request, *args, **kwargs):
        print("GET  查询")
        return HttpResponse("GET success")

    def post(self, request, *args, **kwargs):
        print("POST  新增")
        return HttpResponse("post success")

    def put(self, request, *args, **kwargs):
        print("GET  更新")
        return HttpResponse("put success")

    def delete(self, request, *args, **kwargs):
        print("delete  删除")
        return HttpResponse("delete success")


@method_decorator(csrf_exempt, name='dispatch')
class StudentView(View):

    def get(self, request, *args, **kwargs):
        """
        查询用户接口
        :param request: 请求对象，要有查询用户的id
        :return: 查询后的结果
        """
        # 获取用户的id
        user_id = kwargs.get("id")
        if user_id:
            user = User.objects.filter(id=user_id).values("username", "password", "gender", "email").first()
            if user:
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user,

                })
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "查询用户不存在",
                })
        else:
            user_all = User.objects.all().values("username", "password", "gender", "email")
            if user_all:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_all),
                })
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "查询用户不存在",
                })

    def post(self, request, *args, **kwargs):

        """
        新增单个用户的接口
        :param request: 用户输入的信息
         :return: 新增的结果
        """
        name = request.POST.get("name")
        pwd = request.POST.get("pwd")
        email = request.POST.get("email")
        try:
            user = User.objects.create(username=name, password=pwd, email=email)
            if user:
                return JsonResponse({
                    "status": 200,
                    "message": "创建用户成功",
                    "results": {"username": user.username}
                })
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "创建用户失败",
                })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建用户失败",
            })


class UserAPIView(APIView):
    # 为某个类单独指定渲染器
    # 局部的渲染器比全局的优先级高
    renderer_classes = (JSONRenderer, )
    # 指定此视图接受的参数类型
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):  # DRF类视图中的request是经过封装后的request
        # 通过django原生的request对象来获取参数
        # 如果要访问django原生的request对象，可以通过_request来访问
        print(request._request.GET)  # 不推荐  了解即可

        # 可以通过DRF的request对象获取参数
        print(request.GET)

        # 可以通过 query_params来获取参数  DRF扩展的方法
        print(request.query_params)

        # 获取路径传参
        user_id = kwargs.get("id")

        return Response("DRF GET OK")

    def post(self, request, *args, **kwargs):
        # post请求传递参数的形式  form-data  www-urlencoded json
        print(request._request.POST, "33")  # django原生的request对象
        print(request.POST, "22")  # DRF封装后的request对象
        # DRF 扩展的请求参数  兼容性最强  可以接受任意类型的参数
        print(request.data, "11")

        return Response("DRF POST OK")



