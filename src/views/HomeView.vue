
<template>
 <div>
    <el-container>
      <el-header>
         <div class="header-content">
        <p v-if="username">{{username}},欢迎你</p>
        <el-button type="primary" @click="logout">注销</el-button>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
              <el-menu
                    :uniqueOpened="true"
                    default-active="2"
                    class="el-menu-vertical-demo"
                    background-color="#545c64"
                    text-color="#fff"
                    active-text-color="#ffd04b"
                    router
                  >
            <el-sub-menu index="1">
              <template #title>
                <i class="el-icon-location"></i>
                <span>用户管理</span>
              </template>
                <el-menu-item index="/student">用户列表</el-menu-item>
                <el-menu-item index="/teacher">教师列表</el-menu-item>
                <el-menu-item index="/article">文章列表</el-menu-item>
              </el-sub-menu>
            </el-menu>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<script setup>

import {ref} from "vue"
import {useRouter} from "vue-router"
import {ElMessage} from 'element-plus'
const router=useRouter()

let username=sessionStorage.getItem("username")||""
if(username==""){
    ElMessage.error("请先登录")
    router.push("/login")
}

const logout=()=>{
    sessionStorage.removeItem("username")
    sessionStorage.removeItem("userid")
    ElMessage.success("退出成功")
    router.push("/login")
}
</script>

<style scoped>
.home, .el-container {
  height: 100%;
}
.el-header {
  background-color: #b3c0d1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
}
.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}
.el-aside {
  background-color: #545c64;
}
.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
