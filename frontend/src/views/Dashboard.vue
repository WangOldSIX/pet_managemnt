<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #409eff">
              <el-icon :size="32"><Star /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pets }}</div>
              <div class="stat-label">宠物总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #67c23a">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.users }}</div>
              <div class="stat-label">用户总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #e6a23c">
              <el-icon :size="32"><ShoppingCart /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.orders }}</div>
              <div class="stat-label">订单总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #f56c6c">
              <el-icon :size="32"><Service /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.services }}</div>
              <div class="stat-label">服务总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近宠物</span>
            </div>
          </template>
          <el-table :data="recentPets" style="width: 100%">
            <el-table-column prop="name" label="宠物名称" />
            <el-table-column prop="species" label="物种" />
            <el-table-column prop="breed" label="品种" />
            <el-table-column prop="gender" label="性别" />
            <el-table-column label="操作">
              <template #default="{ row }">
                <el-button link type="primary" @click="viewPet(row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近订单</span>
            </div>
          </template>
          <el-table :data="recentOrders" style="width: 100%">
            <el-table-column prop="id" label="订单号" width="100" />
            <el-table-column prop="service_name" label="服务名称" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="total_price" label="金额">
              <template #default="{ row }">
                ¥{{ row.total_price }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const stats = ref({
  pets: 0,
  users: 0,
  orders: 0,
  services: 0
})

const recentPets = ref([])
const recentOrders = ref([])

const getStatusType = (status) => {
  const map = {
    pending: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return map[status] || 'info'
}

const viewPet = (pet) => {
  // TODO: Navigate to pet detail
  console.log('View pet:', pet)
}

onMounted(async () => {
  // TODO: Fetch dashboard data from API
  // Mock data for now
  stats.value = {
    pets: 156,
    users: 89,
    orders: 234,
    services: 15
  }
  
  recentPets.value = [
    { id: 1, name: '旺财', species: '狗', breed: '金毛', gender: '公' },
    { id: 2, name: '小白', species: '猫', breed: '英短', gender: '母' },
    { id: 3, name: '大黄', species: '狗', breed: '中华田园犬', gender: '公' }
  ]
  
  recentOrders.value = [
    { id: 'ORD001', service_name: '洗澡', status: 'completed', total_price: 50 },
    { id: 'ORD002', service_name: '寄养', status: 'pending', total_price: 200 },
    { id: 'ORD003', service_name: '美容', status: 'pending', total_price: 150 }
  ]
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-weight: bold;
}
</style>
