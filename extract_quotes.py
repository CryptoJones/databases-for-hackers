import pymupdf, os, re, json

SRC = "/home/hermes/databases-for-hackers/source_books"

books = {
    "db_foundations": [
        "2013_Book_ConciseGuideToDatabases.pdf",
        "Learning SQL, 2nd Edition.pdf",
    ],
    "sql_relational": [
        "practicalsql.pdf",
        "PostgreSQL Development Essentials.pdf",
    ],
    "nosql": [
        "10gen Top 5 NoSQL Considerations.pdf",
        "MongoDB Cookbook.pdf",
        "Cosmos DB for MongoDB Developers.pdf",
    ],
    "security_injection": [
        "SQL Injection Attacks And Defense.pdf",
        "Alice and Bob Learn Application Security (Tanya Janca) (Z-Library).pdf",
        "OWASP Top 10-2017.pdf",
    ],
    "security_engineering": [
        "Security Engineering-Second Edition.pdf",
        "Secrets And Lies-Digital Security In A Networked World.pdf",
        "The Web Application Hacker'S Handbook-Finding And Exploiting Security Flaws-2 Second Edition.pdf",
        "Threat Modeling-Designing For Security.pdf",
    ],
    "cloud": [
        "AWS Administration-The Definitive Guide.pdf",
        "Fundamentals Of Azure-2nd Edition.pdf",
    ],
    "broader_security": [
        "Cybersecurity Attack and Defense Strategies.pdf",
        "Industrial Cybersecurity.pdf",
    ],
}

search_terms = {
    "db_foundations": ["database", "relational model", "codd", "schema", "ACID", "transaction", "data model", "normalization"],
    "sql_relational": ["SELECT", "JOIN", "index", "normalization", "PostgreSQL", "relational", "query"],
    "nosql": ["NoSQL", "document store", "MongoDB", "scalability", "CAP theorem", "schema-free", "JSON"],
    "security_injection": ["SQL injection", "parameterized", "OWASP", "input validation", "prepared statement", "sanitiz"],
    "security_engineering": ["attack surface", "privilege escalation", "access control", "breach", "authentication", "misconfiguration", "threat"],
    "cloud": ["shared responsibility", "IAM", "managed service", "encryption", "security group", "cloud"],
    "broader_security": ["database", "attack", "vulnerability", "exploit", "credential", "lateral movement", "defense"],
}

output = {}
for cat, filenames in books.items():
    output[cat] = []
    for fn in filenames:
        fp = os.path.join(SRC, fn)
        if not os.path.exists(fp):
            output[cat].append({"book": fn, "error": "NOT FOUND"})
            continue
        try:
            doc = pymupdf.open(fp)
            bn = fn.replace(".pdf", "")
            pc = doc.page_count
            qf = []
            terms = search_terms[cat]
            for pn in range(min(pc, 200)):
                text = doc[pn].get_text()
                if len(text) < 200:
                    continue
                tl = text.lower()
                hits = sum(1 for t in terms if t.lower() in tl)
                if hits >= 2:
                    sents = re.split(r'(?<=[.!?])\s+', text)
                    good = []
                    for s in sents:
                        s = re.sub(r'\s+', ' ', s.strip())
                        if 40 < len(s) < 500 and any(t.lower() in s.lower() for t in terms):
                            good.append(s)
                    if good:
                        qf.append({"page": pn + 1, "quotes": good[:3]})
                if len(qf) >= 10:
                    break
            doc.close()
            output[cat].append({"book": bn, "total_pages": pc, "excerpts": qf[:10]})
        except Exception as e:
            output[cat].append({"book": fn, "error": str(e)})

with open("/home/hermes/databases-for-hackers/book_quotes.json", "w") as f:
    json.dump(output, f, indent=2)

total = 0
for cat, items in output.items():
    print(f"\n=== {cat.upper()} ===")
    for item in items:
        if "error" in item:
            print(f"  {item['book']}: {item['error']}")
        else:
            n = sum(len(q["quotes"]) for q in item.get("excerpts", []))
            total += n
            print(f"  {item['book']}: {n} quotes from {len(item.get('excerpts', []))} pages")
print(f"\n=== TOTAL: {total} usable quotes ===")
