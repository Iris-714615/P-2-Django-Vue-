<template>
    <div class="login-container" >
    <el-card class="login-card">
    
        欢迎来到在线教育管理系统
        <hr>
        请先登录
        <p>用户名：<el-input v-model="obj.username" placeholder="请输入内容" style="width:240px;"></el-input></p>
        <p>密码：<el-input v-model="obj.password" placeholder="请输入密码" style="width:240px;"></el-input></p>
        <p><el-button type="primary" @click="login">登录</el-button></p>    
    </el-card>
    </div>
</template>

<script setup>

import { ElMessage } from 'element-plus';
import {ref} from "vue"
import { Axios } from 'axios';
import { useRouter } from 'vue-router';
import axios from 'axios';
const router=useRouter()

let obj=ref( {
    "username":"",
    "password":""
    })

const login=()=>{
    if(obj.value.username==""||obj.value.password==""){
        return ElMessage.error("请输入用户名或者密码")
    }
    axios.post("http://127.0.0.1:8000/user/login/",obj.value).then(res=>{
        if(res.data.code==400){
            ElMessage.error(res.data.msg)
        }else{
            ElMessage.success("登录成功")
            sessionStorage.setItem("username",res.data.data.username)
            sessionStorage.setItem("userid",res.data.data.id)
            router.push("/")
        }
    })
}

</script>


<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  width: 400px;
  padding: 20px;
}
h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}
</style>
