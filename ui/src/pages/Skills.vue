<template>
  <div class="skills">
    <el-card class="skills-card">
      <template #header>
        <div class="card-header">
          <span>{{ $t('skills') }}</span>
          <el-button type="primary" @click="handleCreateSkill">
            <el-icon><i-ep-plus /></el-icon>
            {{ $t('createSkill') }}
          </el-button>
        </div>
      </template>
      <div class="skills-content">
        <!-- 技能列表 -->
        <el-table :data="skills" style="width: 100%">
          <el-table-column prop="name" label="{{ $t('skillName') }}" width="200" />
          <el-table-column prop="category" label="{{ $t('skillCategory') }}" width="150" />
          <el-table-column prop="status" label="{{ $t('skillStatus') }}" width="120">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="rating" label="{{ $t('skillRating') }}" width="100">
            <template #default="scope">
              <el-rate v-model="scope.row.rating" disabled />
            </template>
          </el-table-column>
          <el-table-column label="{{ $t('actions') }}" width="200">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEditSkill(scope.row)">
                <el-icon><i-ep-edit /></el-icon>
                {{ $t('editSkill') }}
              </el-button>
              <el-button type="danger" size="small" @click="handleDeleteSkill(scope.row)">
                <el-icon><i-ep-delete /></el-icon>
                {{ $t('deleteSkill') }}
              </el-button>
              <el-button type="success" size="small" @click="handleVerifySkill(scope.row)" v-if="scope.row.status !== 'Verified'">
                <el-icon><i-ep-check /></el-icon>
                {{ $t('verifySkill') }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 创建/编辑技能对话框 -->
        <el-dialog
          :title="dialogTitle"
          v-model="dialogVisible"
          width="600px"
        >
          <el-form :model="skillForm" label-width="100px">
            <el-form-item label="{{ $t('skillName') }}">
              <el-input v-model="skillForm.name" />
            </el-form-item>
            <el-form-item label="{{ $t('skillCategory') }}">
              <el-select v-model="skillForm.category">
                <el-option label="通用任务" value="general_task" />
                <el-option label="研究" value="research" />
                <el-option label="写作" value="writing" />
                <el-option label="分析" value="analysis" />
                <el-option label="规划" value="planning" />
              </el-select>
            </el-form-item>
            <el-form-item label="{{ $t('skillDescription') }}">
              <el-input type="textarea" v-model="skillForm.description" :rows="3" />
            </el-form-item>
            <el-form-item label="{{ $t('executionSteps') }}">
              <el-input type="textarea" v-model="skillForm.steps" :rows="4" />
            </el-form-item>
            <el-form-item label="{{ $t('successCriteria') }}">
              <el-input type="textarea" v-model="skillForm.criteria" :rows="3" />
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="dialogVisible = false">{{ $t('cancel') }}</el-button>
              <el-button type="primary" @click="handleSaveSkill">{{ $t('saveChanges') }}</el-button>
            </span>
          </template>
        </el-dialog>

        <!-- 删除确认对话框 -->
        <el-dialog
          title="{{ $t('confirm') }}"
          v-model="deleteDialogVisible"
          width="400px"
        >
          <p>{{ $t('deleteConfirmation') }}</p>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="deleteDialogVisible = false">{{ $t('cancel') }}</el-button>
              <el-button type="danger" @click="handleConfirmDelete">{{ $t('confirm') }}</el-button>
            </span>
          </template>
        </el-dialog>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// 技能列表数据
const skills = ref([
  { id: 1, name: '市场调研', category: 'research', status: 'Verified', rating: 4.5 },
  { id: 2, name: '文章写作', category: 'writing', status: 'Verified', rating: 4.0 },
  { id: 3, name: '数据分析', category: 'analysis', status: 'Verified', rating: 4.2 },
  { id: 4, name: '项目规划', category: 'planning', status: 'Pending Review', rating: 3.8 },
  { id: 5, name: '客户服务', category: 'general_task', status: 'Beta (Pending Verification)', rating: 3.5 }
])

// 对话框状态
const dialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const dialogTitle = ref('')

// 当前操作的技能
const currentSkill = ref(null)

// 技能表单
const skillForm = reactive({
  name: '',
  category: 'general_task',
  description: '',
  steps: '',
  criteria: ''
})

// 获取状态类型
const getStatusType = (status) => {
  if (status === 'Verified') return 'success'
  if (status === 'Pending Review') return 'warning'
  if (status === 'Rejected') return 'danger'
  return 'info'
}

// 处理创建技能
const handleCreateSkill = () => {
  dialogTitle.value = $t('createSkill')
  currentSkill.value = null
  // 重置表单
  Object.assign(skillForm, {
    name: '',
    category: 'general_task',
    description: '',
    steps: '',
    criteria: ''
  })
  dialogVisible.value = true
}

// 处理编辑技能
const handleEditSkill = (skill) => {
  dialogTitle.value = $t('editSkill')
  currentSkill.value = skill
  // 填充表单
  Object.assign(skillForm, {
    name: skill.name,
    category: skill.category,
    description: skill.description || '',
    steps: skill.steps || '',
    criteria: skill.criteria || ''
  })
  dialogVisible.value = true
}

// 处理保存技能
const handleSaveSkill = () => {
  if (currentSkill.value) {
    // 更新技能
    Object.assign(currentSkill.value, {
      name: skillForm.name,
      category: skillForm.category,
      description: skillForm.description,
      steps: skillForm.steps,
      criteria: skillForm.criteria
    })
    // 显示成功消息
    ElMessage.success($t('skillUpdated'))
  } else {
    // 创建新技能
    const newSkill = {
      id: skills.value.length + 1,
      name: skillForm.name,
      category: skillForm.category,
      status: 'Beta (Pending Verification)',
      rating: 0,
      description: skillForm.description,
      steps: skillForm.steps,
      criteria: skillForm.criteria
    }
    skills.value.push(newSkill)
    // 显示成功消息
    ElMessage.success($t('skillCreated'))
  }
  dialogVisible.value = false
}

// 处理删除技能
const handleDeleteSkill = (skill) => {
  currentSkill.value = skill
  deleteDialogVisible.value = true
}

// 处理确认删除
const handleConfirmDelete = () => {
  if (currentSkill.value) {
    const index = skills.value.findIndex(s => s.id === currentSkill.value.id)
    if (index !== -1) {
      skills.value.splice(index, 1)
      // 显示成功消息
      ElMessage.success($t('skillDeleted'))
    }
  }
  deleteDialogVisible.value = false
}

// 处理验证技能
const handleVerifySkill = (skill) => {
  skill.status = 'Verified'
  // 显示成功消息
  ElMessage.success($t('skillVerified'))
}
</script>

<style scoped>
.skills {
  width: 100%;
}

.skills-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>