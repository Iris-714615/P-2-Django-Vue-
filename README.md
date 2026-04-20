# P-2-Django-Vue-
 搭建Django框架及Vue框架
# P2 项目 在线管理系统

## 步骤一：需求分析

**以文章列表原型图为例**：实现下面的功能

创建模型的时候要注意 两个表  (上传人一，文章多)

实现**文章列表功能** 能够**分页** 能够**搜索**（时间段 关键词 上传人），能够在文章列表中展示出**上传人**

添加的时候 将**上传人渲染为下拉菜单**

实现**上传封面**的功能(上传文件)

实现文章的**添加**  

实现文章的**编辑**

实现文章的**逻辑删除**

实现文章的**批量删除**

## 步骤二：接口文档

1、文章列表
路径/article/list/
方法get
请求参数 page  size  keyword(标题、内容） start  end  people上传人           ordering 排序   isable禁用
响应 {count :  resultes:[]...}
http://127.0.0.1:8000/article/list/

2、文章添加
路径/article/list/
方法post
请求参数 title cover people  intro
响应 {当前添加数据}/验证错误
http://127.0.0.1:8000/article/list/

3、文章编辑
  ○ 路径 /article/list/id/
  ○ 请求方法  put
  ○ 请求参数  {"能修改参数"}  title cover people  intro
  ○ 响应 {修改成功、数据不存在……}
http://127.0.0.1:8000/article/list/5/

4、逻辑删除
  ○ 路径 /article/delete/
  ○ 请求方法  put
  ○ 请求参数 id 主键
  ○ 响应 {删除成功、数据不存在……}
http://127.0.0.1:8000/article/delete/10/

5、批量删除
  ○ 路径 /article/delmany/
  ○ 请求方法  put
  ○ 请求参数  ids :[1,2,3]
  ○ 响应 {删除成功 、失败}
http://127.0.0.1:8000/article/delmany/

6、文件上传

- 路径 /article//upload/
- 请求方法 post
- 请求参数 file 选择的文件
- 响应 {“url”:“路径”,code:200}/{"msg":错误信息，code:400}


7、禁用

- 路径 /article/change/id/
- 请求方法 put
- 请求参数  无
- 响应 设置成功  失败


8、上传人列表(关联表)

- 路径 /article/author/
- 请求方法 get
- 请求参数 无
- 响应 [{},{}]

---

```markdown
# Django + Vue3 + Element Plus 全栈开发步骤指南

> 适用于管理后台常见功能：列表分页、条件搜索、添加（含文件上传）、编辑、逻辑删除、批量删除。

## 目录

- [一、技术栈与环境准备](#一技术栈与环境准备)
- [二、后端 Django 开发步骤](#二后端-django-开发步骤)
  - [1. 项目初始化与配置](#1-项目初始化与配置)
  - [2. 定义模型](#2-定义模型)
  - [3. 序列化器](#3-序列化器)
  - [4. 视图集与分页](#4-视图集与分页)
  - [5. 搜索过滤](#5-搜索过滤)
  - [6. 文件上传接口](#6-文件上传接口)
  - [7. 逻辑删除实现](#7-逻辑删除实现)
  - [8. 批量删除接口](#8-批量删除接口)
  - [9. 路由注册](#9-路由注册)
- [三、前端 Vue3 开发步骤](#三前端-vue3-开发步骤)
  - [1. 项目初始化与依赖](#1-项目初始化与依赖)
  - [2. Axios 封装](#2-axios-封装)
  - [3. API 接口定义](#3-api-接口定义)
  - [4. 列表展示与分页](#4-列表展示与分页)
  - [5. 搜索表单（含下拉菜单）](#5-搜索表单含下拉菜单)
  - [6. 添加功能（含文件上传）](#6-添加功能含文件上传)
  - [7. 编辑功能](#7-编辑功能)
  - [8. 逻辑删除](#8-逻辑删除)
  - [9. 批量删除](#9-批量删除)
- [四、完整组件代码参考](#四完整组件代码参考)
- [五、运行项目](#五运行项目)

---

## 一、技术栈与环境准备

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端 | Django + Django REST Framework | Django 4.x, DRF 3.14+ |
| 数据库 | SQLite（开发）/ MySQL（生产） | - |
| 前端 | Vue3 + Vite + Element Plus | Vue 3.3+, Element Plus 2.4+ |
| HTTP 库 | Axios | ^1.6.0 |

**安装命令：**
​```bash
# 后端
pip install django djangorestframework django-cors-headers pillow

# 前端
npm create vite@latest frontend -- --template vue
cd frontend
npm install element-plus axios
```

---

## 步骤三、后端 Django 开发

### 1. 项目初始化与配置

```bash
django-admin startproject backend
cd backend
python manage.py startapp api
```

**settings.py 关键配置：*

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

# 开发环境允许跨域
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_ROOT = BASE_DIR / 'uploads'
MEDIA_URL = '/uploads/'

```

### 2. 定义模型

以文章管理为例（包含软删除字段）：

```python
# api/models.py
from django.db import models

class Category(models.Model):
    """分类表"""
    name = models.CharField(max_length=50, verbose_name='分类名称')
	class Meta:
        db_table = "category"
    def __str__(self):
        return self.name

class Article(models.Model):
    """文章表"""
    title = models.CharField(max_length=100, verbose_name='标题')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    cover = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name='封面')
    content = models.TextField(null=True,verbose_name='内容')
    status = models.CharField(max_length=10, choices=[('on','上架'),('off','下架')], default='on')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "article"
    def __str__(self):
        return self.title
```

执行迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 序列化器

```python
# api/serializers.py
from rest_framework import serializers
from .models import Category, Article

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id', 'create_time']
```

### 4. 视图集与分页

```python
# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .models import Category, Article
from .serializers import CategorySerializer, ArticleSerializer
from django.db.models import Q

class ArticlePagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 100

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.filter(is_delete=False)
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
```

### 5. 搜索过滤

在 `ArticleViewSet` 中重写 `get_queryset`：

```python
def get_queryset(self):
    query = Q()
    title = self.request.query_params.get('title')
    category = self.request.query_params.get('category')
    status = self.request.query_params.get('status')
    ordering = self.request.query_params.get('ordering')

    if title:
        query &= Q(title__icontains=title)
    if category:
        query &= Q(category=category)
    if status:
        query &= Q(status=status)
    if ordering:
        return self.queryset.filter(query).order_by(ordering) 
    return self.queryset.filter(query)
```

### 6. 文件上传接口

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class UploadImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.data.get('file')
        if not file:
            return Response({'code': 400, 'msg': '未选择文件'})
        if not file.name.endswith((".jpg", ".png", ".jpeg")):
            return Response({"msg": "请选择正确的文件格式", "code": 400})
        if file.size > 2 * 1024 * 1024:
            return Response({"msg": "请上传小于2MB的文件", "code": 400})
        # 使用当前的时间和日期作为名字
        # old_type = file.name.split(".")[-1]
        # new_name = time.strftime("%Y%m%d%H%M%S")+"."+old_type
        # path = default_storage.save("article/" + new_name, file)
        path = default_storage.save("article/" + file.name, file)
        url = "http://127.0.0.1:8000/uploads/" + path
        return Response({"url": url, "code": 200,"msg":"上传成功"})
```

### 7. 逻辑删除实现

```python
class ArticleDelete(APIView):
    def put(self,request,pk):
        info = models.Article.objects.filter(id=pk).first()
        if not info:
            return Response({"msg":"没有该文章","code":400})
        info.is_delete = True
        info.save()
        return Response({"msg":"删除成功","code":200})
```

### 8. 批量删除接口

```python
class ArticleDelmany(APIView):
    def put(self,request):
        ids = request.data.get("ids")
        if not ids:
            return Response({"msg":"请选择要删除的数据","code":400})
        models.Article.objects.filter(id__in=ids).update(is_delete=True)
        return Response({"msg":"删除成功","code":200})
```

### 9. 扩展接口

```python
# ----------  上下架切换(需在模型中设置相应字段) ----------
class Status(APIView):
    def put(self, request, pk):
        info = models.Article.objects.filter(id=pk).first()
        if not info:
            return Response({"code": 400, "msg": "该信息不存在"})
        info.status = not info.status
        info.save()
        return Response({"code": 200, "msg": "状态更新成功"})



# ----------  加价（增加余额） (需在模型中设置相应字段)----------
class AddPrice(APIView):
    def put(self, request, pk):
        price = float(request.data.get("price"))
        info = models.Article.objects.filter(id=pk).first()
        if not info:
            return Response({"code": 400, "msg": "该信息不存在"})
        newprice = float(info.nowprice)+price
        if newprice >= info.price:
            return Response({"code": 400, "msg": "价格不能大于原价"})
        info.nowprice = newprice
        info.save()
        return Response({"code": 200, "msg": f"加价成功，当前余额：{info.nowprice}"})


# ----------  减价（减少余额）(需在模型中设置相应字段) ----------
class CutPrice(APIView):
    def put(self, request, pk):
        price = float(request.data.get("price"))
        info = models.Course.objects.filter(id=pk).first()
        if not info:
            return Response({"code": 400, "msg": "该信息不存在"})
        newprice = float(info.nowprice)-price
        if newprice <= 0:
            return Response({"code": 400, "msg": "金额必须大于0"})
        info.nowprice = newprice
        info.save()
        return Response({"code": 200, "msg": f"减价成功，当前余额：{info.nowprice}"})


# ----------  冻结（仅会员类型且余额为负） ----------
class Freeze(APIView):
    def put(self, request, pk):
        info = models.Course.objects.filter(id=pk).first()
        if not info:
            return Response({"code": 400, "msg": "该信息不存在"})
        if info.studytype != 2:
            return Response({"code": 400, "msg": "只有会员类型的课程才能冻结"})
        if float(info.balance) >= 0:
            return Response({"code": 400, "msg": "余额为负数时才能冻结"})
        # 这里可以设置一个冻结状态字段，我们仅模拟成功返回
        info.is_delete = True
        info.save()
        return Response({"code": 200, "msg": "冻结成功"})
```

### 10. 路由注册

```python
# api/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, ArticleViewSet, UploadImageView

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', UploadImageView.as_view()),
    path("delete/<int:pk>/",views.ArticleDelete.as_view()),
    path("delmany/",views.ArticleDelmany.as_view()),
    path("status/<int:pk>/",views.Status.as_view()),
    path("add/<int:pk>/",views.AddPrice.as_view()),
    path("cut/<int:pk>/",views.CutPrice.as_view()),
    path("freeze/<int:pk>/",views.Freeze.as_view()),
]
urlpatterns += router.urls

