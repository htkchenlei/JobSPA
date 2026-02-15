<template>
  <div class="logs">
    <h3>日志查询</h3>
    <div class="logs-filter">
      <div class="form-group">
        <label>日志类型</label>
        <select class="form-control">
          <option value="">全部</option>
          <option value="project">项目操作</option>
          <option value="todo">待办操作</option>
          <option value="file">文件操作</option>
          <option value="user">用户操作</option>
        </select>
      </div>
      <div class="form-group">
        <label>时间范围</label>
        <div class="date-range">
          <input type="date" class="form-control">
          <span>至</span>
          <input type="date" class="form-control">
        </div>
      </div>
      <div class="form-group">
        <label>关键词</label>
        <input type="text" class="form-control" placeholder="输入关键词">
      </div>
      <button class="btn btn-primary">查询</button>
    </div>
    <div class="logs-list">
      <table class="logs-table">
        <thead>
          <tr>
            <th>时间</th>
            <th>类型</th>
            <th>操作人</th>
            <th>操作内容</th>
            <th>IP地址</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>2026-01-01 10:00:00</td>
            <td>项目操作</td>
            <td>Admin</td>
            <td>创建项目 "企业官网建设"</td>
            <td>127.0.0.1</td>
          </tr>
          <tr>
            <td>2026-01-01 10:30:00</td>
            <td>项目操作</td>
            <td>Admin</td>
            <td>更新项目 "企业官网建设" 状态为 "项目立项"</td>
            <td>127.0.0.1</td>
          </tr>
          <tr>
            <td>2026-01-01 11:00:00</td>
            <td>待办操作</td>
            <td>Admin</td>
            <td>创建待办事项 "完成项目方案"</td>
            <td>127.0.0.1</td>
          </tr>
          <tr>
            <td>2026-01-01 11:30:00</td>
            <td>文件操作</td>
            <td>Admin</td>
            <td>上传文件 "项目方案.docx"</td>
            <td>127.0.0.1</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.logs {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logs-filter {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: end;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-range input {
  flex: 1;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.logs-list {
  overflow-x: auto;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
}

.logs-table th,
.logs-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

.logs-table th {
  background-color: #f8f9fa;
  font-weight: 500;
}

.logs-table tr:hover {
  background-color: #f8f9fa;
}
</style>