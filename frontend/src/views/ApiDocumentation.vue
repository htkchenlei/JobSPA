<template>
  <div class="api-documentation">
    <h1>对外API接口文档</h1>
    
    <!-- 公共API（无需鉴权） -->
    <section class="api-section">
      <h2>公共API（无需鉴权）</h2>
      <div class="api-card highlight">
        <h3>获取本周项目更新</h3>
        <div class="api-details">
          <div class="api-method get">GET</div>
          <div class="api-url">/api/public/weekly-updates</div>
          <div class="api-description">获取从上周六到调用当天的所有项目更新记录，此接口无需登录认证。</div>
          <div class="api-notice">
            <strong>注意：</strong>此接口为公开接口，无需携带任何认证信息。时间范围自动计算：从上周六00:00到当前日期23:59。
          </div>
          <div class="api-request">
            <h4>请求示例（curl）：</h4>
            <pre>curl http://your-domain.com/api/public/weekly-updates</pre>
          </div>
          <div class="api-response">
            <h4>成功响应示例：</h4>
            <pre>{
  "success": true,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "project_id": 1,
      "project_name": "项目名称",
      "client_name": "客户名称",
      "project_stage": 3,
      "project_stage_text": "招投标",
      "update_content": "项目阶段由2变更为3",
      "update_date": "2024-01-15",
      "update_time": "10:30:00",
      "updated_by": "用户名",
      "is_important": 0
    }
  ],
  "count": 1,
  "time_range": {
    "start_date": "2024-01-13",
    "end_date": "2024-01-15"
  }
}</pre>
          </div>
        </div>
      </div>
      
      <div class="api-card">
        <h3>获取本周更新数量</h3>
        <div class="api-details">
          <div class="api-method get">GET</div>
          <div class="api-url">/api/public/weekly-updates/count</div>
          <div class="api-description">获取从上周六到调用当天的项目更新记录总数。</div>
          <div class="api-request">
            <h4>请求示例（curl）：</h4>
            <pre>curl http://your-domain.com/api/public/weekly-updates/count</pre>
          </div>
          <div class="api-response">
            <h4>成功响应示例：</h4>
            <pre>{
  "success": true,
  "count": 15,
  "time_range": {
    "start_date": "2024-01-13",
    "end_date": "2024-01-15"
  }
}</pre>
          </div>
        </div>
      </div>
      
      <div class="api-card highlight">
        <h3>获取当月项目更新</h3>
        <div class="api-details">
          <div class="api-method get">GET</div>
          <div class="api-url">/api/public/monthly-updates</div>
          <div class="api-description">获取当月（1号至调用当天）的全部项目更新记录。</div>
          <div class="api-request">
            <h4>请求示例（curl）：</h4>
            <pre>curl http://your-domain.com/api/public/monthly-updates</pre>
          </div>
          <div class="api-response">
            <h4>成功响应示例：</h4>
            <pre>{
  "success": true,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "project_id": 1,
      "project_name": "项目名称",
      "client_name": "客户名称",
      "project_stage": 3,
      "project_stage_text": "招投标",
      "update_content": "项目阶段由2变更为3",
      "update_date": "2024-01-15",
      "update_time": "10:30:00",
      "updated_by": "用户名",
      "is_important": 0
    }
  ],
  "count": 1,
  "time_range": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-15"
  }
}</pre>
          </div>
        </div>
      </div>
      
      <div class="api-card highlight">
        <h3>获取指定日期范围的项目更新</h3>
        <div class="api-details">
          <div class="api-method get">GET</div>
          <div class="api-url">/api/public/range-updates</div>
          <div class="api-description">获取指定时间范围内的全部项目更新记录。需要提供开始和结束日期参数。</div>
          <div class="api-request">
            <h4>查询参数：</h4>
            <pre>start_date=YYYY-MM-DD（必填）&amp;end_date=YYYY-MM-DD（必填）</pre>
            <h4>请求示例（curl）：</h4>
            <pre>curl "http://your-domain.com/api/public/range-updates?start_date=2024-01-01&amp;end_date=2024-01-15"</pre>
          </div>
          <div class="api-response">
            <h4>成功响应示例：</h4>
            <pre>{
  "success": true,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "project_id": 1,
      "project_name": "项目名称",
      "client_name": "客户名称",
      "project_stage": 3,
      "project_stage_text": "招投标",
      "update_content": "项目阶段由2变更为3",
      "update_date": "2024-01-15",
      "update_time": "10:30:00",
      "updated_by": "用户名",
      "is_important": 0
    }
  ],
  "count": 1,
  "time_range": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-15"
  }
}</pre>
            <h4>错误响应示例（缺少参数）：</h4>
            <pre>{
  "success": false,
  "message": "缺少必要参数: start_date 和 end_date 均为必填项"
}</pre>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// API文档页面组件
</script>

<style scoped>
.api-documentation {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  height: 100vh;
  overflow-y: auto;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 40px;
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

.api-card.highlight {
  background: linear-gradient(135deg, #f0fff4 0%, #fff3e6 100%);
  border: 2px solid #4ade80;
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

.api-notice {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 10px 15px;
  border-radius: 4px;
  margin: 10px 0;
  color: #856404;
  font-size: 14px;
}
</style>
