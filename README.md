# GitHub README Searcher

一个基于Python的GitHub仓库搜索工具，用于搜索GitHub上的高星仓库并获取README内容。该工具直接使用GitHub API，按星数降序排序并返回前N个仓库，无需Docker或其他复杂依赖。

## 功能特性

- 🔍 搜索特定领域的高星GitHub仓库
- ⭐ 按星数降序排序，自动选择最热门的仓库
- 📖 自动获取仓库的README内容
- 🌐 提供REST API接口（端口5088）
- 💻 提供命令行工具
- ⚡ 异步处理，性能优异
- 🚀 简单易用，无需Docker

## 安装

### 1. 克隆仓库

```bash
git clone <repository-url>
cd github-readme-searcher
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
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

### 命令行工具

#### 基本搜索

```bash
python cli_api.py "machine learning" --limit 5
```

#### 高级选项

```bash
# 搜索高星仓库，不获取README（更快）
python cli_api.py "react" --limit 3 --no-readme

# 保存结果到文件
python cli_api.py "python" --limit 10 --output results.json

# 保存为文本格式
python cli_api.py "blockchain" --limit 3 --format txt --output results.txt

# 自定义README显示长度
python cli_api.py "web development" --limit 5 --max-readme-length 1000
```

#### 命令行参数

- `domain`: 搜索的领域/主题（必需）
- `--limit`: 返回仓库数量限制（默认：5）
- `--no-readme`: 跳过README内容获取（更快）
- `--output`: 保存结果到文件
- `--format`: 输出格式（json/txt，默认：json）
- `--max-readme-length`: README显示长度限制（默认：500）
- `--quiet`: 静默模式

### REST API服务

#### 启动API服务器

```bash
python api_server_direct.py
```

或者使用启动脚本：

```bash
./start.sh api
```

服务器将在 `http://localhost:5088` 启动。

#### API端点

**1. 健康检查**
```bash
curl http://localhost:5088/health
```

**2. 搜索仓库（带README）**
```bash
curl -X POST http://localhost:5088/search \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "machine learning",
    "limit": 5
  }'
```

**3. 简单搜索**
```bash
curl "http://localhost:5088/search/machine%20learning?limit=5"
```

**4. 快速搜索（无README）**
```bash
curl "http://localhost:5088/search/machine%20learning/no-readme?limit=5"
```

**5. 获取热门领域**
```bash
curl http://localhost:5088/domains
```

**6. 获取API统计信息**
```bash
curl http://localhost:5088/stats
```

#### API文档

访问 `http://localhost:5088/docs` 查看交互式API文档。

### 直接使用Python模块

```python
import asyncio
from github_api_searcher import GitHubAPISearcher

async def main():
    # 使用async context manager
    async with GitHubAPISearcher("your_github_token") as searcher:
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

## 项目结构

```
github-readme-searcher/
├── github_api_searcher.py     # 核心API客户端
├── cli_api.py                 # 命令行工具
├── api_server_direct.py       # FastAPI服务器（端口5088）
├── example_usage.py           # 使用示例脚本
├── test_example.py            # 测试示例（无需GitHub token）
├── start.sh                   # 便捷启动脚本
├── requirements.txt           # Python依赖
├── env.example               # 环境变量示例
└── README.md                 # 详细文档
```

## 技术架构

- **直接GitHub API集成**: 无需MCP或Docker
- **按星数排序**: 自动按星数降序排序，返回最热门的仓库
- **异步处理**: 使用asyncio进行异步操作
- **REST API**: 基于FastAPI提供Web服务
- **命令行工具**: 使用argparse提供CLI界面
- **端口5088**: 默认API服务端口

## 依赖项

- `aiohttp`: 异步HTTP客户端
- `fastapi`: Web框架
- `uvicorn`: ASGI服务器
- `python-dotenv`: 环境变量管理
- `pydantic`: 数据验证

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

### 调试模式

启用详细日志：

```bash
export PYTHONPATH=.
python -u cli_api.py "test" --limit 1
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 致谢

- [GitHub API](https://docs.github.com/en/rest) - GitHub REST API
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Web框架 