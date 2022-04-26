class File:
    def __init__(self, file_id):
        self.file_id = file_id
        self.title = None
        self.time = None
        self.org = None
        self.location = None
        self.person = None
        self.abstract = None
        self.content = None

    def __str__(self):
        return f"File:{self.file_id} Abstract{self.abstract}"

    def set_attrs(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def execute_query(self, graph):
        try:
            cypher = f"match (title:Title)-[]-(file:File), (title:Title)-[*2]-(m) where id(title)={self.file_id} return title,file,collect(m)"

            result = graph.run(cypher).data()[0]
            title = result['title']['name']
            content = result["file"]['name']
            collect = result["collect(m)"]

            org = []
            location = []
            person = []
            time = []
            abstract = []

            for i in collect:
                label = str(i.labels)
                if label == ":org":
                    org.append(i['name'])
                if label == ":location":
                    location.append(i['name'])
                if label == ":person":
                    person.append(i['name'])
                if label == ":time":
                    time.append(i['name'])
                if label == ":abstract":
                    abstract.append(i['name'])

            information = {
                "title": title,
                "org": org,
                "location": location,
                "person": person,
                "time": time,
                "abstract": abstract,
                "content": content,
            }
            self.set_attrs(**information)
        except (IndexError, TypeError):
            raise "Index or Type Error"
