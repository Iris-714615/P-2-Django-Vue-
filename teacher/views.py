from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from teacher import models,serializers
from django.core.files.storage import default_storage
# Create your views here.

class TeacherPage(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 100

class TeacherList(ModelViewSet):
    queryset = models.Teacher.objects.filter(is_delete=False)
    serializer_class = serializers.TeacherSerializer
    pagination_class = TeacherPage
    def get_queryset(self):
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        keyword = self.request.query_params.get('keyword')
        query = Q()
        if start and end:
            query &= Q(add_time__range=(start,end))
        if keyword:
            query &= Q(account=keyword)|Q(name=keyword)|Q(phone=keyword)
        return self.queryset.filter(query)

class TeacherDelete(APIView):
    def put(self, request,pk):
        info = models.Teacher.objects.filter(id=pk).first()
        if not info:
            return Response({"msg":"没有该讲师","code":400})
        info.is_delete = True
        info.save()
        return Response({"msg":"删除成功","code":200})

class TeacherDelmany(APIView):
    def put(self, request):
        ids = request.data.get("ids")
        if not ids:
            return Response({"msg":"请选择要删除的数据","code":400})
        models.Teacher.objects.filter(id__in=ids).update(is_delete=True)
        return Response({"msg":"删除成功","code":200})


class Upload(APIView):
    def post(self, request):
        fileobj = request.data.get("file")
        if not fileobj:
            return Response({"msg":"请选择上传文件","code":400})
        allowtype = ["jpg","png","jpeg"]
        type = fileobj.name.split(".")[-1]
        if type not in allowtype:
            return Response({"msg":"请上传正确的文件格式","code":400})
        if fileobj.size>2*1024*1024:
            return Response({"msg": "请上传小于2MB的文件", "code": 400})
        path = default_storage.save("teacher/"+fileobj.name, fileobj)
        url = "http://127.0.0.1:8000/uploads/" + path
        return Response({"url":url,"code":200})








