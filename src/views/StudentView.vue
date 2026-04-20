<script setup>
import { ref,onMounted } from 'vue'
import axios from 'axios';
import { ElMessage } from 'element-plus';
let query = ref(  {
    "page": 1,
    "size": 2,
    "start":"",
    "end":"",
    "status": "",
    "search_key": ""
} )

let studentlist = ref([])
let total = ref(0)

let  time1 = ref("")

const getdata = ()=>{
    if(time1.value.length!=0){
        query.value.start = time1.value[0]
        query.value.end = time1.value[1]
    }

    axios.get('http://127.0.0.1:8000/user/student/',{params:query.value})
        .then(res=>{
            console.log(res)
            studentlist.value = res.data.results
            total.value = res.data.count
            
        })
        .catch(err=>{
            console.log(err)
            ElMessage.error("获取数据失败")
        })
}
onMounted(()=>{
    getdata()
})

const handleSizeChange=(size)=>{
    query.value.page = 1
    query.value.size = size
    getdata()
}

const handleCurrentChange=(num)=>{
    query.value.page = num
    getdata()
}

const handleReset=()=>{
    query.value = {
    "page": 1,
    "size": query.value.size,
    "start":"",
    "end":"",
    "status": "",
    "search_key": ""
    }
    getdata()
}
const statuschange=(id)=>{
    axios.put(`http://127.0.0.1:8000/user/status/${id}/`,{status:id.status})
    .then(res=>{
        ElMessage.success(res.data.msg)
        getdata()
    })
 
}
const handleDelete=(id)=>{
    if(confirm("确定删除该学员吗？")){
        axios.delete(`http://127.0.0.1:8000/user/delete/${id}/`)
        .then(res=>{if(res.data.code==200)
            {ElMessage.success(res.data.msg)
                query.value.page = 1
            }
            
            getdata()
        })
    }
}
let dialogFormVisible = ref(false)
let editForm = ref({})
const handleEdit=(info)=>{
   dialogFormVisible.value = true
   editForm.value = info
}
const handleEditSubmit=()=>{
    axios.put(`http://127.0.0.1:8000/user/student/${editForm.value.id}/`,editForm.value)
    .then(res=>{
        if(res.data){
        dialogFormVisible.value = false
        getdata()
    }
    })

}
let selectEmits = ref([])
const handleSelectionChange=(val)=>{
    selectEmits.value = val
}
const handleDeleteAll=()=>{
    if(selectEmits.value.length==0){
        return ElMessage.warning("请选择要删除的学员")
    }
    let ids = selectEmits.value.map(item=>item.id)
    axios.put("http://127.0.0.1:8000/user/delmany/",{ids:ids}).then(res=>{
        if(res.data.code==200){
            query.value.page = 1
            ElMessage.success(res.data.msg)
            getdata()
        }
})
}

const exportdata=()=>{
    if(selectEmits.value.length==0){
        return ElMessage.warning("请选择要导出的学员")
    }
    let ids = selectEmits.value.map(item=>item.id)
    window.open("http://127.0.0.1:8000/user/export/?ids="+ids.join(","))
}
</script>


<template>     
    <el-card>
    <p>注册时间：
          <el-date-picker
        v-model="time1"
        type="daterange"
        range-separator="To"
        format="YYYY/MM/DD"
        value-format="YYYY-MM-DD"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
            />
        
    </p>
   
    <p>手动搜索
     <el-input v-model="query.search_key" style="width: 240px" placeholder="请输入学员ID、昵称、手机号" />
    </p>
    <el-select v-model="query.status" placeholder="选择状态" style="width: 240px">
            <el-option
            label="禁用"
            value="1"
            />
            <el-option
            label="不禁用"
            value="0"
            />
    </el-select>

    <p>
        <el-button type="primary" @click="getdata">搜索</el-button>
        <el-button  @click="handleReset">重置</el-button>
    </p>
    </el-card>
    <el-card>
        <p>订单列表</p>
        <el-table :data="studentlist" style="width: 100%" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" />
            <el-table-column property="no" label="用户ID" width="120" />
            <el-table-column property="name" label="用户昵称" width="120" />
            <el-table-column property="phone" label="手机号" width="120" />
            <el-table-column property="price" label="付费金额" width="120" />
            <el-table-column property="number" label="订单数量" width="120" />
            <el-table-column property="add_time" label="付费时间" width="120" />
            <el-table-column prop="status" label="账号禁用" width="120">
            <template #default="scope">
                <el-switch v-model="scope.row.status" @click="statuschange(scope.row.id)" /></template>
            </el-table-column>
            <el-table-column  label="操作" width="120">
            <template #default="scope">
                <el-button type="primary" @click="handleEdit(scope.row)" size="small">编辑</el-button>
                <el-button type="success" @click="handleDelete(scope.row.id)" size="small">删除</el-button></template>
            </el-table-column>
        </el-table>  
        <div>
            <el-pagination
                v-model:current-page="query.page"
                v-model:page-size="query.size"
                :page-sizes="[1, 2, 3, 4]"
                size="small"               
                background
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
        </div>
        <el-button type="primary" @click="handleDeleteAll">批量删除</el-button>
        <el-button type="primary" @click="exportdata">批量导出</el-button>
        <el-dialog v-model="dialogFormVisible" title="修改信息" width="500">
           <p>昵称：<el-input v-model="editForm.name" style="width:240px" placeholder="昵称"/></p>
           <p>手机号：<el-input v-model="editForm.phone" style="width:240px" placeholder="手机号"/></p>
            <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleEditSubmit">
                保存
        </el-button></div></template></el-dialog>

    </el-card>
  
</template>


<style scoped>

.el-pagination {
    margin-top: 20px;
    text-align: right;
}

</style>
