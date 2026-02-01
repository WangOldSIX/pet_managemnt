<template>
  <div class="health-records">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>健康记录</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增记录
          </el-button>
        </div>
      </template>
      
      <div class="search-form">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="宠物名称">
            <el-input v-model="searchForm.pet_name" placeholder="请输入宠物名称" clearable />
          </el-form-item>
          <el-form-item label="记录类型">
            <el-select v-model="searchForm.record_type" placeholder="请选择类型" clearable>
              <el-option label="疫苗" value="vaccination" />
              <el-option label="体检" value="checkup" />
              <el-option label="治疗" value="treatment" />
              <el-option label="其他" value="other" />
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
        <el-table-column prop="record_type" label="记录类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getRecordTypeColor(row.record_type)">
              {{ getRecordTypeLabel(row.record_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="record_date" label="记录日期" width="120" />
        <el-table-column prop="doctor" label="医生" width="100" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
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
  pet_name: '',
  record_type: ''
})

const getRecordTypeLabel = (type) => {
  const map = {
    vaccination: '疫苗',
    checkup: '体检',
    treatment: '治疗',
    other: '其他'
  }
  return map[type] || type
}

const getRecordTypeColor = (type) => {
  const map = {
    vaccination: 'success',
    checkup: 'primary',
    treatment: 'warning',
    other: 'info'
  }
  return map[type] || 'info'
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
        record_type: 'vaccination',
        description: '狂犬疫苗接种',
        record_date: '2024-01-01',
        doctor: '王医生'
      },
      {
        id: 2,
        pet_name: '小白',
        record_type: 'checkup',
        description: '年度体检',
        record_date: '2024-01-15',
        doctor: '李医生'
      }
    ]
  } catch (error) {
    console.error('Failed to fetch health records:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  fetchData()
}

const handleReset = () => {
  Object.assign(searchForm, { pet_name: '', record_type: '' })
  fetchData()
}

const handleAdd = () => {
  ElMessage.info('新增记录功能待实现')
}

const handleView = (row) => {
  ElMessage.info('查看记录详情功能待实现')
}

const handleDelete = (row) => {
  ElMessage.info('删除记录功能待实现')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.health-records {
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
