<template>
    <div>
    {{ peoplelist }}
        <el-card>
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
                <el-form-item>
                <el-button type="primary" @click="onSubmit">添加</el-button>
                <el-button @click="clear">取消</el-button>
            </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
const router = useRouter()

let obj=ref({
    "title":"",
    "cover":"",
    "intro":"",    
    "people":""
})
let peoplelist=ref([])
const getpeople=()=>{
    axios.get("http://127.0.0.1:8000/article/people/").then(res=>{  
            peoplelist.value=res.data   
    })
}
onMounted(()=>{
    getpeople()
})
const handleAvatarSuccess=(res)=>{
  if(res.code==400){
    return ElMessage.error(res.msg)
  }
  obj.value.cover=res.url
}

const onSubmit=()=>{
    if(obj.value.title==""||obj.value.cover==""||obj.value.intro==""){
        return ElMessage.error("请填写完整信息")
    }
    axios.post("http://127.0.0.1:8000/article/list/",obj.value,{withCredentials:true}).then(res=>{
        if(res.data){
            ElMessage.success("添加成功")
            router.push("/article")
        }
        }).catch(err=>{
            console.log(err.response)
            let errdata=err.response.data
            for(let i in errdata){
                ElMessage.error(i+":"+errdata[i])
            }     
        })
}
const clear=()=>{
    obj.value={
        "title":"",
        "cover":"",
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
