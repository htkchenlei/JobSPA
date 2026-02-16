<template>
  <div class="change-password">
    <h1>个人设置</h1>
    
    <div class="settings-tabs">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'password' }"
        @click="activeTab = 'password'"
      >
        修改密码
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'ai' }"
        @click="activeTab = 'ai'"
      >
        AI模型设置
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'api' }"
        @click="activeTab = 'api'"
      >
        API文档
      </button>
    </div>
    
    <!-- 修改密码表单 -->
    <div v-if="activeTab === 'password'" class="change-password-form">
      <form @submit.prevent="submitChangePassword">
        <div class="form-group">
          <label>当前密码</label>
          <input type="password" v-model="changePasswordForm.currentPassword" class="form-control" required>
        </div>
        <div class="form-group">
          <label>新密码</label>
          <input type="password" v-model="changePasswordForm.newPassword" class="form-control" required>
        </div>
        <div class="form-group">
          <label>确认新密码</label>
          <input type="password" v-model="changePasswordForm.confirmPassword" class="form-control" required>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">保存</button>
        </div>
      </form>
    </div>
    
    <!-- AI模型设置 -->
    <div v-if="activeTab === 'ai'" class="ai-settings-form">
      <div class="form-group">
        <label>选择AI模型</label>
        <div class="model-options">
          <label v-for="model in models" :key="model.value" class="model-option">
            <input type="radio" v-model="aiForm.defaultModel" :value="model.value">
            <span>{{ model.label }}</span>
          </label>
        </div>
      </div>
      
      <div class="model-apis">
        <h4>API密钥设置</h4>
        
        <div v-if="aiForm.defaultModel === 'deepseek'" class="form-group">
          <label>DeepSeek API密钥</label>
          <input type="password" v-model="aiForm.apiKeys.deepseek" class="form-control" placeholder="输入DeepSeek API密钥" required>
          <small class="form-text text-muted">从 https://www.deepseek.com/ 获取API密钥</small>
        </div>
        
        <div v-if="aiForm.defaultModel === 'qwen'" class="form-group">
          <label>Qwen API密钥</label>
          <input type="password" v-model="aiForm.apiKeys.qwen" class="form-control" placeholder="输入Qwen API密钥" required>
          <small class="form-text text-muted">从 https://dashscope.aliyun.com/ 获取API密钥</small>
        </div>
        
        <div v-if="aiForm.defaultModel === 'doubao'" class="form-group">
          <label>Doubao API密钥</label>
          <input type="password" v-model="aiForm.apiKeys.doubao" class="form-control" placeholder="输入Doubao API密钥" required>
          <small class="form-text text-muted">从 https://console.volcengine.com/ark/ 获取API密钥</small>
        </div>
      </div>
      
      <div class="form-actions">
        <button class="btn btn-primary" @click="updateAiSettings">保存设置</button>
      </div>
    </div>
    
    <!-- API文档 -->
    <div v-if="activeTab === 'api'" class="api-documentation">
      <h1>API接口文档</h1>
      
      <!-- 认证相关API -->
      <section class="api-section">
        <h2>认证相关API</h2>
        <div class="api-card">
          <h3>登录</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/auth/login</div>
            <div class="api-description">用户登录接口，返回JWT token</div>
            <div class="api-request">
              <h4>请求参数：</h4>
              <pre>{"username": "用户名", "password": "密码"}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"token": "JWT token", "user": {"id": 1, "username": "用户名", "is_admin": false}}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>验证token</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/auth/verify</div>
            <div class="api-description">验证JWT token的有效性</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"user": {"id": 1, "username": "用户名", "is_admin": false}}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>登出</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/auth/logout</div>
            <div class="api-description">用户登出接口</div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"message": "登出成功"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>修改密码</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/auth/change-password</div>
            <div class="api-description">修改用户密码</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"currentPassword": "当前密码", "newPassword": "新密码"}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"message": "密码修改成功"}</pre>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 用户相关API -->
      <section class="api-section">
        <h2>用户相关API</h2>
        <div class="api-card">
          <h3>获取用户列表</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/users/</div>
            <div class="api-description">获取所有用户列表</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>[{"id": 1, "username": "用户名"}]</pre>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 项目相关API -->
      <section class="api-section">
        <h2>项目相关API</h2>
        <div class="api-card">
          <h3>获取项目列表</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/projects/</div>
            <div class="api-description">获取所有未删除的项目列表</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>[{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 1, "stage_text": "立项中"}]</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>获取单个项目</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/projects/{id}</div>
            <div class="api-description">获取单个项目的详细信息</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 1, "stage_text": "立项中"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>创建项目</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/projects/</div>
            <div class="api-description">创建新项目</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"name": "项目名称", "client_name": "客户名称", "stage": 1}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 1, "stage_text": "立项中"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>更新项目</h3>
          <div class="api-details">
            <div class="api-method put">PUT</div>
            <div class="api-url">/api/projects/{id}</div>
            <div class="api-description">更新项目信息</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"name": "项目名称", "client_name": "客户名称", "stage": 2}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 2, "stage_text": "立项中"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>更新项目进度</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/projects/{id}/progress</div>
            <div class="api-description">更新项目进度信息</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"update_content": "进度内容", "stage": 3, "updated_by": "更新人"}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "stage": 3, "stage_text": "已立项", "message": "项目进度更新成功"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>获取项目进度历史</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/projects/{id}/progress</div>
            <div class="api-description">获取项目的进度历史记录</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>[{"id": 1, "update_content": "进度内容", "update_date": "2024-01-01", "update_time": "12:00:00", "updated_by": "更新人"}]</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>删除项目</h3>
          <div class="api-details">
            <div class="api-method delete">DELETE</div>
            <div class="api-url">/api/projects/{id}</div>
            <div class="api-description">软删除项目</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"message": "项目删除成功"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>获取项目阶段列表</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/projects/stages</div>
            <div class="api-description">获取所有项目阶段列表</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>[{"value": 1, "label": "立项中"}, {"value": 2, "label": "立项中"}]</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>搜索项目</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/projects/search</div>
            <div class="api-description">根据关键词搜索项目</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"keywords": "关键词", "start_date": "开始日期", "end_date": "结束日期"}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>[{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 1, "stage_text": "立项中"}]</pre>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 文件相关API -->
      <section class="api-section">
        <h2>文件相关API</h2>
        <div class="api-card">
          <h3>获取文件系统</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/files/</div>
            <div class="api-description">获取用户的文件系统结构</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": "root", "name": "根目录", "type": "folder", "children": [{"id": "file1.txt", "name": "file1.txt", "type": "file", "size": "1KB"}]}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>创建文件夹</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/files/folders</div>
            <div class="api-description">创建新文件夹</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"name": "文件夹名称", "parentId": "父文件夹ID"}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"message": "文件夹创建成功", "path": "文件夹路径"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>上传文件</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/files/upload</div>
            <div class="api-description">上传文件到指定文件夹</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>FormData: {"files": [文件对象], "folderId": "文件夹ID"}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"message": "文件上传成功", "files": [{"name": "文件名", "path": "文件路径"}]}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>删除文件/文件夹</h3>
          <div class="api-details">
            <div class="api-method delete">DELETE</div>
            <div class="api-url">/api/files/{path}</div>
            <div class="api-description">删除指定的文件或文件夹</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"message": "文件删除成功"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>下载文件</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/files/download/{path}</div>
            <div class="api-description">下载指定的文件</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应：</h4>
              <pre>文件内容（二进制）</pre>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 待办事项相关API -->
      <section class="api-section">
        <h2>待办事项相关API</h2>
        <div class="api-card">
          <h3>获取待办事项列表</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/todos/</div>
            <div class="api-description">获取用户的待办事项列表</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>查询参数：</h4>
              <pre>is_finished=true/false（可选）</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>[{"id": 1, "item": "待办事项内容", "is_finished": false, "create_at": "2024-01-01 12:00:00", "finish_at": null}]</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>获取单个待办事项</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/todos/{id}</div>
            <div class="api-description">获取单个待办事项的详细信息</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "item": "待办事项内容", "is_finished": false, "create_at": "2024-01-01 12:00:00", "finish_at": null}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>创建待办事项</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/todos/</div>
            <div class="api-description">创建新的待办事项</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"item": "待办事项内容"}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "item": "待办事项内容", "is_finished": false, "create_at": "2024-01-01 12:00:00"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>更新待办事项</h3>
          <div class="api-details">
            <div class="api-method put">PUT</div>
            <div class="api-url">/api/todos/{id}</div>
            <div class="api-description">更新待办事项内容</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"item": "新的待办事项内容", "is_finished": true/false}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "item": "新的待办事项内容", "is_finished": true, "create_at": "2024-01-01 12:00:00", "finish_at": "2024-01-01 13:00:00"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>标记待办事项为完成</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/todos/{id}/complete</div>
            <div class="api-description">将待办事项标记为已完成</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "is_finished": true, "finish_at": "2024-01-01 13:00:00", "message": "待办事项标记为完成"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>标记待办事项为未完成</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/todos/{id}/uncomplete</div>
            <div class="api-description">将待办事项标记为未完成</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "is_finished": false, "finish_at": null, "message": "待办事项标记为未完成"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>删除待办事项</h3>
          <div class="api-details">
            <div class="api-method delete">DELETE</div>
            <div class="api-url">/api/todos/{id}</div>
            <div class="api-description">删除待办事项</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"message": "待办事项删除成功"}</pre>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 工作日志相关API -->
      <section class="api-section">
        <h2>工作日志相关API</h2>
        <div class="api-card">
          <h3>获取所有工作日志</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/work-log/</div>
            <div class="api-description">获取所有工作日志</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>[{"id": 1, "today_activities": "活动记录", "user": 1, "work_log_by_ai": "AI生成的工作日志", "log_date": "2024-01-01", "log_time": "12:00:00", "created_by_ai": "DeepSeek"}]</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>获取用户的工作日志</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/work-log/user/{user_id}</div>
            <div class="api-description">获取指定用户的所有工作日志</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>[{"id": 1, "today_activities": "活动记录", "user": 1, "work_log_by_ai": "AI生成的工作日志", "log_date": "2024-01-01", "log_time": "12:00:00", "created_by_ai": "DeepSeek"}]</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>获取指定日期的工作日志</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/work-log/date/{log_date}</div>
            <div class="api-description">获取指定日期的工作日志</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"id": 1, "today_activities": "活动记录", "user": 1, "work_log_by_ai": "AI生成的工作日志", "log_date": "2024-01-01", "log_time": "12:00:00", "created_by_ai": "DeepSeek"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>生成今日活动记录</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/work-log/generate-activities</div>
            <div class="api-description">生成今日的活动记录</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"user_id": 1}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"activities": ["活动1", "活动2", "活动3"]}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>保存工作日志</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/work-log/save</div>
            <div class="api-description">保存工作日志</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"user_id": 1, "work_log_by_ai": "AI生成的工作日志"}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"message": "工作日志保存成功"}</pre>
            </div>
          </div>
        </div>
        
        <div class="api-card">
          <h3>获取今日活动记录</h3>
          <div class="api-details">
            <div class="api-method get">GET</div>
            <div class="api-url">/api/work-log/today-activities</div>
            <div class="api-description">获取今日的活动记录</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>["活动1", "活动2", "活动3"]</pre>
            </div>
          </div>
        </div>
      </section>
      
      <!-- AI相关API -->
      <section class="api-section">
        <h2>AI相关API</h2>
        <div class="api-card">
          <h3>生成AI内容</h3>
          <div class="api-details">
            <div class="api-method post">POST</div>
            <div class="api-url">/api/ai/generate</div>
            <div class="api-description">调用大模型生成内容</div>
            <div class="api-request">
              <h4>请求头：</h4>
              <pre>Authorization: Bearer {token}</pre>
              <h4>请求参数：</h4>
              <pre>{"model": "deepseek", "prompt": "提示词", "max_tokens": 500}</pre>
            </div>
            <div class="api-response">
              <h4>响应示例：</h4>
              <pre>{"content": "AI生成的内容"}</pre>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 当前激活的标签
