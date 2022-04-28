import os
from tqdm import tqdm
import spacy
from ..utils.graph_database import create_node, create_relationship

nlp = spacy.load("zh_core_web_lg")
cfg = {"segmenter": "jieba"}
nlp.from_config({"nlp": {"tokenizer": cfg}})


class Neo4jDataLoader:
    def __init__(self, filePath):
        self.filePath = filePath

    def execute_load(self):
        fileList = os.listdir(self.filePath)

        textList = []

        for file in fileList:
            with open(os.path.join(self.filePath, file), encoding='UTF-8') as f:
                textList.append(f.readlines())

        # result_text:对textList的内容进行处理\n",
        result_text = []
        for i in textList:
            result_text.append(''.join(i))

        # titleList:存放所有文件名（去除后缀）\n",
        titleList = []
        for i in fileList:
            titleList.append(i[:-4])

        # dataset: 存放最终数据 格式: 标题,内容\n",
        dataset = []
        for i in range(len(titleList)):
            dataset.append((titleList[i], result_text[i]))

        # 数据集正式导入数据库
        for i in tqdm(iterable=dataset, desc="txt => neo4j loading"):
            try:
                self.load_data(title=i[0], text=i[1])
            except Exception:
                continue
        return "Success Loading!"

    def load_data(self, title, text):
        """单篇文章导入图数据库"""
        doc = nlp(text)
        entity = set()
        location = []
        person = []
        unit = []
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PERSON', 'WORK_OF_ART', 'LAW', 'LANGUAGE']:
                entity.add((ent.text, ent.label_))
            if ent.label_ == 'ORG':
                unit.append((ent.text, 'org'))
            if ent.label_ == 'LOC':
                location.append((ent.text, 'location'))
            if ent.label_ == 'GPE':  # 国家
                location.append((ent.text, 'location'))
            if ent.label_ == 'PERSON':
                person.append((ent.text, 'person'))

        objects = []
        times = []
        objects.extend(entity)

        # 关系抽取
        for token in doc:
            if token.dep_ == 'compound:nn' and token.tag_ == 'NT' and token.head.tag_ == 'NT':
                times.append((token.text + token.head.text, 'time'))

        # 创建Node Title 目前是一篇文章的root
        create_node(label='Title', name=title)

        # 创建Node Content 存放一篇文章的所有内容
        content_name = 'Content' + title
        create_node(label='Content', name=content_name)

        # 创建Node File 存放一篇文章的原始文件
        create_node(label='File', name=text)

        # 创建Node Time 存放一篇文章的所有时间
        time_name = 'Time' + title
        create_node(label='Time', name=time_name)

        # 创建Node Location 存放一篇文章的所有地理位置
        loc_name = 'Loc' + title
        create_node(label='Location', name=loc_name)

        # 创建Node Person 存放一篇文章的所有人
        person_name = 'Person' + title
        create_node(label='Person', name=person_name)

        # 创建Node Unit 存放一篇文章的所有组织ORG
        org_name = 'ORG' + title
        create_node(label='ORG', name=org_name)

        # 创建relation Title has_content Content
        create_relationship('Title', 'Content', title,
                            content_name, 'Content', 'has_content')

        # 创建relation Title has_file File
        create_relationship('Title', 'File', title,
                            text, 'File', 'has_file')

        # 创建relation Title has_time Time
        create_relationship('Title', 'Time', title,
                            time_name, 'Time', 'has_time')

        # 将所有子时间结点与Time（时间root）创建关系
        for i in times:
            create_node(label=i[1], name=i[0])
            create_relationship('Time', i[1], time_name,
                                i[0], 'time', 'has_Time')

        # 创建relation Title has_person Person
        create_relationship('Title', 'Person', title,
                            person_name, 'Person', 'has_person')

        # 将所有子结点与Person（root）创建关系
        for i in person:
            create_node(label=i[1], name=i[0])
            create_relationship('Person', i[1], person_name,
                                i[0], 'person', 'has_person')

        create_relationship('Title', 'Location', title,
                            loc_name, 'Location', 'has_location')

        # 将所有子结点与Location（root）创建关系
        for i in location:
            create_node(label=i[1], name=i[0])
            create_relationship('Location', i[1], loc_name,
                                i[0], 'location', 'has_location')

        create_relationship('Title', 'ORG', title,
                            org_name, 'ORG', 'has_org')

        # 将所有子结点与ORG（root）创建关系
        for i in unit:
            create_node(label=i[1], name=i[0])
            create_relationship('ORG', i[1], org_name,
                                i[0], 'organization', 'has_organization')
