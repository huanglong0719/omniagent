<template>
  <div class="monitoring">
    <el-card class="monitoring-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('monitoring') }}</span>
        </div>
      </template>
      <div class="monitoring-content">
        <!-- 系统健康状态 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="health-card healthy">
              <div class="health-item">
                <div class="health-icon">
                  <el-icon><i-ep-check /></el-icon>
                </div>
                <div class="health-info">
                  <div class="health-title">{{ $t('systemHealth') }}</div>
                  <div class="health-value">{{ $t('healthy') }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="health-card">
              <div class="health-item">
                <div class="health-icon">
                  <el-icon><i-ep-microchip /></el-icon>
                </div>
                <div class="health-info">
                  <div class="health-title">{{ $t('cpuUsage') }}</div>
                  <div class="health-value">15%</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="health-card">
              <div class="health-item">
                <div class="health-icon">
                  <el-icon><i-ep-save /></el-icon>
                </div>
                <div class="health-info">
                  <div class="health-title">{{ $t('memoryUsage') }}</div>
                  <div class="health-value">45%</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 监控图表 -->
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span>请求处理时间</span>
                </div>
              </template>
              <div class="chart-container">
                <div ref="responseTimeChart" class="chart"></div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span>请求计数</span>
                </div>
              </template>
              <div class="chart-container">
                <div ref="requestCountChart" class="chart"></div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 技能使用统计 -->
        <el-card class="skill-usage-card" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>技能使用统计</span>
            </div>
          </template>
          <div class="chart-container">
            <div ref="skillUsageChart" class="chart"></div>
          </div>
        </el-card>

        <!-- 系统日志 -->
        <el-card class="logs-card" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>系统日志</span>
            </div>
          </template>
          <el-table :data="logs" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180">
              <template #default="scope">
                {{ formatTime(scope.row.time) }}
              </template>
            </el-table-column>
            <el-table-column prop="level" label="级别" width="100">
              <template #default="scope">
                <el-tag :type="getLevelType(scope.row.level)">
                  {{ scope.row.level }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="message" label="消息" />
          </el-table>
          <div class="pagination-container">
            <el-pagination
              layout="prev, pager, next"
              :total="100"
              :page-size="10"
              :current-page="1"
            />
          </div>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

// 图表实例
const responseTimeChart = ref(null)
const requestCountChart = ref(null)
const skillUsageChart = ref(null)
let responseTimeChartInstance = null
let requestCountChartInstance = null
let skillUsageChartInstance = null

// 系统日志数据
const logs = ref([
  { time: new Date(), level: 'INFO', message: '系统启动成功' },
  { time: new Date(Date.now() - 3600000), level: 'INFO', message: '技能 "市场调研" 被创建' },
  { time: new Date(Date.now() - 7200000), level: 'INFO', message: '技能 "数据分析" 被验证' },
  { time: new Date(Date.now() - 10800000), level: 'WARN', message: '内存使用接近阈值' },
  { time: new Date(Date.now() - 14400000), level: 'INFO', message: '用户登录成功' }
])

// 格式化时间
const formatTime = (date) => {
  return new Date(date).toLocaleString()
}

// 获取日志级别类型
const getLevelType = (level) => {
  if (level === 'INFO') return 'info'
  if (level === 'WARN') return 'warning'
  if (level === 'ERROR') return 'danger'
  return 'info'
}

// 初始化图表
const initCharts = () => {
  // 请求处理时间图表
  responseTimeChartInstance = echarts.init(responseTimeChart.value)
  responseTimeChartInstance.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00']
    },
    yAxis: {
      type: 'value',
      name: '毫秒'
    },
    series: [{
      data: [120, 190, 150, 250, 180, 150],
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

  // 请求计数图表
  requestCountChartInstance = echarts.init(requestCountChart.value)
  requestCountChartInstance.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00']
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: [120, 200, 150, 250, 220, 180],
      type: 'bar',
      itemStyle: {
        color: '#1890ff'
      }
    }]
  })

  // 技能使用统计图表
  skillUsageChartInstance = echarts.init(skillUsageChart.value)
  skillUsageChartInstance.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: ['市场调研', '文章写作', '数据分析', '项目规划', '客户服务']
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: [120, 90, 80, 60, 40],
      type: 'bar',
      itemStyle: {
        color: function(params) {
          const colors = ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1']
          return colors[params.dataIndex]
        }
      }
    }]
  })
}

// 响应式调整
const handleResize = () => {
  responseTimeChartInstance?.resize()
  requestCountChartInstance?.resize()
  skillUsageChartInstance?.resize()
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  responseTimeChartInstance?.dispose()
  requestCountChartInstance?.dispose()
  skillUsageChartInstance?.dispose()
})
</script>

<style scoped>
.monitoring {
  width: 100%;
}

.monitoring-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.health-card {
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
}

.health-card.healthy {
  border-left: 4px solid #67c23a;
}

.health-item {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.health-icon {
  font-size: 32px;
  margin-right: 20px;
  color: #1890ff;
}

.health-info {
  flex: 1;
}

.health-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.health-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.chart-card {
  height: 300px;
}

.skill-usage-card {
  height: 300px;
}

.chart-container {
  height: 240px;
}

.chart {
  width: 100%;
  height: 100%;
}

.logs-card {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>