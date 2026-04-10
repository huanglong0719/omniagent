<template>
  <div class="app-container">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <h2>OmniAgent</h2>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          router
        >
          <el-menu-item index="/dashboard">
            <el-icon><i-ep-home /></el-icon>
            <span>{{ $t('dashboard') }}</span>
          </el-menu-item>
          <el-menu-item index="/skills">
            <el-icon><i-ep-tools /></el-icon>
            <span>{{ $t('skills') }}</span>
          </el-menu-item>
          <el-menu-item index="/settings">
            <el-icon><i-ep-setting /></el-icon>
            <span>{{ $t('settings') }}</span>
          </el-menu-item>
          <el-menu-item index="/monitoring">
            <el-icon><i-ep-data-analysis /></el-icon>
            <span>{{ $t('monitoring') }}</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-container class="main-container">
        <!-- 顶部导航栏 -->
        <el-header class="header">
          <div class="header-left">
            <el-button
              type="text"
              class="menu-toggle"
              @click="toggleSidebar"
            >
              <el-icon><i-ep-menu /></el-icon>
            </el-button>
          </div>
          <div class="header-right">
            <el-dropdown>
              <span class="user-info">
                <el-avatar :size="32" :src="userAvatar" />
                <span class="user-name">{{ $t('user') }}</span>
                <el-icon class="el-icon--right"><i-ep-arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>{{ $t('profile') }}</el-dropdown-item>
                  <el-dropdown-item>{{ $t('logout') }}</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <el-dropdown>
              <el-button type="text" class="language-toggle">
                <el-icon><i-ep-translation /></el-icon>
                <span>{{ currentLanguage }}</span>
                <el-icon class="el-icon--right"><i-ep-arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="changeLanguage('zh-CN')">中文</el-dropdown-item>
                  <el-dropdown-item @click="changeLanguage('en-US')">English</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>

        <!-- 内容区域 -->
        <el-main class="content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { locale, t } = useI18n()

// 侧边栏状态
const sidebarCollapsed = ref(false)

// 当前激活的菜单
const activeMenu = computed(() => {
  return router.currentRoute.value.path
})

// 切换侧边栏
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

// 用户信息
const userAvatar = ref('https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50')

// 当前语言
const currentLanguage = computed(() => {
  return locale.value === 'zh-CN' ? '中文' : 'English'
})

// 切换语言
const changeLanguage = (lang) => {
  locale.value = lang
}
</script>

<style scoped>
.app-container {
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  background-color: #001529;
  color: #fff;
  transition: all 0.3s;
}

.logo {
  text-align: center;
  padding: 20px 0;
  border-bottom: 1px solid #002140;
}

.logo h2 {
  color: #fff;
  margin: 0;
  font-size: 18px;
}

.sidebar-menu {
  margin-top: 20px;
}

.sidebar-menu .el-menu-item {
  color: #fff;
}

.sidebar-menu .el-menu-item.is-active {
  background-color: #1890ff;
}

.main-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #fff;
  border-bottom: 1px solid #e8e8e8;
  height: 64px;
}

.menu-toggle {
  margin-right: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.user-name {
  margin-left: 10px;
  margin-right: 5px;
}

.language-toggle {
  margin-left: 20px;
}

.content {
  flex: 1;
  overflow: auto;
  padding: 20px;
  background-color: #f0f2f5;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>