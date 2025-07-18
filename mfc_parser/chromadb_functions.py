import psycopg2
import chromadb
from config import Config
from chromadb.config import Settings
from local_embeddings import CustomOllamaEmbeddings


def get_chroma_client():
    return chromadb.HttpClient(
        host=Config.CHROMADB_HOST,
        port=Config.CHROMADB_PORT,
        settings=Settings(
            is_persistent=True,
            persist_directory=Config.PERSIST_DIRECTORY,
            chroma_client_auth_provider=Config.CHROMA_CLIENT_AUTH_PROVIDER,
            chroma_client_auth_credentials=Config.CHROMA_SERVER_AUTHN_CREDENTIALS,
        )
    )


def get_collection(client=None):
    if client is None:
        client = get_chroma_client()
    return client.get_or_create_collection(
        name=Config.CHROMA_COLLECTION_NAME,
        embedding_function=CustomOllamaEmbeddings()
    )


def update_chromadb():
    client = get_chroma_client()
    collection = get_collection(client)

    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )

    cur = conn.cursor()
    cur.execute("SELECT id, text FROM ticket")
    rows = cur.fetchall()
    ids = [str(row[0]) for row in rows]
    docs = [row[1] for row in rows]

    if ids:
        collection.delete(ids=ids)

    batch_size = 100
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        collection.add(documents=batch_docs, ids=batch_ids)

    cur.close()
    conn.close()
    return {"status": "success", "message": f"Updated {len(docs)} documents"}


def get_situation_from_chromadb_by_id(ticket_id):
    collection = get_collection()
    result = collection.get(ids=[str(ticket_id)])
    if result and result['documents']:
        return {"status": "success", "document": result['documents'][0]}
    return {"status": "not_found"}


def search_chroma_by_text(query_text, top_k=3):
    collection = get_collection()
    result = collection.query(query_texts=[query_text], n_results=top_k)
    return {
        "query": query_text,
        "results": [
            {
                "id": result["ids"][0][i],
                "text": result["documents"][0][i],
                "distance": result["distances"][0][i]
            }
            for i in range(len(result["ids"][0]))
        ]
    }
