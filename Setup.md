# *Notice File Question & Answer*

**基于BERT和知识推理的校园通告/通知智能问答系统**

*修订记录*

| 时间      | 版本 | 作者   | 备注           |
| --------- | ---- | ------ | -------------- |
| 2022.3.18 | V1.0 | 尚若冰 | 编写第一版文档 |
|           |      |        |                |

[TOC]

## 安装说明

***NFQA由Word文件+图数据库Neo4j+MySQL+前端+后端组成，请按照接下来的步骤进行安装使用。***



### Neo4j

Neo4j的数据文件为:graph-dbms-neo4j.dump

安装步骤：

1. 首先点击Reveal files in File Explorer按钮打开数据文件目录，将Neo4j的数据文件(.dump)拷贝至该目录，之后在软件界面可见Project-File包含数据文件![image-20220318075943084](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318075943084.png)

2. 点击蓝色Open按钮右边的省略号，Create new DBMS from dump<img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080202960.png" alt="image-20220318080202960" style="zoom: 67%;" />

3. 在配置好用户名和密码后，点击Create，图数据库初始化完成

   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080340917.png" alt="image-20220318080340917" style="zoom:50%;" />

4. 之后的使用，在项目中点击Start，当数据库显示如下(ACTIVE)，代表成功运行![image-20220318080557830](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080557830.png)

5. 点击蓝色按钮Open，打开图数据库浏览器，看到如下界面，恭喜你完成图数据库的安装🎉🎉![image-20220318080722161](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318080722161.png)



### Django后端

准备步骤：

1. 安装Git bash，并配置相应的用户名和邮箱以及**环境变量**⚠ [Git 安装配置 | 菜鸟教程 (runoob.com)](https://www.runoob.com/git/git-install-setup.html)
   ```
   git config --global user.name "Your Name"
   git config --global user.email "Your Email"
   ```

2. 注册一个Gitee账号(可以把它看作中国版的Github)

3. 点击右端的Fork按钮，Fork后端项目[NFQA后端开发](https://gitee.com/shangruobing/nfqa-backend-development)![image-20220318082816637](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318082816637.png)

4. 点击橙色的克隆/下载按钮，复制仓库的HTTPS或SSH的地址

   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318082925417.png" alt="image-20220318082925417" style="zoom:50%;" />

5. 在你想要安装后端的文件夹下，打开CMD输入git clone + 刚刚复制的项目地址

   ```shell
   git clone git@gitee.com:shangruobing/nfqa-backend-development.git
   ```

6. 稍等片刻，出现下图，即安装成功![image-20220318083629177](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318083629177.png)

7. 接下来我们可以发现，已经成功的把Git仓库中的Project，Clone到我们本地的计算机中

8. 接下来我们需要配置Python环境，安装第三方依赖包，使用Pycharm打开后端项目，可以看到项目目录中含有一个requirements.txt文件，这个文来负责记录Python环境需要的依赖包，我们可以通过如下命令安装所有的项目依赖，如果有该文件未记录的依赖，请及时与我反馈。
   ```shell
   pip install -r requirements.txt
   ```

9. 完成Django的模型迁移

   ```
   python manage.py makemigrations
   ```

   ```
   python manage.py migrate
   ```
   ⚠***需要把settings.py文件中的MySQL用户和密码改为自己的***
   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318104322296.png" alt="image-20220318104322296" style="zoom: 67%;" />

   ⚠需要把views.py文件中的neo4j连接的auth改为自己的用户名和密码

   ![image-20220318113051781](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318113051781.png)

10. 安装自定义jieba字典，字典数据文件为：myDict.txt,放置在后端项目/public/下即可

11. 使用下述命令启动Django，如果启动正常，说明Django后端安装完成，恭喜🎉

   ```shell
   python manage.py runserver
   ```

### MySQL

MySQL的数据文件为:qas_notice.sql

安装步骤:

1. 安装好MySQL数据库

2. 安装数据库管理器Navicat(可选，推荐)

3. 注意需要先进行Django的模型迁移，再进行之后步骤

   ```
   python manage.py makemigrations
   ```

   ```
   python manage.py migrate
   ```

4. 完成Django模型迁移后，在DBMS中执行qas_notice.sql中的插值命令

### Word

*Word文件的存在是为了实现通知文件预览功能，Word不存在，并不影响系统运行*

Word的数据文件为：Word合集.zip

将Word合集解压至 后端项目/public/Word文件夹下即可

<img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318082452461.png" alt="image-20220318082452461" style="zoom:67%;" />



**到此后端部分，部署完成！**🎉

------

### Vue前端

1. 安装Node.js [Download Node.js](https://nodejs.dev/download) ⚠需要配置环境变量

2. 点击右端的Fork按钮，Fork我的前端项目[NFQA前端开发](https://gitee.com/shangruobing/nfqa-front-end-development)

3. 按照之前介绍后端的流程，将前端项目Clone到本地

4. 切换到项目目录，使用如下命令安装前端依赖包

   ```shell
   npm install
   ```
   ⚠注意npm可能下载速度会很慢，可以考虑换源为淘宝镜像，具体步骤如下

   ```shell
   npm install -g cnpm --registry=https://registry.npm.taobao.org
   ```

   之后使用下述命令安装前端依赖包
   ```shell
   cnpm install
   ```
   
5. 使用如下命令,运行Vite服务器
   
   ```shell
   npm run dev
   ```
   
6. 出现如下界面，恭喜，前端安装完成并且成功启动!🎉

   <img src="C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220318085656983.png" alt="image-20220318085656983" style="zoom:67%;" />

------

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