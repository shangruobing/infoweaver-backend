from redis import Redis, exceptions
from py2neo import Graph, errors
from django.conf import settings


def getGraphInstance():
    try:
        if not settings.ENABLE_NEO4J:
            print("Neo4j Not Enabled")
            return None
        config = settings.DATABASES.get("neo4j")
        graph = Graph(config.get("HOST"), auth=(config.get("USER"), config.get("PASSWORD")))
        print("Neo4j graph database connected successfully")
        return graph

    except errors.ConnectionUnavailable:
        raise ConnectionError("Neo4j graph database connection failed")


def getRedisConnectivity():
    try:
        config = settings.DATABASES.get("redis")
        instance = Redis(host=config.get("HOST"), port=config.get("PORT"), password=config.get("PASSWORD"))
        if instance.ping():
            print("Redis connected successfully")
    except (ConnectionRefusedError, exceptions.ConnectionError):
        print('Redis Not Enabled')
        raise ConnectionError("Redis connection failed")
