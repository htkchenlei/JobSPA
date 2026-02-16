# 项目根目录
$PROJECT_ROOT = Get-Location
# NAS地址
$NAS_ADDRESS = "192.168.2.2"
# NAS上的项目目录
$NAS_PROJECT_DIR = "/volume1/docker/JobSPA"

# 构建Docker镜像
Write-Host "构建Docker镜像..."
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "构建失败，请检查错误信息"
    exit 1
}

Write-Host "构建成功！"

Write-Host "项目打包完成！"
Write-Host "请手动执行以下步骤上传到NAS："
Write-Host "1. 保存Docker镜像：docker save jobspa-backend jobspa-frontend -o jobspa_images.tar"
Write-Host "2. 上传镜像到NAS：scp jobspa_images.tar admin@$NAS_ADDRESS:$NAS_PROJECT_DIR/"
Write-Host "3. 上传docker-compose.yml：scp docker-compose.yml admin@$NAS_ADDRESS:$NAS_PROJECT_DIR/"
Write-Host "4. 上传数据库文件：scp backend/projectmanagement.db admin@$NAS_ADDRESS:$NAS_PROJECT_DIR/data/"
Write-Host "5. 在NAS上启动容器：cd $NAS_PROJECT_DIR ; docker-compose up -d"