# 在 backend/urls.py 中：
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"uploads/(?P<path>.*)",serve,{'document_root':settings.MEDIA_ROOT}),
    path('api/',include('api.urls')),
]
```

---

## 步骤四、前端 Vue3 开发

### 1. 项目初始化与依赖

```bash
npm install
npm install element-plus axios
```

在 `main.js` 中引入 Element Plus：

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.mount('#app')
```

### 2. Axios 封装

创建 `src/utils/request.js`：

```javascript
import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  timeout: 10000
})

// 响应拦截器（可选）
request.interceptors.response.use(
  response => response,
  error => {
    console.error('请求错误', error)
    return Promise.reject(error)
  }
)

export default request
```

### 3. API 接口定义

创建 `src/api/article.js`：

```javascript
import request from '@/utils/request'

// 分类
export const getCategories = () => request.get('categories/')

// 文章列表
export const getArticles = (params) => request.get('articles/', { params })

// 添加文章
export const addArticle = (data) => request.post('articles/', data)

// 编辑文章
export const updateArticle = (id, data) => request.put(`articles/${id}/`, data)

// 删除文章（逻辑删除）
export const deleteArticle = (id) => request.delete(`articles/${id}/`)

// 批量删除
export const batchDeleteArticles = (ids) => request.post('articles/batch_delete/', { ids })

// 图片上传
export const uploadImage = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('upload/', formData)
}
```

