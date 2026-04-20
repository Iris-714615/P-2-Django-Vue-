<script setup>
import {onMounted, ref} from "vue"
import axios from "axios";
import {ElMessage} from "element-plus"
import { Plus } from '@element-plus/icons-vue'
import { el } from "element-plus/es/locale/index.mjs";

let query=ref({
    "page":1,
    "size":2,
    "start":"",
    "end":"",
    "keyword":"",
    "people":"",
    "ordering":""
})
let articlelist=ref([])
let total=ref(0)

let peoplelist=ref([])
const getpeople=()=>{
    axios.get("http://127.0.0.1:8000/article/people/").then(res=>{
            peoplelist.value=res.data
        
    })
}
const getdata=()=>{
    axios.get("http://127.0.0.1:8000/article/list/",{
        params:query.value
    }).then(res=>{
        articlelist.value=res.data.results
        total.value=res.data.count
    }).catch(err=>{ElMessage.error("请求失败：" + (err.response?.data?.msg || "服务器错误"))
})
}
onMounted(()=>{
    getdata()
    getpeople()
})
const handleSizeChange=(size)=>{
    query.value.size=size
    getdata()
}
const handleCurrentChange=(page)=>{
    query.value.page=page
    getdata()
}

const reset=()=>{
    query.value={
        "page":1,
        "size":2,
        "start":"",
        "end":"",
        "keyword":"",
        "people":"",
        "ordering":""
    }
    getdata()
}

const handleDelete=(id)=>{
    if(confirm("确定删除吗？")){
        axios.put(`http://127.0.0.1:8000/article/delete/${id}/`).then(res=>{ 
        if(res.data.code==200){
        ElMessage.success(res.data.msg)
        query.value.page=1
        getdata()}
})
    }
}
let dialogFormVisible=ref(false)
let obj = ref({})
const handleEdit=(info1)=>{
        dialogFormVisible.value = true
        obj.value = info1        
}
const handleAvatarSuccess=(res)=>{
  if(res.code==400){
    return ElMessage.error(res.msg)
  }
  obj.value.cover=res.url
}
const save=()=>{ 
    axios.put(`http://127.0.0.1:8000/article/list/${obj.value.id}/`,obj.value,{withCredentials:true}).then(res=>{ 
        if(res.data){
        ElMessage.success("保存成功")
        dialogFormVisible.value = false
        getdata()}
}).catch(err=>{
   console.log(err.response)
   let errdata=err.response.data
   for(let i in errdata){
                ElMessage.error(i+":"+errdata[i])
            }
})
}

let select=ref([])
const handleSelectionChange=(val)=>{ 
    select.value = val
}
const delmany=()=>{ 
    if(select.value.length==0){
        return ElMessage.warning("请选择要删除的数据")
    }
    let ids=select.value.map(item=>item.id)
    axios.put("http://127.0.0.1:8000/article/delmany/",{ids:ids}).then(res=>{
        if(res.data.code==200){
        ElMessage.success(res.data.msg)
        query.value.page = 1
        getdata()
        } 
})
}

</script>

<template>
    <div> 
        <router-link to="addarticle">添加文章</router-link>
    </div>
    <el-card>
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
	<p> 关键词搜索
      <el-input v-model="query.keyword" style="width: 240px" placeholder="输入标题或其他关键字" />
      	</p>
        <p>筛选上传人
        <el-select v-model="query.people" placeholder="请选择上传人" style="width: 240px">
            <el-option
              v-for="item in peoplelist"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
          </p>
          <p>
            <el-select v-model="query.ordering" placeholder="排序" style="width: 240px">
                <el-option label="上传时间" value="add_time" />
                <el-option label="最新" value="-id" />
            </el-select>
          </p>
	<p>
        <el-button type="primary" @click="getdata">查询</el-button>
      <el-button @click="reset">重置</el-button>
	</p>
    </el-card>
    <el-card>
        <el-table :data="articlelist" style="width: 100%" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" />
            <el-table-column property="title" label="标题" />           
            <el-table-column property="cover" label="封面" >
                <template #default="scope">
                <el-image style="width: 100px; height: 100px" :src="scope.row.cover" :fit="fit" />
                </template>
            </el-table-column>
            <el-table-column property="uploader" label="上传人" />
            <el-table-column property="intro" label="描述" />
            <el-table-column property="add_time" label="添加时间" />
            <el-table-column label="操作" >
                <template #default="scope">
                <el-button type="primary" @click="handleEdit(scope.row)">编辑</el-button>
                <el-button type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        
        <el-pagination
            v-model:current-page="query.page"
            v-model:page-size="query.size"
            :page-sizes="[1, 2, 3, 4]"
            background
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
         />
         <hr>
         <el-button type="primary" @click="delmany">批量删除</el-button>
         <!-- <el-button type="primary" @click="exportdata">批量导出</el-button> -->
         
         
         <el-dialog v-model="dialogFormVisible" title="修改信息" width="600">
            <el-form :model="obj" label-width="auto" style="max-width: 500px">
                <el-form-item label="文章标题">
                <el-input v-model="obj.title" />
            </el-form-item>
            <el-form-item label="上传人">
          <el-select v-model="obj.people" placeholder="请选择上传人">
            <el-option
              v-for="item in peoplelist"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>          
        </el-form-item>
            <el-form-item label="文章封面">
            <el-upload
                class="avatar-uploader"
                action="http://127.0.0.1:8000/article/upload/"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"               
                >
                <img v-if="obj.cover" :src="obj.cover" class="avatar" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            </el-upload>
            </el-form-item>
            
             <el-form-item label="文章描述">
                <el-input v-model="obj.intro" type="textarea" />
                </el-form-item>
                </el-form>
          <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="save">保存</el-button>           
            </div>
            </template>
            
        </el-dialog>
    </el-card>
    
</template>

<style scoped>
.el-table{
    margin:10px
}
img{
    width: 100px;
    height: 100px;
}
.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409eff;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>
