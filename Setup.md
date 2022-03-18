# *Notice File Question & Answer*

**基于BERT和知识推理的校园通告/通知智能问答系统**

## 安装说明

***NFQA由Word文件+图数据库Neo4j+MySQL+前端+后端组成，请按照接下来的步骤进行安装使用。***

### 数据库

#### 图数据库Neo4j

Neo4j的数据文件为:graph-dbms-neo4j.dump

安装步骤：

1. 首先将Neo4j的数据文件拷贝到Neo4j的数据目录，之后在软件界面可见Project-File包含数据文件![image-20220318075943084](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318075943084.png)

2. 点击蓝色Open按钮右边的省略号、Create new DBMS from dump<img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080202960.png" alt="image-20220318080202960" style="zoom: 67%;" />

3. 在配置好用户名和密码后，图数据库初始化完成

   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080340917.png" alt="image-20220318080340917" style="zoom:50%;" />

4. 之后的使用，在项目中点击Start，当数据库显示如下(ACTIVE)，代表成功运行![image-20220318080557830](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080557830.png)

5. 打开图数据库浏览器，看到如下界面，恭喜你完成这一步。![image-20220318080722161](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080722161.png)

#### MySQL

MySQL的数据文件为:qas_notice.sql

安装步骤:

1. 安装好MySQL数据库
2. 安装数据库管理器Navicat(可选，推荐)
3. 在DBMS中执行qas_notice.sql的建表和插值命令

### 后端

准备步骤：

1. 注册一个Gitee账号(可以把它看作中国版的Github)

2. 点击右端的Fork按钮，Fork我的后端项目[NFQA后端开发](https://gitee.com/shangruobing/nfqa-backend-development)![image-20220318082816637](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318082816637.png)

3. 点击橙色的克隆/下载按钮，复制仓库的HTTPS或SSH的地址

   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318082925417.png" alt="image-20220318082925417" style="zoom:50%;" />

4. 在你想要安装后端的文件夹下，打开CMD输入git clone + 刚刚复制的项目地址

   ```shell
   git clone git@gitee.com:shangruobing/nfqa-backend-development.git
   ```

5. 稍等片刻，出现下图，即安装成功![image-20220318083629177](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318083629177.png)

6. 接下来我们可以发现，已经成功的把Git仓库中的Project，Clone到我们本地的计算机中

7. 接下来我们需要配置Python环境，安装第三方依赖包，可以看到项目目录中含有一个requirements.txt文件，这个文件用来负责记录Python环境需要的依赖包，我们可以通过如下命令安装所有的项目依赖，如果有文件中缺少的库，请及时与我反馈。
   ```shell
   pip install -r requirements.txt
   ```

8. 使用下述命令启动Django，如果启动正常，说明后端安装完成，恭喜

   ```shell
   python manage.py runserver
   ```


### 前端

1. 安装Node.js [Download Node.js](https://nodejs.dev/download)

2. 点击右端的Fork按钮，Fork我的前端项目[NFQA前端开发](https://gitee.com/shangruobing/nfqa-front-end-development)

3. 按照之前介绍后端的流程，将前端项目Clone到本地

4. 切换到项目目录，使用如下命令安装前端依赖包

   ```shell
   npm install
   ```

5. 使用如下命令,运行Vite服务器
   
   ```shell
   npm run dev
   ```
   
6. 出现如下界面，恭喜，前端安装完成并且成功启动!

   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318085656983.png" alt="image-20220318085656983" style="zoom:67%;" />

### Word

*Word文件的存在是为了实现通知文件预览功能，Word不存在，并不影响系统运行*

Word的数据文件为：Word合集.zip

将Word合集解压至 后端项目/public/Word文件夹下即可

<img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318082452461.png" alt="image-20220318082452461" style="zoom:67%;" />



## 运行说明

***在成功安装上述所有步骤后，便可以正式体验我们的问答机器人啦！***

启动步骤：

1. 启动图数据库

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