from py2neo import Graph, errors
from django.conf import settings


def getGraphInstance():
    try:
        # Warning!!!
        return None

        config = settings.DATABASES.get("neo4j")
        graph = Graph(config.get("HOST"), auth=(config.get("USER"), config.get("PASSWORD")))
        print("Neo4j graph database connected successfully")
        return graph

    except errors.ConnectionUnavailable:
        raise ConnectionError("Neo4j graph database connection failed")
