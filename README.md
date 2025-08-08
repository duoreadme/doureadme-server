# GitHub README Searcher API

一个基于Python的GitHub仓库搜索API服务，用于搜索GitHub上的高星仓库并获取README内容。该服务直接使用GitHub API，按星数降序排序并返回前N个仓库，提供RESTful API接口。

## 功能特性

- 🔍 搜索特定领域的高星GitHub仓库
- ⭐ 按星数降序排序，自动选择最热门的仓库
- 📖 自动获取仓库的README内容
- 🌐 提供REST API接口（端口5088）
- ⚡ 异步处理，性能优异
- 🚀 简单易用，无需Docker
- 🏗️ 标准化的项目结构，易于维护和扩展

## 项目结构

```
github-readme-searcher/
├── app/                          # 主应用包
│   ├── __init__.py
│   ├── api/                      # API模块
│   │   ├── __init__.py
│   │   ├── app.py               # FastAPI应用
│   │   └── routes.py            # API路由
│   ├── config/                   # 配置模块
│   │   ├── __init__.py
│   │   └── settings.py          # 应用配置
│   ├── core/                     # 核心功能模块
│   │   ├── __init__.py
│   │   ├── models.py            # 数据模型
│   │   └── searcher.py          # GitHub API搜索器
│   └── utils/                    # 工具模块
│       └── __init__.py
├── tests/                        # 测试套件
│   ├── __init__.py
│   └── test_searcher.py         # 搜索器测试
├── docs/                         # 文档
│   └── API.md                   # API文档
├── main.py                      # API服务器入口
├── requirements.txt             # Python依赖
├── setup.py                     # 安装配置
├── pyproject.toml              # 项目配置
├── Makefile                     # 构建脚本
├── Dockerfile                   # Docker配置
├── docker-compose.yml          # Docker Compose配置
├── .env.example                # 环境变量示例
└── README.md                   # 项目文档
```

## 安装

### 1. 克隆仓库

```bash
git clone <repository-url>
cd github-readme-searcher
```

### 2. 安装依赖

#### 生产环境
```bash
pip install -r requirements.txt
```

#### 开发环境
```bash
make install-dev
# 或者
pip install -r requirements.txt
pip install -e ".[dev]"
```

### 3. 配置GitHub Token

创建 `.env` 文件并添加你的GitHub Personal Access Token：

```bash
cp env.example .env
```

编辑 `.env` 文件：

```env
GITHUB_TOKEN=your_github_personal_access_token_here
```

**获取GitHub Token的步骤：**

