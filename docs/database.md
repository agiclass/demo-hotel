**数据库选择**

1. pinecone

支持tokenizer ids的sparse向量，用于做keyword检索

2. milvus

Feature Roadmap
https://github.com/milvus-io/milvus/discussions/
https://wiki.lfaidata.foundation/display/MIL/Feature+plans

"Hybrid search with BM25 and vector"计划在3.0+版本，即最早明年初release

3. weaviate

支持BM25，但不能与向量检索同时查询，可以搜两次然后交集