### 4. 列表展示与分页

```vue
<template>
  <div>
    <!-- 表格 -->
    <el-table :data="tableData" border>
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="category_name" label="分类" />
      <el-table-column prop="status_display" label="状态" />
      <el-table-column prop="create_time" label="创建时间" />
      <!-- 操作列后续添加 -->
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="query.page"
      v-model:page-size="query.size"
      :total="total"
      layout="total, sizes, prev, pager, next"
      @size-change="fetchData"
      @current-change="fetchData"
      style="margin-top:20px; justify-content:flex-end"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getArticles } from '@/api/article'

const tableData = ref([])
const total = ref(0)
const query = reactive({ page: 1, size: 10 })

const fetchData = async () => {
  const res = await getArticles(query)
  tableData.value = res.data.results
  total.value = res.data.count
}

onMounted(fetchData)
</script>
```

### 5. 搜索表单（含下拉菜单）

```vue
<template>
  <div>
    <!-- 搜索区 -->
    <el-form :inline="true" :model="query">
      <el-form-item label="标题">
        <el-input v-model="query.title" placeholder="请输入" clearable />
      </el-form-item>
      <el-form-item label="分类">
        <el-select v-model="query.category" clearable>
          <el-option v-for="item in categoryList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" clearable>
          <el-option label="上架" value="on" />
          <el-option label="下架" value="off" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 表格和分页... -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories } from '@/api/article'

const categoryList = ref([])
const query = reactive({
  page: 1,
  size: 10,
  title: '',
  category: '',
  status: ''
})

const fetchCategories = async () => {
  const res = await getCategories()
  categoryList.value = res.data
}

const handleSearch = () => {
  query.page = 1
  fetchData()
}

const handleReset = () => {
  query.title = ''
  query.category = ''
  query.status = ''
  query.page = 1
  fetchData()
}

onMounted(() => {
  fetchCategories()
  fetchData()
})
</script>
```