1. 访问 [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token (classic)"
3. 选择以下权限：
   - `repo` (完整的仓库访问权限)
   - `read:user` (读取用户信息)
   - `read:org` (读取组织信息)
4. 生成并复制token到 `.env` 文件

## 使用方法

### REST API服务

#### 启动API服务器

```bash
# 使用主入口文件
python main.py

# 使用uvicorn直接启动
uvicorn app.api.app:app --host 0.0.0.0 --port 5088

# 使用Makefile
make run-api
```

服务器将在 `http://localhost:5088` 启动。

#### API端点

**1. 健康检查**
```bash
curl http://localhost:5088/api/v1/health
```

**2. 搜索仓库（带README）**
```bash
curl -X POST http://localhost:5088/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "machine learning",
    "limit": 5
  }'
```

**3. 简单搜索**
```bash
curl "http://localhost:5088/api/v1/search/machine%20learning?limit=5"
```

**4. 快速搜索（无README）**
```bash
curl "http://localhost:5088/api/v1/search/machine%20learning/no-readme?limit=5"
```

**5. 获取热门领域**
```bash
curl http://localhost:5088/api/v1/domains
```

**6. 获取API统计信息**
```bash
curl http://localhost:5088/api/v1/stats
```

#### API文档

访问 `http://localhost:5088/docs` 查看交互式API文档。

### 直接使用Python模块

```python
import asyncio
from app.core.searcher import GitHubAPISearcher

async def main():
    # 使用async context manager
    async with GitHubAPISearcher() as searcher:
        # 搜索仓库并获取README
        repositories = await searcher.search_and_get_readmes(
            domain="machine learning",
            limit=5
        )
        
        # 处理结果
        for repo in repositories:
            print(f"Repository: {repo.full_name}")
            print(f"Stars: {repo.stars}")
            print(f"README: {repo.readme_content[:200]}...")

# 运行
asyncio.run(main())
```

## 开发

### 运行测试

```bash
# 运行所有测试
make test

# 运行测试并生成覆盖率报告
make test-coverage

# 直接使用pytest
pytest tests/ -v
```

### 代码格式化

```bash
# 格式化代码
make format

# 检查代码格式
make format-check
```

### 代码检查

```bash
# 运行linting
make lint

# 运行所有检查（格式、lint、测试）
make check
```

### 清理

```bash
# 清理生成的文件
make clean
```

## Docker部署

### 构建镜像

```bash
make docker-build
# 或者
docker build -t github-readme-searcher .
```

### 运行容器

```bash
make docker-run
# 或者
docker run -p 5088:5088 --env-file .env github-readme-searcher
```

### 使用Docker Compose

```bash
docker-compose up -d
```

## 支持的搜索领域

该服务支持搜索各种技术领域，包括但不限于：

- 机器学习 (machine learning)
- 人工智能 (artificial intelligence)
- Web开发 (web development)
- 移动开发 (mobile development)
- 数据科学 (data science)
- 区块链 (blockchain)
- 网络安全 (cybersecurity)
- DevOps
- 前端框架 (React, Vue, Angular)
- 编程语言 (Python, JavaScript, TypeScript, Go, Rust)
- 容器技术 (Docker, Kubernetes)
- 微服务 (microservices)
- API开发
- 数据库
- 云计算
- 无服务器 (serverless)
- 游戏开发 (game development)
- 计算机视觉 (computer vision)
- 自然语言处理 (natural language processing)
- 深度学习 (deep learning)

## 技术架构

- **模块化设计**: 清晰的分层架构，易于维护和扩展
- **配置管理**: 统一的环境变量和配置管理
- **直接GitHub API集成**: 无需MCP或Docker
- **按星数排序**: 自动按星数降序排序，返回最热门的仓库
- **异步处理**: 使用asyncio进行异步操作
- **REST API**: 基于FastAPI提供Web服务
- **端口5088**: 默认API服务端口
- **测试覆盖**: 完整的单元测试套件
- **Docker支持**: 容器化部署支持

## 依赖项

- `aiohttp`: 异步HTTP客户端
- `fastapi`: Web框架
- `uvicorn`: ASGI服务器
- `python-dotenv`: 环境变量管理
- `pydantic`: 数据验证
- `pytest`: 测试框架
- `pytest-asyncio`: 异步测试支持

## 故障排除

### 常见问题

1. **GitHub Token无效**
   ```
   Error: Bad credentials
   ```
   解决方案：检查GitHub Token是否正确设置，确保有足够权限

2. **网络连接问题**
   ```
   Error: Connection timeout
   ```
   解决方案：检查网络连接，确保可以访问GitHub API

3. **端口被占用**
   ```
   Error: Address already in use
   ```
   解决方案：检查端口5088是否被其他程序占用，或修改端口

4. **导入错误**
   ```
   ModuleNotFoundError: No module named 'app'
   ```
   解决方案：确保在项目根目录运行命令，或设置PYTHONPATH

### 调试模式

启用详细日志：

```bash
export PYTHONPATH=.
python -u main.py
```

## 贡献

欢迎提交Issue和Pull Request！

### 开发流程

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 代码规范

- 使用Black进行代码格式化
- 使用Flake8进行代码检查
- 使用MyPy进行类型检查
- 编写单元测试
- 更新文档

## 许可证

MIT License

## 致谢

- [GitHub API](https://docs.github.com/en/rest) - GitHub REST API
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Web框架
- [Pydantic](https://pydantic-docs.helpmanual.io/) - 数据验证
- [aiohttp](https://docs.aiohttp.org/) - 异步HTTP客户端 