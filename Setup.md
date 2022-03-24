# NFQA开发环境部署文档

**基于BERT和知识推理的校园通告/通知智能问答系统**

## 修订记录

| 时间      | 版本 | 作者   | 备注           |
| --------- | ---- | ------ | -------------- |
| 2022.3.18 | V1.0 | 尚若冰 | 编写第一版文档 |
| 2022.3.20 | V1.2 | 尚若冰 | 修改了文档结构 |
| 2022.3.22 | V1.5 | 尚若冰 | 订正部分错误   |

## 目录
[TOC]

## 文件清单

| 文件名称              | 作用                               | 备注                             |
| --------------------- | ---------------------------------- | -------------------------------- |
| graph-dbms-neo4j.dump | neo4j的数据文件                    |                                  |
| ~~mydict.txt~~        | jieba的自定义字典                  | ***已上传至Gitee,无需手动安装*** |
| qas_notice.sql        | mysql的通知表插值语句              |                                  |
| Word.zip              | word文件合集，有1K个左右的通知文件 |                                  |



## 部署说明

**NFQA由前端+后端+数据库+文件资源组成，请按照接下来的步骤进行安装使用。**

- 前端:Vue3 Element-Plus Vite Vue-Router
- 后端:Django Django-Rest-Framework
- 数据库:MySQL Neo4j(Graph Database）
- 文件资源:自定义词典 Word文件



### Neo4j

Neo4j的数据文件为:graph-dbms-neo4j.dump *详见文件清单*

安装步骤：

1. 首先点击Project中的Reveal files in File Explorer按钮打开数据文件目录，将Neo4j的数据文件(.dump)拷贝至该目录，之后在软件界面可见Project-File包含数据文件![image-20220318162656126](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318162656126.png)
2. 点击蓝色Open按钮右边的省略号，Create new DBMS from dump<img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318163053132.png" alt="image-20220318163053132" style="zoom: 50%;" />
3. 在配置好用户名和密码后，点击Create，图数据库初始化完成
<img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080340917.png" alt="image-20220318080340917" style="zoom:50%;" />
4. 之后的使用，在Project中点击Start，当数据库显示如下(ACTIVE)，代表成功运行![image-20220318080557830](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080557830.png)
5. 点击蓝色按钮Open，打开图数据库浏览器，看到如下界面，恭喜你完成图数据库的安装🎉🎉![image-20220318080722161](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080722161.png)



### Django后端

准备步骤：

1. 安装Git bash，并配置相应的用户名和邮箱以及**环境变量**⚠
   参考文档:[Git 安装配置|菜鸟教程 (runoob.com)](https://www.runoob.com/git/git-install-setup.html)
   
   ```
   git config --global user.name "Your Name"
   git config --global user.email "Your Email"
   ```
   
2. 注册一个Gitee账号(可以把它看作中国版的Github)

3. 点击右端的Fork按钮，Fork后端项目

   项目链接:[NFQA后端开发](https://gitee.com/shangruobing/nfqa-backend-development)![image-20220318082816637](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318082816637.png)

4. 点击橙色的克隆/下载按钮，复制仓库的HTTPS或SSH的地址

   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318082925417.png" alt="image-20220318082925417" style="zoom:50%;" />

5. 在想要安装后端项目的文件夹下，打开CMD输入git clone + 刚刚复制的项目地址

   ```shell
   git clone git@gitee.com:shangruobing/nfqa-backend-development.git
   ```

6. 稍等片刻，出现下图，代表成功！可以发现，Git仓库中的Project已经Clone到我们的计算机当中![image-20220318083629177](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318083629177.png)

7. 接下来我们需要配置Python环境，安装第三方依赖包，使用Pycharm打开后端项目，可以看到项目目录中含有一个requirements.txt文件，这个文件用来记录Python环境需要的依赖包。
   **我们可以通过如下命令安装所有的项目依赖**，如果有该文件未记录的依赖，请及时与我反馈。

   ```shell
   pip install -r requirements.txt
   ```

8. 打开终端，切换到后端的APP目录，完成Django的模型迁移

   ```
   python manage.py makemigrations
   ```

   ```
   python manage.py migrate
   ```
   #### 注意事项

   ⚠**需要把settings.py文件中的MySQL用户和密码改为自己的用户名和密码**

   ```python
   DATABASES = {
       'default':
           {
               'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
               'NAME': 'NFQA',  # 数据库名称
               'HOST': '127.0.0.1',  # 数据库地址，本机 ip 地址 127.0.0.1
               'PORT': 3306,  # 端口
               'USER': 'root',  # 数据库用户名
               'PASSWORD': 'Your Password',  # 数据库密码
           }
   }
   ```

   ⚠**需要把views.py文件中的neo4j连接的auth改为自己的用户名和密码**

   ```python
   try:
       graph = Graph("http://localhost:7474", auth=("neo4j", "010209"))
       print("Neo4j graph database connection succeeded")
   except py2neo.errors.ConnectionUnavailable:
       raise APIException("Neo4j graph database connection failed")
   ```

9. 使用下述命令启动Django，出现下图结果，代表Django成功启动，至此Django安装完成，恭喜🎉

   ```shell
   python manage.py runserver
   ```

<img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318165749490.png" alt="image-20220318165749490" style="zoom:50%;" />


### MySQL

MySQL的数据文件为:qas_notice.sql *详见文件清单*

安装步骤:

1. 安装好MySQL数据库
2. 安装数据库管理器Navicat(可选，推荐)
3. 在Navicat或MySQL Workbench中执行qas_notice.sql中的SQL语句



### Vue前端

1. 安装Node.js ⚠需要配置环境变量

   参考链接：[Download Node.js](https://nodejs.dev/download) 

2. 点击右端的Fork按钮，Fork前端项目

   项目链接：[NFQA前端开发](https://gitee.com/shangruobing/nfqa-front-end-development)

3. 按照之前介绍后端的流程，将前端项目Clone到本地

4. 切换到项目目录，使用如下命令安装前端依赖包

   ```shell
   npm install
   ```
   ⚠注意npm可能下载速度会很慢，可以考虑换源为淘宝镜像，命令如下

   ```shell
   npm install -g cnpm --registry=https://registry.npm.taobao.org
   ```

   之后使用下述命令安装前端依赖包
   ```shell
   cnpm install
   ```

5. 依赖安装完成后，使用如下命令,运行Vite服务器

   ```shell
   npm run dev
   ```

6. 出现如下界面，恭喜，前端安装完成并且成功启动!🎉

   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318085656983.png" alt="image-20220318085656983" style="zoom:67%;" />
   
   
   
### Word文件部署

   ⚠**Word文件资源不存在，只会影响文件预览功能，不影响系统运行**

   Word的数据文件为：Word合集.zip *详见文件清单

   将Word合集解压至 后端项目/public/Word文件夹下即可

   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318082452461.png" alt="image-20220318082452461" style="zoom:67%;" />

------



## 运行说明

***在成功完成所有步骤后，便可以正式体验我们的问答机器人啦！***🎉

启动步骤：

1. 启动图数据库neo4j

2. 启动MySQL服务

3. 启动Django服务器

   ```shell
   python manage.py runserver
   ```

4. 启动Vite服务器

   ```shell
    npm run dev
   ```

5. 体验并及时记录、反馈🎉🎉



## 目前存在的问题

- [x] 部分电脑，百度Paddle模型无法运行，从而会导致jieba的语义识别出问题

  参数如下:paddlepaddle-tiny==1.6.1

  日志如下:
  
  ```
  PaddleCheckError: Cannot open file C:\Users\吴翰芃\AppData\Local\Programs\Python\
  Python37\lib\site-packages\jieba\lac_small\model_baseline\word_emb for load op at [D:\paddle-tiny-release-liujinquan\1.6.1-tiny\Paddle\paddle/fluid/operators/
  load_op.h:37]
  [operator < load > error]
  ```
  
  解决办法:用管理员模式执行Django的启动脚本