const activeTab = ref('password')

// 修改密码表单
const changePasswordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 模型列表
const models = [
  { value: 'deepseek', label: 'DeepSeek' },
  { value: 'qwen', label: 'Qwen' },
  { value: 'doubao', label: 'Doubao' }
]

// AI模型设置表单
const aiForm = ref({
  defaultModel: 'deepseek',
  apiKeys: {
    deepseek: '',
    qwen: '',
    doubao: ''
  }
})

// 初始化表单数据
onMounted(() => {
  // 从localStorage获取AI设置
  const aiSettingsStr = localStorage.getItem('aiSettings')
  if (aiSettingsStr) {
    aiForm.value = { ...aiForm.value, ...JSON.parse(aiSettingsStr) }
  }
})

// 提交修改密码
const submitChangePassword = async () => {
  // 验证新密码和确认密码是否一致
  if (changePasswordForm.value.newPassword !== changePasswordForm.value.confirmPassword) {
    alert('新密码和确认密码不一致')
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/auth/change-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      body: JSON.stringify(changePasswordForm.value)
    })
    
    if (response.ok) {
      const data = await response.json()
      alert('密码修改成功')
      // 重置表单
      changePasswordForm.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
      // 可以选择跳转回仪表盘
      // router.push('/dashboard')
    } else {
      const errorData = await response.json()
      alert(`密码修改失败: ${errorData.error}`)
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    alert('修改密码失败，请稍后重试')
  }
}

