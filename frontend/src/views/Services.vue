<template>
  <div class="services">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>服务管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增服务
          </el-button>
        </div>
      </template>
      
      <el-table :data="tableData" v-loading="loading" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="服务名称" width="150" />
        <el-table-column prop="description" label="服务描述" />
        <el-table-column prop="price" label="价格" width="100">
          <template #default="{ row }">
            ¥{{ row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="时长(分钟)" width="120" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])

const fetchData = async () => {
  loading.value = true
  try {
    // Mock data
    await new Promise(resolve => setTimeout(resolve, 500))
    
    tableData.value = [
      { id: 1, name: '洗澡', description: '宠物洗澡服务', price: 50, duration: 30, is_active: true },
      { id: 2, name: '美容', description: '宠物美容服务', price: 150, duration: 60, is_active: true },
      { id: 3, name: '寄养', description: '宠物寄养服务', price: 200, duration: 1440, is_active: true }
    ]
  } catch (error) {
    console.error('Failed to fetch services:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  ElMessage.info('新增服务功能待实现')
}

const handleEdit = (row) => {
  ElMessage.info('编辑服务功能待实现')
}

const handleDelete = (row) => {
  ElMessage.info('删除服务功能待实现')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.services {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
