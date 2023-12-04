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

### 第一步：安装依赖

```
pip install -r requirements.txt
```

### 第二步：准备环境变量

##### 进入项目目录，并且复制 `.env.example` 生成新的配置文件 `.env`

```
cp .env.example .env
```

##### 准备好环境变量：
ps: .env.example 给大家带的配置文件仅供参考

```.env 
OPENAI_API_KEY=
WEAVIATE_URL=
WEAVIATE_API_KEY=
```

##### 去 OpenAI 官方获取

`OPENAI_API_KEY` 从 OpenAI 官方获取 api 的 key

##### 获取 weaviate 向量数据库相关配置

去官网 https://console.weaviate.cloud/ 注册登录，可以免费创建向量数据库，然后复制相关配置
`WEAVIATE_URL` 
`WEAVIATE_API_KEY` 

* 注意：免费的有效期 14天

### 第三步：初始化数据

##### 执行下面命令
```
python -m hotel_chatbot cli
```

##### 在弹出的界面输入：

第一步输入：`create` #用于创建数据结构

第二步输入：`insert` #用于初始化数据

### 第四步：启动 web 界面
```
python -m hotel_chatbot web
```

#### 建议问题：

* 推荐一下奢华的酒店
* 帮忙推荐一下可以打牌的酒店

### 备注 
1.查看帮助 `python -m hotel_chatbot --help`
2.可安装到全局使用 `python setup.py install`

### 如果你会 Docker

可以私有化本地部署向量数据库，在根目录直接执行命令。

连接数据库的配置需要更改

```
docker-compose up -d
```

#### Cli 提问方式
<img src=docs/media/screenshot-cli.png width=450 />

#### web网页界面提问方式：

<img src=docs/media/screenshot-web.png width=600 />
