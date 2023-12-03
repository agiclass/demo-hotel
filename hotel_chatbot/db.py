import os
import re

from tqdm import tqdm
import weaviate
from weaviate import Client
from weaviate.util import generate_uuid5
from dotenv import load_dotenv
load_dotenv()

weaviate_url = os.environ.get("WEAVIATE_URL", "")
weaviate_key = os.environ.get("WEAVIATE_API_KEY", "")

def rrf(rankings, k=60):
    scores = dict()
    for ranking in rankings:
        for i, doc in enumerate(ranking):
            doc_id = doc["hotel_id"] if isinstance(doc, dict) else doc
            if doc_id not in scores:
                scores[doc_id] = (0, doc)
            scores[doc_id] = (scores[doc_id][0] + 1 / (k + i), doc)
    sorted_scores = sorted(scores.values(), key=lambda x: x[0], reverse=True)
    return [item[1] for item in sorted_scores]


class HotelDB:
    def __init__(self, ip="localhost", port=8080):
        header = {"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}

        url = weaviate_url
        auth_config = weaviate.AuthApiKey(api_key=weaviate_key)

        self.client = weaviate.Client(
            url=url,
            additional_headers=header,
            auth_client_secret=auth_config,
        )

        # try:
        #     url = os.getenv("WEAVIATE_URL")
        #     # url = f"http://{ip}:{port}"
        #     self.client = Client(
        #         url=url, additional_headers=header, timeout_config=(3, 10)
        #     )
        # except Exception:
        #     ip = "weaviate"
        #     url = f"http://{ip}:{port}"
        #     self.client = Client(
        #         url=url, additional_headers=header, timeout_config=(3, 10)
        #     )

    def create(self, name="Hotel"):
        schema = {
            "classes": [
                {
                    "class": name,
                    "description": "hotel meta data",
                    "properties": [
                        {
                            "dataType": ["number"],
                            "description": "id of hotel",
                            "name": "hotel_id",
                        },
                        {
                            "dataType": ["text"],
                            "description": "name of hotel",
                            "name": "_name",  # 分词过用于搜索的
                            "indexSearchable": True,
                            "tokenization": "whitespace",
                            "moduleConfig": {
                                "text2vec-contextionary": {"skip": True}
                            },
                        },
                        {
                            "dataType": ["text"],
                            "description": "type of hotel",
                            "name": "name",
                            "indexSearchable": False,
                            "moduleConfig": {
                                "text2vec-contextionary": {"skip": True}
                            },
                        },
                        {
                            "dataType": ["text"],
                            "description": "type of hotel",
                            "name": "type",
                            "indexSearchable": False,
                            "moduleConfig": {
                                "text2vec-contextionary": {"skip": True}
                            },
                        },
                        {
                            "dataType": ["text"],
                            "description": "address of hotel",
                            "name": "_address",  # 分词过用于搜索的
                            "indexSearchable": True,
                            "tokenization": "whitespace",
                            "moduleConfig": {
                                "text2vec-contextionary": {"skip": True}
                            },
                        },
                        {
                            "dataType": ["text"],
                            "description": "type of hotel",
                            "name": "address",
                            "indexSearchable": False,
                            "moduleConfig": {
                                "text2vec-contextionary": {"skip": True}
                            },
                        },
                        {
                            "dataType": ["text"],
                            "description": "nearby subway",
                            "name": "subway",
                            "indexSearchable": False,
                            "moduleConfig": {
                                "text2vec-contextionary": {"skip": True}
                            },
                        },
                        {
                            "dataType": ["text"],
                            "description": "phone of hotel",
                            "name": "phone",
                            "indexSearchable": False,
                            "moduleConfig": {
                                "text2vec-contextionary": {"skip": True}
                            },
                        },
                        {
                            "dataType": ["number"],
                            "description": "price of hotel",
                            "name": "price",
                        },
                        {
                            "dataType": ["number"],
                            "description": "rating of hotel",
                            "name": "rating",
                        },
                        {
                            "dataType": ["text"],
                            "description": "facilities provided",
                            "name": "facilities",
                            "indexSearchable": True,
                            "moduleConfig": {
                                "text2vec-contextionary": {"skip": False}
                            },
                        },
                    ],
                    "vectorizer": "text2vec-openai",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "vectorizeClassName": False,
                            "model": "ada",
                            "modelVersion": "002",
                            "type": "text",
                        },
                    },
                }
            ]
        }
        self.client.schema.create(schema)
        # 单class创建也可用client.schema.create_class(schema)

    def delete(self, name="Hotel"):
        self.client.schema.delete_class(name)

    def insert(self, data, name="Hotel", batch=4):
        self.client.batch.configure(batch_size=batch, dynamic=True)
        for item in tqdm(data):
            self.client.batch.add_data_object(
                data_object=item,
                class_name=name,
                uuid=generate_uuid5(item, name),
            )
        self.client.batch.flush()

    def search(
        self,
        dsl,
        name="Hotel",
        output_fields=["hotel_id", "name", "type", "rating", "price"],
        limit=10,
    ):
        candidates = []
        if not dsl:
            return []
        if "hotel_id" not in output_fields:  # rrf排序中使用hotel_id
            output_fields.append("hotel_id")
        # ===================== assemble filters ========================= #
        filters = []
        keys = [
            "type",
            "price.range.low",
            "price.range.high",
            "rating.range.low",
            "rating.range.hight",
        ]
        if any(key in dsl for key in keys):
            if "type" in dsl:
                filters.append(
                    {
                        "path": ["type"],
                        "operator": "Equal",
                        "valueString": dsl["type"],
                    }
                )
            if "price.range.low" in dsl:
                filters.append(
                    {
                        "path": ["price"],
                        "operator": "GreaterThan",
                        "valueNumber": dsl["price.range.low"],
                    }
                )
            if "price.range.high" in dsl:
                filters.append(
                    {
                        "path": ["price"],
                        "operator": "LessThan",
                        "valueNumber": dsl["price.range.high"],
                    }
                )
            if "rating.range.low" in dsl:
                filters.append(
                    {
                        "path": ["rating"],
                        "operator": "GreaterThan",
                        "valueNumber": dsl["rating.range.low"],
                    }
                )
            if "rating.range.high" in dsl:
                filters.append(
                    {
                        "path": ["rating"],
                        "operator": "LessThan",
                        "valueNumber": dsl["rating.range.high"],
                    }
                )
            # 补丁，过滤掉未给价格的-1值
            filters.append(
                {
                    "path": ["price"],
                    "operator": "GreaterThan",
                    "valueNumber": 0,
                }
            )
        if (len(filters)) == 1:
            filters = filters[0]
        elif len(filters) > 1:
            filters = {"operator": "And", "operands": filters}
        # ===================== vector search ============================= #
        if "facilities" in dsl:
            query = self.client.query.get(name, output_fields)
            query = query.with_near_text(
                {"concepts": [f'酒店提供:{dsl["facilities"]}']}
            )
            if filters:
                query = query.with_where(filters)
            query = query.with_limit(limit)
            result = query.do()
            candidates = rrf([candidates, result["data"]["Get"][name]])
        # ===================== keyword search ============================ #
        if "name" in dsl:
            text = " ".join(re.findall(r"[\dA-Za-z\-]+|\w", dsl["name"]))
            query = self.client.query.get(name, output_fields)
            query = query.with_bm25(query=text, properties=["_name"])
            if filters:
                query = query.with_where(filters)
            query = query.with_limit(limit)
            result = query.do()
            candidates = rrf([candidates, result["data"]["Get"][name]])
        if "address" in dsl:
            text = " ".join(re.findall(r"[\dA-Za-z\-]+|\w", dsl["address"]))
            query = self.client.query.get(name, output_fields)
            query = query.with_bm25(query=text, properties=["_address"])
            if filters:
                query = query.with_where(filters)
            query = query.with_limit(limit)
            result = query.do()
            candidates = rrf([candidates, result["data"]["Get"][name]])
        # ====================== condition search ========================== #
        if not candidates:
            query = self.client.query.get(name, output_fields)
            if filters:
                query = query.with_where(filters)
            query = query.with_limit(limit)
            result = query.do()
            candidates = result["data"]["Get"][name]
        # ========================== sort ================================= #
        if "sort.slot" in dsl:
            if dsl["sort.ordering"] == "descend":
                candidates = sorted(
                    candidates, key=lambda x: x[dsl["sort.slot"]], reverse=True
                )
            else:
                candidates = sorted(
                    candidates, key=lambda x: x[dsl["sort.slot"]]
                )
        return candidates
