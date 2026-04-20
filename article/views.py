from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.core.files.storage import default_storage
from rest_framework.generics import ListAPIView
from article import models, serializers

import time

# Create your views here.
class ArticlePage(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 100

class ArticleList(ModelViewSet):
    queryset = models.Article.objects.filter(is_delete=False)
    serializer_class = serializers.ArticleSerializer
    pagination_class = ArticlePage
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        people = self.request.query_params.get('people')
        ordering = self.request.query_params.get('ordering')
        query = Q()
        if keyword:
            query &= Q(title__icontains=keyword)|Q(intro__icontains=keyword)
        if people:
            query &= Q(people__id=people)
        if start :
            query &= Q(add_time__gte=start)
        if end:
            query &= Q(add_time__lte=end)
        if ordering:
            return self.queryset.filter(query).order_by(ordering)
        return self.queryset.filter(query)


class ArticleDelete(APIView):
    def put(self,request,pk):
        info = models.Article.objects.filter(id=pk).first()
        if not info:
            return Response({"msg":"没有该文章","code":400})
        info.is_delete = True
        info.save()
        return Response({"msg":"删除成功","code":200})

class ArticleDelmany(APIView):
    def put(self,request):
        ids = request.data.get("ids")
        if not ids:
            return Response({"msg":"请选择要删除的数据","code":400})
        models.Article.objects.filter(id__in=ids).update(is_delete=True)
        return Response({"msg":"删除成功","code":200})

class ArticleUpload(APIView):
    def post(self,request):
        fileobj = request.data.get("file")
        if not fileobj:
            return Response({"msg":"请选择上传文件","code":400})
        if  not fileobj.name.endswith((".jpg",".png",".jpeg")):
            return Response({"msg":"请选择正确的文件格式","code":400})
        if fileobj.size>2*1024*1024:
            return Response({"msg":"请上传小于2MB的文件","code":400})
        #使用当前的时间和日期作为名字
        # old_type = fileobj.name.split(".")[-1]
        # new_name = time.strftime("%Y%m%d%H%M%S")+"."+old_type
        # path = default_storage.save("article/" + new_name, fileobj)
        path = default_storage.save("article/"+fileobj.name, fileobj)
        url = "http://127.0.0.1:8000/uploads/"+path
        return Response({"url":url,"code":200})

class People(ListAPIView):
    queryset = models.People.objects.all()
    serializer_class = serializers.PeopleSerializer