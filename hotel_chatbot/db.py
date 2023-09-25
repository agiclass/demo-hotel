import os
from tqdm import tqdm
from weaviate import Client
from weaviate.util import generate_uuid5

def rrf(rankings, k=60):
    scores = dict()
    for ranking in rankings:
        for i, doc in enumerate(ranking):
            doc_id = doc['hotel_id'] if isinstance(doc, dict) else doc
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += 1 / (k + i)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

class Database():
    def __init__(self, ip='localhost', port=8080):
        url = f'http://{ip}:{port}'
        header = {'X-OpenAI-Api-Key':os.getenv('OPENAI_API_KEY')}
        self.client = Client(url=url, additional_headers=header) 

    def create(self, schema):
        self.client.schema.create(schema)

    def delete(self, name):
        self.client.schema.delete_class(name)

    def insert(self, data, name='Hotel', batch=4):
        self.client.batch.configure(batch_size=batch, dynamic=True)
        for item in tqdm(data):
            self.client.batch.add_data_object(
                data_object=item,
                class_name=name,
                uuid=generate_uuid5(item, name)
            )
        self.client.batch.flush()

    def search(self, dsl, output_fields=["hotel_id","name","type","rating","price"], limit=10):
        candidates = []
        ##################### assemble filters ###########################
        filters = []
        keys = ['type','price.range.low','price.range.high','rating.range.low','rating.range.hight']
        if any(key in dsl for key in keys):
            if 'type' in dsl:
                filters.append({"path": ["type"], "operator": "Equal", "valueString": dsl['type']})
            if 'price.range.low' in dsl:
                filters.append({"path": ["price"], "operator": "GreaterThan", "valueNumber": dsl['price.range.low']})
            if 'price.range.high' in dsl:
                filters.append({"path": ["price"], "operator": "LessThan", "valueNumber": dsl['price.range.high']})
            if 'rating.range.low' in dsl:
                filters.append({"path": ["rating"], "operator": "GreaterThan", "valueNumber": dsl['rating.range.low']})
            if 'rating.range.high' in dsl:
                filters.append({"path": ["rating"], "operator": "LessThan", "valueNumber": dsl['rating.range.high']})
        if (len(filters)) == 1:
            filters = filters[0]
        elif len(filters) > 1:
            filters = {"operator":"And","operands":filters}
        ####################### vector search ###############################
        if 'facilities' in dsl:
            query = self.client.query.get("Hotel",output_fields)
            query = query.with_near_text({"concepts": [f"酒店提供:{dsl['facilities']}"]})
            if filters:
                query = query.with_where(filters)
            query = query.with_limit(limit)
            result = query.do()
            # candidates = candidates + [item for item in result['data']['Get']['Hotel'] if item not in candidates]
            candidates = rrf([candidates, result['data']['Get']['Hotel']])
        ####################### keyword search ##############################
        if 'name' in dsl:
            text = ' '.join(re.findall(r'[\dA-Za-z\-]+|\w', dsl['name']))
            query = self.client.query.get("Hotel",output_fields)
            query = query.with_bm25(query=text, properties= ["_name"])
            if filters:
                query = query.with_where(filters)
            query = query.with_limit(limit)
            result = query.do()
            candidates = rrf([candidates, result['data']['Get']['Hotel']])
        if 'address' in dsl:
            text = ' '.join(re.findall(r'[\dA-Za-z\-]+|\w', dsl['address']))
            query = self.client.query.get("Hotel",output_fields)
            query = query.with_bm25(query=text, properties= ["_address"])
            if filters:
                query = query.with_where(filters)
            query = query.with_limit(limit)
            result = query.do()
            candidates = rrf([candidates, result['data']['Get']['Hotel']])
        ######################## condition search ############################
        if not candidates:
            print("--- 字段搜索未命中，仅返回filter过滤结果 ---")
            query = self.client.query.get("Hotel",output_fields)
            if filters:
                query = query.with_where(filters)
            query = query.with_limit(limit)
            result = query.do()
            candidates = result['data']['Get']['Hotel']
        ############################ sort ###################################
        if 'sort.slot' in dsl:
            if dsl['sort.ordering'] == 'descend':
                candidates = sorted(candidates, key=lambda x: x[dsl['sort.slot']], reverse=True)
            else:
                candidates = sorted(candidates, key=lambda x: x[dsl['sort.slot']])
        return candidates