### 6. 添加功能（含文件上传）

#### 6.1 添加对话框模板

```vue
<template>
  <!-- 添加按钮 -->
  <el-button type="primary" @click="openAddDialog">添加文章</el-button>

  <!-- 对话框 -->
  <el-dialog v-model="dialogVisible" title="添加文章" width="600px">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="分类" prop="category">
        <el-select v-model="form.category">
          <el-option v-for="c in categoryList" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="封面图" prop="cover">
        <el-upload
          class="avatar-uploader"
          action="http://127.0.0.1:8000/api/upload/"
          :show-file-list="false"
          :on-success="handleUploadSuccess"
          :before-upload="beforeUpload"
        >
          <img v-if="form.cover" :src="form.cover" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload>
      </el-form-item>
      <el-form-item label="状态">
        <el-radio-group v-model="form.status">
          <el-radio value="on">上架</el-radio>
          <el-radio value="off">下架</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitForm">保存</el-button>
    </template>
  </el-dialog>
</template>
```

#### 6.2 脚本逻辑

```javascript
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { addArticle, uploadImage } from '@/api/article'

const dialogVisible = ref(false)
const formRef = ref()
const form = reactive({
  title: '',
  category: null,
  cover: '',
  status: 'off'
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

const openAddDialog = () => {
  Object.assign(form, { title: '', category: null, cover: '', status: 'off' })
  dialogVisible.value = true
}

const handleUploadSuccess = (res) => {
  if (res.code === 200) {
    form.cover = res.url
    formRef.value?.clearValidate('cover')
  } else {
    ElMessage.error(res.msg)
  }
}

const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt500K = file.size / 1024 < 500
  if (!isImage) ElMessage.error('只能上传图片文件')
  if (!isLt500K) ElMessage.error('图片不能超过500KB')
  return isImage && isLt500K
}

const submitForm = async () => {
  await formRef.value.validate()
  await addArticle(form)
  ElMessage.success('添加成功')
  dialogVisible.value = false
  fetchData()
}
```

### 7. 编辑功能

