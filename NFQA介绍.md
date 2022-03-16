# *Notice File Question & Answer*

**基于BERT和知识推理的校园通告/通知智能问答系统**

[TOC]

## 项目概述

​	建立一个针对学校新近发布的通告和通知的智能问答系统，能够自动识别和理解用户提出的关于通告和通知的疑问，并自动给出比较满意的答案，来解决通告和通知在下发过程中传达效率低、理解不到位、咨询工作量大等棘手问题。

## 方案和技术路线

​	利用通知公告文件构建知识库，将知识库存入Neo4j图数据库，将BERT模型结合知识库进行参数微调，通过编写B/S应用，使用户能通过文字，语音与模型进行交互，应用将通过自然语言处理技术理解用户问题，通过检索知识库给出答案，用户亦能通过应用对答案进行评价，从而继续训练模型。

![img](file:///C:/Users/冰/AppData/Local/Temp/msohtmlclip1/01/clip_image002.png)

### 查询逻辑

![image-20220316230407263](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316230407263.png)

## 项目进度

可以在聊天框对机器人进行对话，当询问的通知文件被检索到时，可以点击消息预览及下载文件。

![image-20220316230623272](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316230623272.png)

系统可以根据自然语言处理中的实体识别和语义分析，自动、批量地将通知文件转换为如下的图：

***目前我们数据库中含有管理与经济学院近10年来的1032篇通知文件，具有16997个结点和23601个关系***

![image-20220316230723462](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316230723462.png)



## 使用案例

主要界面如下：

- 打开网页进入到系统的主界面点击机器人按钮，进入到问答界面
- 在聊天框输入提问的语句，进行提问
- 输入问题后得到的回答有三种来源



### 查询示例

#### MySQL查询

提问涉及到文件名称，如《“我爱昆工”校园文化创意产品设计大赛》，系统在字典中匹配到该项目，则直接进入MySQL查询并返回。

![image-20220316230759625](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316230759625.png)

#### Neo4j查询

提问没有涉及文件名称，则进入图数据库端的查询，利用jieba进行语义分析，同时生成Cypher查询语句。

![image-20220316230908635](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316230908635.png)

#### 查询失败，未能识别问题

![image-20220316231006495](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316231006495.png)

#### 输入的文件名不准确或数据库中没有该文件未得到结果

![image-20220316231058936](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316231058936.png)

#### 非法输入

![image-20220316231334726](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316231334726.png)

#### 百度百科搜索

![image-20220316231415328](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316231415328.png)

### 预览功能

![image-20220316231501809](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316231501809.png)



## 尚为解决的问题

- [ ] 在后端会将清明节识别为TIME

![image-20220316231544833](C:/Users/%E5%86%B0/AppData/Roaming/Typora/typora-user-images/image-20220316231544833.png)

- [ ] 没有使用Bert