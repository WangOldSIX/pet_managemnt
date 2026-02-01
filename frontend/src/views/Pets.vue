<template>
  <div class="pets">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>宠物管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增宠物
          </el-button>
        </div>
      </template>
      
      <!-- Search -->
      <div class="search-form">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="宠物名称">
            <el-input v-model="searchForm.name" placeholder="请输入宠物名称" clearable />
          </el-form-item>
          <el-form-item label="物种">
            <el-select v-model="searchForm.species" placeholder="请选择物种" clearable>
              <el-option label="狗" value="狗" />
              <el-option label="猫" value="猫" />
              <el-option label="鸟" value="鸟" />
              <el-option label="兔子" value="兔子" />
            </el-select>
          </el-form-item>
          <el-form-item label="性别">
            <el-select v-model="searchForm.gender" placeholder="请选择性别" clearable>
              <el-option label="公" value="公" />
              <el-option label="母" value="母" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- Table -->
      <el-table :data="tableData" v-loading="loading" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="宠物名称" width="120" />
        <el-table-column prop="species" label="物种" width="100" />
        <el-table-column prop="breed" label="品种" width="120" />
        <el-table-column prop="gender" label="性别" width="80" />
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="weight" label="体重" width="80" />
        <el-table-column prop="owner_name" label="主人" width="100" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看</el-button>
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- Pagination -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
    
    <!-- Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="宠物名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入宠物名称" />
        </el-form-item>
        <el-form-item label="物种" prop="species">
          <el-select v-model="formData.species" placeholder="请选择物种">
            <el-option label="狗" value="狗" />
            <el-option label="猫" value="猫" />
            <el-option label="鸟" value="鸟" />
            <el-option label="兔子" value="兔子" />
          </el-select>
        </el-form-item>
        <el-form-item label="品种" prop="breed">
          <el-input v-model="formData.breed" placeholder="请输入品种" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="formData.gender">
            <el-radio value="公">公</el-radio>
            <el-radio value="母">母</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="formData.age" :min="0" :max="30" />
        </el-form-item>
        <el-form-item label="体重" prop="weight">
          <el-input-number v-model="formData.weight" :min="0" :max="100" :precision="2" />
        </el-form-item>
        <el-form-item label="主人" prop="owner_id">
          <el-select v-model="formData.owner_id" placeholder="请选择主人" filterable>
            <el-option
              v-for="user in users"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="formData.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getPetList, createPet, updatePet, deletePet } from '@/api/pets'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增宠物')
const isEdit = ref(false)
const currentId = ref(null)

const formRef = ref(null)

const searchForm = reactive({
  name: '',
  species: '',
  gender: ''
})

const formData = reactive({
  name: '',
  species: '',
  breed: '',
  gender: '公',
  age: 1,
  weight: 5.0,
  owner_id: null,
  phone: '',
  notes: ''
})

const formRules = {
  name: [{ required: true, message: '请输入宠物名称', trigger: 'blur' }],
  species: [{ required: true, message: '请选择物种', trigger: 'change' }],
  breed: [{ required: true, message: '请输入品种', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  weight: [{ required: true, message: '请输入体重', trigger: 'blur' }],
  owner_id: [{ required: true, message: '请选择主人', trigger: 'change' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
}

const tableData = ref([])
const users = ref([])

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getPetList({
      ...searchForm,
      page: pagination.page,
      size: pagination.size
    })
    
    if (res.data) {
      tableData.value = res.data.items || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('Failed to fetch pets:', error)
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
    name: '',
    species: '',
    gender: ''
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
  dialogTitle.value = '新增宠物'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

const handleView = (row) => {
  // TODO: Show pet detail
  ElMessage.info('查看宠物详情功能待实现')
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑宠物'
  isEdit.value = true
  currentId.value = row.id
  
  Object.assign(formData, {
    name: row.name,
    species: row.species,
    breed: row.breed,
    gender: row.gender,
    age: row.age,
    weight: row.weight,
    owner_id: row.owner_id,
    phone: row.phone,
    notes: row.notes || ''
  })
  
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该宠物吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deletePet(row.id)
      ElMessage.success('删除成功')
      fetchData()
    } catch (error) {
      console.error('Failed to delete pet:', error)
    }
  }).catch(() => {
    // User cancelled
  })
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (!valid) return
    
    submitLoading.value = true
    
    if (isEdit.value) {
      await updatePet(currentId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await createPet(formData)
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error('Failed to submit:', error)
  } finally {
    submitLoading.value = false
  }
}

const handleDialogClose = () => {
  resetForm()
}

const resetForm = () => {
  Object.assign(formData, {
    name: '',
    species: '',
    breed: '',
    gender: '公',
    age: 1,
    weight: 5.0,
    owner_id: null,
    phone: '',
    notes: ''
  })
  
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

onMounted(() => {
  // Mock users for now
  users.value = [
    { id: 1, username: '张三' },
    { id: 2, username: '李四' },
    { id: 3, username: '王五' }
  ]
  
  fetchData()
})
</script>

<style scoped>
.pets {
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
