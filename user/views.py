from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from user import serializers,models
from openpyxl import Workbook
from django.http import HttpResponse
from io import BytesIO
# Create your views here.

class User(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        info = models.User.objects.filter(username=username).first()
        if not info:
            return Response({"msg":"用户名错误","code":400})
        if password != info.password:
            return Response({"msg":"密码错误","code":400})
        return Response({"msg":"登陆成功","code":200,"data":{"id":info.id,"username":info.username,"password":info.password}})

class StudentPage(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 100

class StudentList(ModelViewSet):
    queryset = models.Student.objects.filter(is_delete=False)
    serializer_class = serializers.StudentSerializer
    pagination_class = StudentPage
    def get_queryset(self):
        search_key = self.request.query_params.get('search_key')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        status = self.request.query_params.get('status')
        query = Q()
        if start and end:
            query = query & Q(add_time__range=(start,end))
        if search_key:
            query = query & Q(no__icontains=search_key) | Q(name__icontains=search_key) | Q(phone__icontains=search_key)
        if status:
            query &= Q(status=status)
        return self.queryset.filter(query)

class StudentStatus(APIView):
    def put(self,request,pk):
        info = models.Student.objects.filter(id=pk).first()
        if not info:
            return Response({"msg":"没有该学员","code":400})
        info.status = not info.status
        info.save()
        return Response({"msg":"修改成功"})

class StudentDelete(APIView):
    def delete(self,request,pk):
        info = models.Student.objects.filter(id=pk).first()
        if not info:
            return Response({"msg":"没有该学员","code":400})
        info.is_delete = True
        info.save()
        return Response({"msg":"删除成功"})


class Delmany(APIView):
    def put(self,request):
        ids = request.data.get("ids")
        models.Student.objects.filter(id__in=ids).update(is_delete=True)
        return Response({"msg":"删除成功","code":200})


class Export(APIView):
    def get(self,request):
        ids = request.query_params.get("ids")
        ids = ids.split(",")
        infolist=models.Student.objects.filter(id__in=ids)
        wb=Workbook()
        ws=wb.active
        ws.append(["编号","昵称","电话"])
        for info in infolist:
            ws.append([info.id,info.name,info.phone])
        output=BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(output,content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment;filename='user_list.xlsx'"

        return response


