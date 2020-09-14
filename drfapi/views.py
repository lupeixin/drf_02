from rest_framework.response import Response
from rest_framework.views import APIView

from app1.models import User


class StudentAPIView(APIView):

    def get(self, request, *args, **kwargs):
        stu_id = kwargs.get("id")

        if stu_id:
            user = User.objects.filter(id=stu_id).values("username", "password", "gender", "email").first()
            if user:
                return Response({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user,

                })
            else:
                return Response({
                    "status": 500,
                    "message": "查询用户不存在",
                })
        else:
            user_all = User.objects.all().values("username", "password", "gender", "email")
            if user_all:
                return Response({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_all),
                })
            else:
                return Response({
                    "status": 500,
                    "message": "查询用户不存在",
                })

    def post(self,request, *args, **kwargs):
        data = request.data
        try:
            user = User.objects.create(username=data.name, password=data.pwd, email=data.email)
            if user:
                return Response({
                    "status": 200,
                    "message": "创建用户成功",
                    "results": {"username": user.username}
                })
            else:
                return Response({
                    "status": 500,
                    "message": "创建用户失败",
                })
        except:
            return Response({
                "status": 500,
                "message": "创建用户失败",
            })

    def put(self, request, *args, **kwargs):
        data = request.data
        if data.id:
            user = User.objects.first(id=1)
            user.username = data.name
            user.gender = data.gender
            user.password = data.password
            user.email = data.email
            return Response({
                "status": 200,
                "message": "创建用户成功",
                "results": {"username": user.username}
            })
