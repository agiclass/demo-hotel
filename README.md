# 酒店查询客服

[![codecov](https://codecov.io/gh/toddlt/hotel-chatbot/branch/main/graph/badge.svg?token=hotel-chatbot_token_here)](https://codecov.io/gh/toddlt/hotel-chatbot)
[![CI](https://github.com/toddlt/hotel-chatbot/actions/workflows/main.yml/badge.svg)](https://github.com/toddlt/hotel-chatbot/actions/workflows/main.yml)

[酒店原始数据](https://raw.githubusercontent.com/thu-coai/CrossWOZ/master/data/crosswoz/database/hotel_db.json)

[对话原始数据](https://raw.githubusercontent.com/thu-coai/CrossWOZ/master/data/crosswoz/train.json.zip)

- 📦 基本的setup.py文件，用于提供安装、打包和分发服务，模板使用setuptools
- 🤖 带有常用命令的Makefile，用于安装、测试、清理、格式化和发布您的项目。
- 🐋 带有Dockerfile和docker-compose.yml，用于构建容器镜像和依赖的服务。
- 📃 使用mkdocs的文档结构
- 🧪 使用pytest的测试结构
- ✅ 使用flake8进行代码清理
- 📊 使用codecov生成代码覆盖率报告

## 安装与使用

1. 使用conda或venv创建python虚拟环境
2. 安装依赖 `pip install -r requirements.txt`
3. 使用Docker启动向量数据库服务 `docker-compose up -d`
4. 运行主脚本 `python -m hotel_chatbot --help`
   - 网页界面 `python -m hotel_chatbot web`
   - 命令界面 `python -m hotel_chatbot cli`
5. 可安装到全局使用 `python setup.py install`

命令界面：

<img src=docs/media/screenshot-cli.png width=450 />

网页界面：

<img src=docs/media/screenshot-web.png width=600 />