// 更新AI模型设置
const updateAiSettings = () => {
  console.log('更新AI模型设置:', aiForm.value)
  localStorage.setItem('aiSettings', JSON.stringify(aiForm.value))
  alert('AI模型设置保存成功')
}
</script>

<style scoped>
.change-password {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 40px;
}

/* 标签页样式 */
.settings-tabs {
  display: flex;
  margin-bottom: 30px;
  border-bottom: 1px solid #e9ecef;
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: #3498db;
}

.tab-btn.active {
  border-bottom-color: #3498db;
  color: #3498db;
  font-weight: 500;
}

/* 表单样式 */
.change-password-form,
.ai-settings-form {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
}

.form-actions {
  margin-top: 30px;
  text-align: center;
}

/* 模型API设置样式 */
.model-apis {
  margin-top: 30px;
}

.model-apis h4 {
  color: #333;
  margin-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 10px;
}

.form-text {
  font-size: 12px;
  color: #6c757d;
  margin-top: 5px;
  display: block;
}

/* 模型选项样式 */
.model-options {
  display: flex;
  gap: 30px;
  margin-top: 10px;
}

.model-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.model-option input[type="radio"] {
  width: auto;
  margin: 0;
}

.model-option span {
  font-size: 14px;
  color: #555;
}

/* 按钮样式 */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  text-decoration: none;
}

.btn-primary {
  background-color: #3498db;
  color: white;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
}

.btn-primary:hover {
  background-color: #2980b9;
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.4);
}

/* API文档样式 */
.api-documentation {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.api-section {
  margin-bottom: 40px;
}

.api-section h2 {
  color: #4a4a4a;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.api-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.api-card h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 15px;
}

.api-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.api-method {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  color: white;
  width: 80px;
  text-align: center;
}

.api-method.get {
  background-color: #4CAF50;
}

.api-method.post {
  background-color: #2196F3;
}

.api-method.put {
  background-color: #FF9800;
}

.api-method.delete {
  background-color: #f44336;
}

.api-url {
  font-family: monospace;
  font-size: 16px;
  color: #333;
  background-color: #e8e8e8;
  padding: 8px;
  border-radius: 4px;
}

.api-description {
  color: #666;
  font-size: 14px;
}

.api-request, .api-response {
  margin-top: 10px;
}

.api-request h4, .api-response h4 {
  margin: 0 0 5px 0;
  color: #4a4a4a;
  font-size: 14px;
}

.api-request pre, .api-response pre {
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 14px;
  overflow-x: auto;
  margin: 0;
}
</style>