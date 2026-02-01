<template>
  <div class="users">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增用户
          </el-button>
        </div>
      </template>
      
      <div class="search-form">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="用户名">
            <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="searchForm.role" placeholder="请选择角色" clearable>
              <el-option label="管理员" value="admin" />
              <el-option label="员工" value="staff" />
              <el-option label="宠物主" value="owner" />
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
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="real_name" label="姓名" width="120" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)">
              {{ getRoleLabel(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserList } from '@/api/users'

const loading = ref(false)
const tableData = ref([])

const searchForm = reactive({
  username: '',
  role: ''
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const getRoleType = (role) => {
  const map = {
    admin: 'danger',
    staff: 'warning',
    owner: 'success'
  }
  return map[role] || 'info'
}

const getRoleLabel = (role) => {
  const map = {
    admin: '管理员',
    staff: '员工',
    owner: '宠物主'
  }
  return map[role] || role
}

const fetchData = async () => {
  loading.value = true
  try {
    // Mock data for now
    await new Promise(resolve => setTimeout(resolve, 500))
    
    tableData.value = [
      {
        id: 1,
        username: 'admin',
        real_name: '管理员',
        email: 'admin@example.com',
        phone: '13800138000',
        role: 'admin',
        is_active: true,
        created_at: '2024-01-01 10:00:00'
      },
      {
        id: 2,
        username: 'staff1',
        real_name: '张三',
        email: 'staff1@example.com',
        phone: '13800138001',
        role: 'staff',
        is_active: true,
        created_at: '2024-01-02 10:00:00'
      },
      {
        id: 3,
        username: 'owner1',
        real_name: '李四',
        email: 'owner1@example.com',
        phone: '13800138002',
        role: 'owner',
        is_active: true,
        created_at: '2024-01-03 10:00:00'
      }
    ]
    pagination.total = 3
  } catch (error) {
    console.error('Failed to fetch users:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const handleReset = () => {
  Object.assign(searchForm, {
    username: '',
    role: ''
  })
  handleSearch()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchData()
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchData()
}

const handleAdd = () => {
  ElMessage.info('新增用户功能待实现')
}

const handleEdit = (row) => {
  ElMessage.info('编辑用户功能待实现')
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
    fetchData()
  }).catch(() => {})
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.users {
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