在表格操作列添加编辑按钮，并实现编辑逻辑：

```vue
<el-table-column label="操作" width="200">
  <template #default="{ row }">
    <el-button link @click="openEditDialog(row)">编辑</el-button>
    <!-- 其他按钮... -->
  </template>
</el-table-column>
```

```javascript
const openEditDialog = (row) => {
  dialogTitle.value = '编辑文章'
  // 注意：需要深拷贝或只复制需要的字段，避免引用问题
  Object.assign(form, {
    id: row.id,
    title: row.title,
    category: row.category,
    cover: row.cover,
    status: row.status
  })
  dialogVisible.value = true
}

// 修改提交方法，判断是否存在 id
const submitForm = async () => {
  await formRef.value.validate()
  if (form.id) {
    await updateArticle(form.id, form)
  } else {
    await addArticle(form)
  }
  ElMessage.success('保存成功')
  dialogVisible.value = false
  fetchData()
}
```

### 8. 逻辑删除

```javascript
import { ElMessageBox } from 'element-plus'
import { deleteArticle } from '@/api/article'

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该文章吗？', '提示', { type: 'warning' })
  await deleteArticle(id)
  ElMessage.success('删除成功')
  fetchData()
}
```

### 9. 批量删除

表格增加多选列：

```vue
<el-table :data="tableData" @selection-change="handleSelectionChange">
  <el-table-column type="selection" width="55" />
  <!-- 其他列 -->
</el-table>

<el-button type="danger" :disabled="selectedIds.length === 0" @click="batchDelete">
  批量删除
</el-button>
```

```javascript
const selectedIds = ref([])

const handleSelectionChange = (selection) => {
  selectedIds.value = selection.map(item => item.id)
}

const batchDelete = async () => {
  await ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 条数据吗？`, '批量删除', { type: 'warning' })
  await batchDeleteArticles(selectedIds.value)
  ElMessage.success('批量删除成功')
  selectedIds.value = []
  fetchData()
}
```

---### **10、完整组件代码参考**

将上述所有片段整合后的 `ArticleManage.vue` 完整代码（包含样式）：

```vue
<template>
  <div class="article-manage">
    <!-- 搜索区 -->
    <el-form :inline="true" :model="query" class="search-form">
     <p>时间段搜索
        <el-date-picker
        v-model="query.start"
        type="date"
        placeholder="开始时间"
        value-format="YYYY-MM-DD"
      />
       <el-date-picker
        v-model="query.end"
        type="date"
        placeholder="结束时间"
        value-format="YYYY-MM-DD"
      /></p>
      <el-form-item label="标题">
        <el-input v-model="query.title" placeholder="请输入" clearable />
      </el-form-item>
      <el-form-item label="分类">
        <el-select v-model="query.category" clearable>
          <el-option v-for="item in categoryList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" clearable>
          <el-option label="上架" value="on" />
          <el-option label="下架" value="off" />
        </el-select>
      </el-form-item>
      <el-form-item label="排序">
        <el-select v-model="query.ordering" placeholder="排序" style="width: 240px">
           <el-option label="上传时间" value="add_time" />
           <el-option label="最新" value="-id" />
            </el-select>  
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 操作按钮 -->
    <div class="action-bar">
      <el-button type="primary" @click="openAddDialog">添加文章</el-button>
      <el-button type="danger" :disabled="selectedIds.length === 0" @click="batchDelete">批量删除</el-button>
    </div>

    <!-- 表格 -->
    <el-table :data="tableData" border @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="category_name" label="分类" />
      <el-table-column prop="status_display" label="状态" />
      <el-table-column prop="create_time" label="创建时间" width="180" />
      <el-table-column label="封面" width="100">
        <template #default="{ row }">
          <el-image v-if="row.cover" :src="row.cover" style="width:60px;height:60px" fit="cover" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link @click="openEditDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="query.page"
      v-model:page-size="query.size"
      :total="total"
      layout="total, sizes, prev, pager, next"
      @size-change="fetchData"
      @current-change="fetchData"
      class="pagination"
    />

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category">
            <el-option v-for="c in categoryList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="封面图">
          <el-upload
            class="avatar-uploader"
            action="http://127.0.0.1:8000/api/upload/"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <img v-if="form.cover" :src="form.cover" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio value="on">上架</el-radio>
            <el-radio value="off">下架</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import {
  getCategories,
  getArticles,
  addArticle,
  updateArticle,
  deleteArticle,
  batchDeleteArticles
} from '@/api/article'

