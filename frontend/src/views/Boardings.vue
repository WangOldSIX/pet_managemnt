<template>
  <div class="boardings">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>寄养管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增寄养
          </el-button>
        </div>
      </template>
      
      <div class="search-form">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="寄养中" value="boarding" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table :data="tableData" v-loading="loading" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="pet_name" label="宠物名称" width="120" />
        <el-table-column prop="owner_name" label="主人" width="100" />
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="end_date" label="结束日期" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_price" label="总金额" width="120">
          <template #default="{ row }">
            ¥{{ row.total_price }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看</el-button>
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])

const searchForm = reactive({
  status: ''
})

const getStatusType = (status) => {
  const map = {
    boarding: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return map[status] || 'info'
}

const getStatusLabel = (status) => {
  const map = {
    boarding: '寄养中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

const fetchData = async () => {
  loading.value = true
  try {
    // Mock data
    await new Promise(resolve => setTimeout(resolve, 500))
    
    tableData.value = [
      {
        id: 1,
        pet_name: '旺财',
        owner_name: '张三',
        start_date: '2024-01-01',
        end_date: '2024-01-10',
        status: 'completed',
        total_price: 1800
      },
      {
        id: 2,
        pet_name: '小白',
        owner_name: '李四',
        start_date: '2024-01-15',
        end_date: '2024-01-25',
        status: 'boarding',
        total_price: 2000
      }
    ]
  } catch (error) {
    console.error('Failed to fetch boardings:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  fetchData()
}

const handleReset = () => {
  searchForm.status = ''
  fetchData()
}

const handleAdd = () => {
  ElMessage.info('新增寄养功能待实现')
}

const handleView = (row) => {
  ElMessage.info('查看寄养详情功能待实现')
}

const handleEdit = (row) => {
  ElMessage.info('编辑寄养功能待实现')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.boardings {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}
</style>
