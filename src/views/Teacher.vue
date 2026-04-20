<script setup>
import {onMounted, ref} from "vue"
import axios from "axios";
import {ElMessage} from "element-plus"

let query=ref({
    "page":1,
    "size":2,
    "start":"",
    "end":"",
    "keyword":""
})
let teacherlist=ref([])
let total=ref(0)
const getdata=()=>{
    axios.get("http://127.0.0.1:8000/teacher/list/",{
        params:query.value
    }).then(res=>{
        teacherlist.value=res.data.results
        total.value=res.data.count
    }).catch(err=>{ElMessage.error("请求失败：" + (err.response?.data?.msg || "服务器错误"))
})
}
onMounted(()=>{
    getdata()
})
const  handleSizeChange=(size)=>{
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
        
    }
    getdata()
}
const handleDelete=(id)=>{
    if(confirm("确定删除吗？")){
        axios.put(`http://127.0.0.1:8000/teacher/delete/${id}/`).then(res=>{ 
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
  obj.value.headimg=res.url
}
const save=()=>{ 
    if(obj.value.name==""||obj.value.headimg==""||obj.value.intro==""){
        return ElMessage.error("请填写完整信息")
    }
    axios.put(`http://127.0.0.1:8000/teacher/list/${obj.value.id}/`,obj.value).then(res=>{ 
        if(res.data){
        ElMessage.success("添加成功")
        dialogFormVisible.value = false
        getdata()}
}).catch(err=>{
    ElMessage.error("添加失败")
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
    axios.put("http://127.0.0.1:8000/teacher/delmany/",{ids:ids}).then(res=>{
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
        <router-link to="addteacher">添加讲师</router-link>
    </div>
    <el-card>
	<p>
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
	<p>
      <el-input v-model="query.keyword" style="width: 240px" placeholder="输入账号、昵称、手机号" />
      	</p>
	<p>
        <el-button type="primary" @click="getdata">查询</el-button>
      <el-button @click="reset">重置</el-button>
	</p>
    </el-card>
    <el-card>
        <el-table :data="teacherlist" style="width: 100%" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" />
            <el-table-column property="account" label="账号" />
            <el-table-column property="name" label="名称" />
            <el-table-column property="headimg" label="头像" >
                <template #default="scope">
                <el-image style="width: 100px; height: 100px" :src="scope.row.headimg" :fit="fit" />
                </template>
            </el-table-column>
            <el-table-column property="intro" label="简介" />
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
                <el-form-item label="讲师账号">
                <el-input v-model="obj.account" />
            </el-form-item>
            <el-form-item label="讲师姓名">
                <el-input v-model="obj.name" />
            </el-form-item>
            <el-form-item label="讲师头像">
            <el-upload
                class="avatar-uploader"
                action="http://127.0.0.1:8000/teacher/upload/"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"               
                >
                <img v-if="obj.headimg" :src="obj.headimg" class="avatar" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            </el-upload>
            </el-form-item>
            <el-form-item label="入职时间">
                <el-input v-model="obj.add_time" />
            </el-form-item>
             <el-form-item label="个人简介">
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
