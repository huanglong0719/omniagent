<template>
  <div class="settings">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('settings') }}</span>
        </div>
      </template>
      <div class="settings-content">
        <el-tabs v-model="activeTab">
          <!-- 基本设置 -->
          <el-tab-pane label="{{ $t('general') }}" name="general">
            <el-form :model="settingsForm" label-width="150px">
              <el-form-item label="{{ $t('language') }}">
                <el-select v-model="settingsForm.language">
                  <el-option label="中文" value="zh-CN" />
                  <el-option label="English" value="en-US" />
                </el-select>
              </el-form-item>
              <el-form-item label="{{ $t('theme') }}">
                <el-select v-model="settingsForm.theme">
                  <el-option label="{{ $t('lightMode') }}" value="light" />
                  <el-option label="{{ $t('darkMode') }}" value="dark" />
                </el-select>
              </el-form-item>
            </el-form>
          </el-tab-pane>

          <!-- API 设置 -->
          <el-tab-pane label="API" name="api">
            <el-form :model="apiForm" label-width="150px">
              <el-form-item label="{{ $t('apiEndpoint') }}">
                <el-input v-model="apiForm.endpoint" />
              </el-form-item>
              <el-form-item label="API Key">
                <el-input v-model="apiForm.key" type="password" />
              </el-form-item>
              <el-form-item label="代理设置">
                <el-input v-model="apiForm.proxy" />
              </el-form-item>
            </el-form>
          </el-tab-pane>

          <!-- 向量数据库设置 -->
          <el-tab-pane label="{{ $t('vectorDatabase') }}" name="vector">
            <el-form :model="vectorForm" label-width="150px">
              <el-form-item label="数据库类型">
                <el-select v-model="vectorForm.type">
                  <el-option label="Qdrant" value="qdrant" />
                  <el-option label="本地索引" value="local" />
                </el-select>
              </el-form-item>
              <el-form-item label="Qdrant URL">
                <el-input v-model="vectorForm.url" />
              </el-form-item>
              <el-form-item label="集合名称">
                <el-input v-model="vectorForm.collection" />
              </el-form-item>
            </el-form>
          </el-tab-pane>

          <!-- 监控设置 -->
          <el-tab-pane label="{{ $t('monitoringSettings') }}" name="monitoring">
            <el-form :model="monitoringForm" label-width="150px">
              <el-form-item label="Prometheus URL">
                <el-input v-model="monitoringForm.prometheusUrl" />
              </el-form-item>
              <el-form-item label="Grafana URL">
                <el-input v-model="monitoringForm.grafanaUrl" />
              </el-form-item>
              <el-form-item label="监控频率">
                <el-input v-model="monitoringForm.frequency" type="number" />
                <span style="margin-left: 10px;">秒</span>
              </el-form-item>
            </el-form>
          </el-tab-pane>

          <!-- 通知设置 -->
          <el-tab-pane label="{{ $t('notificationSettings') }}" name="notification">
            <el-form :model="notificationForm" label-width="150px">
              <el-form-item label="邮件通知">
                <el-switch v-model="notificationForm.email" />
              </el-form-item>
              <el-form-item label="邮件地址" v-if="notificationForm.email">
                <el-input v-model="notificationForm.emailAddress" />
              </el-form-item>
              <el-form-item label="短信通知">
                <el-switch v-model="notificationForm.sms" />
              </el-form-item>
              <el-form-item label="手机号码" v-if="notificationForm.sms">
                <el-input v-model="notificationForm.phone" />
              </el-form-item>
              <el-form-item label="告警级别">
                <el-select v-model="notificationForm.level">
                  <el-option label="全部" value="all" />
                  <el-option label="警告及以上" value="warning" />
                  <el-option label="严重" value="critical" />
                </el-select>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>

        <!-- 保存按钮 -->
        <div class="save-button-container">
          <el-button type="primary" @click="handleSaveSettings">
            {{ $t('saveSettings') }}
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// 当前激活的标签
const activeTab = ref('general')

// 基本设置
const settingsForm = reactive({
  language: 'zh-CN',
  theme: 'light'
})

// API 设置
const apiForm = reactive({
  endpoint: 'http://localhost:8000',
  key: '',
  proxy: 'http://localhost:10808'
})

// 向量数据库设置
const vectorForm = reactive({
  type: 'qdrant',
  url: 'http://localhost:6333',
  collection: 'omniagent_messages'
})

// 监控设置
const monitoringForm = reactive({
  prometheusUrl: 'http://localhost:9090',
  grafanaUrl: 'http://localhost:3000',
  frequency: 15
})

// 通知设置
const notificationForm = reactive({
  email: false,
  emailAddress: '',
  sms: false,
  phone: '',
  level: 'warning'
})

// 处理保存设置
const handleSaveSettings = () => {
  // 保存设置的逻辑
  console.log('保存设置:', {
    settingsForm,
    apiForm,
    vectorForm,
    monitoringForm,
    notificationForm
  })
  // 显示成功消息
  ElMessage.success($t('settingsSaved'))
}
</script>

<style scoped>
.settings {
  width: 100%;
}

.settings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.save-button-container {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end;
}
</style>