// 查询参数
const query = reactive({
  page: 1,
  size: 10,
  title: '',
  category: '',
  status: '',
  ordering:'',
})

// 表格数据
const tableData = ref([])
const total = ref(0)
const selectedIds = ref([])

// 分类下拉
const categoryList = ref([])

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('添加文章')
const formRef = ref()
const form = reactive({
  id: null,
  title: '',
  category: null,
  cover: '',
  status: 'off'
})

// 表单校验
const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

// 获取分类
const fetchCategories = async () => {
  const res = await getCategories()
  categoryList.value = res.data
}

// 获取列表
const fetchData = async () => {
  const res = await getArticles(query)
  tableData.value = res.data.results
  total.value = res.data.count
}

// 搜索
const handleSearch = () => {
  query.page = 1
  fetchData()
}

// 重置
const handleReset = () => {
  query.title = ''
  query.category = ''
  query.status = ''
  query.page = 1
  fetchData()
}

// 打开添加对话框
const openAddDialog = () => {
  dialogTitle.value = '添加文章'
  Object.assign(form, { id: null, title: '', category: null, cover: '', status: 'off' })
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (row) => {
  dialogTitle.value = '编辑文章'
  Object.assign(form, {
    id: row.id,
    title: row.title,
    category: row.category,
    cover: row.cover,
    status: row.status
  })
  dialogVisible.value = true
}

// 上传成功回调
const handleUploadSuccess = (res) => {
  if (res.code === 200) {
    form.cover = res.url
  } else {
    ElMessage.error(res.msg)
  }
}

// 上传前校验
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt500K = file.size / 1024 < 500
  if (!isImage) ElMessage.error('只能上传图片文件')
  if (!isLt500K) ElMessage.error('图片不能超过500KB')
  return isImage && isLt500K
}

// 提交表单
const submitForm = async () => {
  await formRef.value.validate()
  if (form.id) {
    await updateArticle(form.id, form)
  } else {
    await addArticle(form)
  }
  ElMessage.success('保存成功')
  dialogVisible.value = false
  fetchData()
}

// 单个删除
const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该文章吗？', '提示', { type: 'warning' })
  await deleteArticle(id)
  ElMessage.success('删除成功')
  fetchData()
}

// 批量删除
const handleSelectionChange = (selection) => {
  selectedIds.value = selection.map(item => item.id)
}

const batchDelete = async () => {
  await ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 条数据吗？`, '批量删除', { type: 'warning' })
  await batchDeleteArticles(selectedIds.value)
  ElMessage.success('批量删除成功')
  selectedIds.value = []
  fetchData()
}

onMounted(() => {
  fetchCategories()
  fetchData()
})
</script>

<style scoped>
.article-manage { padding: 20px; }
.search-form { margin-bottom: 20px; }
.action-bar { margin-bottom: 20px; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
.avatar-uploader .avatar { width: 178px; height: 178px; display: block; object-fit: cover; }
.avatar-uploader :deep(.el-upload) { border: 1px dashed #d9d9d9; border-radius: 6px; cursor: pointer; }
.avatar-uploader-icon { font-size: 28px; color: #8c939d; width: 178px; height: 178px; line-height: 178px; text-align: center; }
</style>
```

---

## 步骤五、运行项目

### 后端

```bash
cd backend
python manage.py runserver
```

### 前端

```bash
cd frontend
npm run dev
```

访问 `http://localhost:5173` 即可看到完整的管理界面。

---

> **备注**：以上代码涵盖了 Django+Vue3+Element Plus 开发中最常见的六个功能模块，可直接作为项目基础脚手架使用。
