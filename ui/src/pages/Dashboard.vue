<template>
  <div class="dashboard">
    <el-card class="dashboard-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('welcome') }}</span>
        </div>
      </template>
      <div class="dashboard-content">
        <!-- 系统状态卡片 -->
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="status-card healthy">
              <div class="status-item">
                <div class="status-icon">
                  <el-icon><i-ep-check /></el-icon>
                </div>
                <div class="status-info">
                  <div class="status-title">{{ $t('systemHealth') }}</div>
                  <div class="status-value">{{ $t('healthy') }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="status-card">
              <div class="status-item">
                <div class="status-icon">
                  <el-icon><i-ep-microchip /></el-icon>
                </div>
                <div class="status-info">
                  <div class="status-title">{{ $t('cpuUsage') }}</div>
                  <div class="status-value">15%</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="status-card">
              <div class="status-item">
                <div class="status-icon">
                  <el-icon><i-ep-save /></el-icon>
                </div>
                <div class="status-info">
                  <div class="status-title">{{ $t('memoryUsage') }}</div>
                  <div class="status-value">45%</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="status-card">
              <div class="status-item">
                <div class="status-icon">
                  <el-icon><i-ep-data-analysis /></el-icon>
                </div>
                <div class="status-info">
                  <div class="status-title">{{ $t('skillCount') }}</div>
                  <div class="status-value">24</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 图表区域 -->
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span>{{ $t('systemStatus') }}</span>
                </div>
              </template>
              <div class="chart-container">
                <div ref="cpuChart" class="chart"></div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span>{{ $t('skillCount') }}</span>
                </div>
              </template>
              <div class="chart-container">
                <div ref="skillChart" class="chart"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 最近活动 -->
        <el-card class="activity-card" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>{{ $t('recentActivities') }}</span>
            </div>
          </template>
          <el-table :data="activities" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180">
              <template #default="scope">
                {{ formatTime(scope.row.time) }}
              </template>
            </el-table-column>
            <el-table-column prop="activity" label="活动" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'success' ? 'success' : 'warning'">
                  {{ scope.row.status === 'success' ? '成功' : '处理中' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

// 图表实例
const cpuChart = ref(null)
const skillChart = ref(null)
let cpuChartInstance = null
let skillChartInstance = null

// 最近活动数据
const activities = ref([
  { time: new Date(), activity: '技能 "市场调研" 被创建', status: 'success' },
  { time: new Date(Date.now() - 3600000), activity: '系统启动', status: 'success' },
  { time: new Date(Date.now() - 7200000), activity: '技能 "数据分析" 被验证', status: 'success' },
  { time: new Date(Date.now() - 10800000), activity: '用户登录', status: 'success' },
  { time: new Date(Date.now() - 14400000), activity: '技能 "项目规划" 被更新', status: 'success' }
])

// 格式化时间
const formatTime = (date) => {
  return new Date(date).toLocaleString()
}

// 初始化图表
const initCharts = () => {
  // CPU 使用率图表
  cpuChartInstance = echarts.init(cpuChart.value)
  cpuChartInstance.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00']
    },
    yAxis: {
      type: 'value',
      max: 100
    },
    series: [{
      data: [12, 19, 15, 25, 18, 15],
      type: 'line',
      smooth: true,
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [{
            offset: 0, color: 'rgba(24, 144, 255, 0.5)'
          }, {
            offset: 1, color: 'rgba(24, 144, 255, 0.1)'
          }]
        }
      }
    }]
  })

  // 技能数量图表
  skillChartInstance = echarts.init(skillChart.value)
  skillChartInstance.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [{
      name: '技能类别',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 8, name: '通用任务' },
        { value: 6, name: '研究' },
        { value: 4, name: '写作' },
        { value: 3, name: '分析' },
        { value: 3, name: '规划' }
      ]
    }]
  })
}

// 响应式调整
const handleResize = () => {
  cpuChartInstance?.resize()
  skillChartInstance?.resize()
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  cpuChartInstance?.dispose()
  skillChartInstance?.dispose()
})
</script>

<style scoped>
.dashboard {
  width: 100%;
}

.dashboard-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-card {
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
}

.status-card.healthy {
  border-left: 4px solid #67c23a;
}

.status-item {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.status-icon {
  font-size: 32px;
  margin-right: 20px;
  color: #1890ff;
}

.status-info {
  flex: 1;
}

.status-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.status-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.chart-card {
  height: 300px;
}

.chart-container {
  height: 240px;
}

.chart {
  width: 100%;
  height: 100%;
}

.activity-card {
  margin-top: 20px;
}
</style>