from services.chroma_client import add_documents, query_docs

docs = [
    "Unauthorized database access can cause data breaches",
    "Implement MFA to improve security",
    "Regular patching reduces vulnerabilities"
]

add_documents(docs)

result = query_docs("database security")

print(result)