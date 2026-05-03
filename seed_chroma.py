from services.chroma_client import add_documents, collection

documents = [
    "Server crashes occur when critical infrastructure fails during peak load. Prevention includes load balancing, auto-scaling, and regular stress testing.",
    "Data breaches happen when unauthorized parties access sensitive information. Key mitigations include encryption, access controls, and regular security audits.",
    "Key person dependency risk occurs when critical knowledge is held by a single employee. Mitigation includes documentation, cross-training, and succession planning.",
    "Payment gateway failures can result in revenue loss and customer dissatisfaction. Redundant payment providers and fallback mechanisms reduce this risk.",
    "Supply chain disruptions can halt operations. Organizations should maintain buffer inventory and develop alternative supplier relationships.",
    "Regulatory compliance risks arise when organizations fail to meet legal requirements. Regular audits, legal reviews, and compliance training are essential.",
    "Cybersecurity threats include phishing, ransomware, and DDoS attacks. Defense strategies include firewalls, employee training, and incident response plans.",
    "Project delivery risks occur due to unclear requirements, scope creep, or resource constraints. Agile methodologies and regular stakeholder communication help mitigate these.",
    "Financial risks include budget overruns and cash flow problems. Regular financial reviews, contingency budgets, and cost monitoring are key controls.",
    "Reputational risks arise from negative publicity or customer dissatisfaction. Crisis communication plans and proactive customer service help manage these risks."
]

# Clear existing documents first
existing = collection.get()
if existing["ids"]:
    collection.delete(ids=existing["ids"])

add_documents(documents)
print(f"Successfully seeded {len(documents)} documents into ChromaDB!")

# Verify
result = collection.get()
print(f"Total documents in ChromaDB: {len(result['ids'])}")