from py2neo import Node
from QAS.utils.db_connection import getGraphInstance

graph = getGraphInstance()


def create_node(label, name):
    """
    label:node type
    name:node's name
    """
    node = Node(label, name=name)
    graph.merge(node, label, "name")


def create_relationship(start_node_label, end_node_label, start_node_name,
                        end_node_name, rel_type, rel_name):
    """
    example: 小明训练小华 小明和小华的类型是学生 训练的属性是1000米\n",
    start_node_label = '学生'\n",
    end_node_label = '学生'\n",
    start_node_name = '小明'\n",
    end_node_name = '小华'\n",
    rel_type = '训练'\n",
    rel_name = '1000米'\n",
   """
    query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' merge (p)-[rel:%s{name:'%s'}]->(q)" % (
        start_node_label, end_node_label, start_node_name, end_node_name, rel_type, rel_name)
    try:
        graph.run(query)
    except Exception as e:
        print(e)
