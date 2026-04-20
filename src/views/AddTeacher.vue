<template>
    <div>
        <el-card>
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
                <el-form-item>
                <el-button type="primary" @click="onSubmit">添加</el-button>
                <el-button @click="clear">取消</el-button>
            </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
const router = useRouter()

let obj=ref({
    "name":"",
    "headimg":"",
    "intro":""
})
const handleAvatarSuccess = (res,file) => {
    if(res.code==200){
        ElMessage.success("上传成功")
        obj.value.headimg = res.url
    }else{
        ElMessage.error(res.msg)        
    }    
}

const onSubmit=()=>{
    if(obj.value.name==""||obj.value.headimg==""||obj.value.intro==""){
        return ElMessage.error("请填写完整信息")
    }
    axios.post("http://127.0.0.1:8000/teacher/list/",obj.value,{withCredentials:true}).then(res=>{
        if(res.data){
            ElMessage.success("添加成功")
            router.push("/teacher")
        }
        }).catch(err=>{
            ElMessage.error("添加失败")
        })
}
const clear=()=>{
    obj.value={
        "name":"",
        "headimg":"",
        "intro":""
    }
}
</script>

<style scoped>
.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>












