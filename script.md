# Databases for Hackers
## A Ronin 48 Stand-Up Talk — Speaker Script

**Speaker:** Aaron K. Clark
**Duration:** 45 minutes of material + 5 minutes Q&A
**Audience:** New security analysts, junior SOC, entry-level pentesters, GRC folks going technical
**Tone:** Conversational. Smart friend at a bar. Never condescending.

---

## Section 1: Opening — Why Hackers Care About Databases
*(target: ~3 minutes)*

[SLIDE 1 — Title card: "Databases for Hackers" / A Ronin 48 Stand-Up Talk / "No CS degree required"]

[SLIDE 2 — Name card: Aaron K. Clark / Ronin 48]

Alright, welcome in. Grab your coffee. If you've got a notebook, open it. If you don't, that's fine — there are slides, there's a script, and there's a recording. I'm not going to make you memorize anything.

Here is the only sentence you have to remember from the next forty-five minutes.

[SLIDE 3 — Single huge line of text: **"Every breach you have ever read about ends at a database."**]

Every breach you have ever read about ends at a database.

Equifax in 2017 — one hundred and forty-seven million people's personal records — that data lived in a database. Capital One in 2019 — a hundred million credit applications — database. MOVEit in 2023 — the file-transfer software that turned into a supply-chain catastrophe across what felt like the entire Fortune 500 — every one of those organizations was bleeding data from a database. T-Mobile, LinkedIn, the OPM breach, the Marriott breach — and SolarWinds too, though that one's the outlier: a software supply-chain compromise more than a straight database heist. I could keep going for the whole forty-five minutes. The names change, the headlines change, the press releases change. The destination is always the same.

[SLIDE 4 — Stylized image: a vault with rows of filing cabinets behind it]

Attackers don't care about your beautiful single-page app. They don't care about your microservices diagram. They don't really care about your firewall, except as something to get past. They care about the data. The crown jewels. The thing that converts into money or leverage or headlines. And the data lives in a database.

So here's my pitch for the next forty-five minutes. I'm going to give you a *mental map* of the database world — the kind of map that lets you walk into any breach report, any pentest engagement, any SOC alert, and immediately know what you're looking at. You do not need a computer science degree to follow along. You do not need to know how a B-tree works. We're not building one. We're learning to read them, attack them, defend them, and reason about them. As Crowther puts it in *Concise Guide to Databases* — *"a glance at the past does much to inform future thinking, and this book serves to prepare the foundations of a mature approach to using database technologies in the 21st century."* That's our energy today. Mature approach. Foundations. — *Concise Guide to Databases*, p.7.

A quick disclaimer before we dive in: this is **Ronin 48**, and Ronin 48 is in the business of taking people without a traditional CS background and getting them ready to do real security work. So if you've ever felt like the database conversation in the security industry assumes you've been writing SQL since you were twelve — that ends today.

[TRANSITION — pause, sip water, shift posture. Drop into "explain mode."]

---

## Section 2: What Is a Database, Really?
*(target: ~4 minutes)*

[SLIDE 5 — Header: "What Is a Database?" / Bullet: organized storage + a way to ask questions]

Let's strip the jargon off this. A database is two things stapled together. Organized storage. Plus a way to ask questions.

That's it. That's the whole concept. Everything else is detail.

If you've ever used a filing cabinet — paper files, color-coded folders, alphabetical by last name — congratulations, you've used a database. The cabinet is the storage. Your eyeballs and fingers are the query engine. If you've ever opened Excel and used Ctrl+F to find a row, congratulations, you've used a database. The spreadsheet is the storage. Find-and-replace is the query.

What a real database gives you on top of those is *scale*, *speed*, *concurrency* — more than one person hitting it at once — and a *formal language* for asking questions instead of using your eyeballs. That's it. It's a filing cabinet that doesn't get tired, that several people can use at once, and that you talk to in a structured language.

[SLIDE 6 — Vocabulary block, big font:
**Table** — like a spreadsheet tab
**Row** — one record, one customer, one event
**Column** — one attribute of that record
**Query** — the question you're asking
**Schema** — the shape of your data
**Index** — the bookmark that makes lookups fast
**CRUD** — Create, Read, Update, Delete]

Let me give you the vocab you actually need. There are six words. Memorize these and you can hold a real conversation with a DBA.

A **table** is a spreadsheet tab. Customers. Orders. Login events. Alerts.

A **row** is one record. One customer. One order. One alert.

A **column** is one attribute of that record. Email address. Order total. Source IP.

A **query** is the question you ask. "Show me every login from outside the United States in the last hour." That's a query.

A **schema** is the shape of the data — the columns, their types, the rules. A schema is the difference between "this column holds email addresses" and "this column holds whatever the application happened to dump in there." Spoiler — the second one is where vulnerabilities live.

An **index** is a bookmark. If you've got a hundred million rows and you want to find one by email address, an index makes that nearly instant instead of taking forever. Indexes are also a security topic, because indexes are how attackers tell whether their probes are working — timing attacks, blind SQL injection, all of it.

And **CRUD** — Create, Read, Update, Delete — those are the four things any database lets you do. Every alert you ever investigate, every query an attacker runs, every action your application takes — it's some flavor of one of those four verbs.

Now, here's the thing that the textbook will not tell you. Databases live on a spectrum. On one end, you have rigid, *structured* data — every row looks the same, every column has a type, the schema is enforced. Think relational. On the other end, you have *unstructured* data — text, blobs, PDFs, log files where every line might have a different shape. And in between you have everything else. JSON documents that are sort of structured. Time-series points that are wildly structured but really repetitive. The point is — when you walk into an environment, the first question is not "is there a database here." There's always a database. The question is "where does this org live on the structured-to-unstructured spectrum?" That tells you what attacks apply.

As Alan Beaulieu writes in *Learning SQL* — *"SQL is the language for generating, manipulating, and retrieving data from a relational database… One of the reasons for the popularity of relational databases is that properly designed relational databases can handle huge amounts of data."* — *Learning SQL, 2nd Edition*, p.11. That's the foundation. We're going to build out from there.

[TRANSITION — "now let's take the historical tour, because the history is the *why* of every weird thing you'll see in a real environment."]

---

## Section 3: The History Tour — 1960s to Now
*(target: ~4 minutes)*

[SLIDE 7 — Timeline graphic: 1960s flat files → 1970s hierarchical → late-70s network → 1980s relational → 1990s client-server → 2000s NoSQL → 2010s cloud/NewSQL → 2020s vector/serverless]

Quick history tour. I am not doing this because I love history. I am doing this because every weird thing you will see in a real production environment is a fossil from one of these eras. So when you see something strange, you'll be able to say *"oh, that's a 1990s thing"* or *"that's a NoSQL hangover from 2010"* — and that is a real superpower.

**1960s — flat files.** Data was just files on a tape or a disk. If you wanted to find a customer, you read the whole file. Slow. No concurrency. *Security commentary*: filesystem permissions were the only access control. If you got on the box, you got the data.

**Late 1960s — hierarchical databases**, like IBM's IMS. Data in a tree. Great for things that are naturally tree-shaped, like a bill of materials. Terrible if you wanted to ask a question the tree wasn't built for. *Security commentary*: still mainframe-era. The threat model was "physical access to the data center."

**1970s — network databases**, the CODASYL model. Records linked to other records by pointers. Slightly more flexible than hierarchical. Wildly painful to maintain. As Beaulieu observes in *Learning SQL* — *"Both hierarchical and network database systems are alive and well today, although generally in the mainframe world."* — *Learning SQL, 2nd Edition*, p.20. They never died. They're still humming away in your bank's back office. Promise.

**1970 — the moment.** Edgar Codd at IBM publishes *"A Relational Model of Data for Large Shared Data Banks."* Codd basically says — stop with the pointers, stop with the trees, just use tables and let the math sort it out. *Learning SQL* puts it nicely: *"Codd of IBM's research laboratory published a paper titled 'A Relational Model of Data for Large Shared Data Banks' that proposed that data be represented as sets of tables."* — p.20. From that paper you get Oracle, you get SQL, you get the entire industry. *Security commentary*: relational databases bring the concept of *access control inside the database*. Grants. Roles. The notion that "you can connect, but you cannot read this table." A huge step.

**1980s — Oracle, DB2, Sybase, eventually Microsoft SQL Server.** As *practicalsql* tells us — *"In 1979, a precursor to the database company Oracle (then called Relational Software) became the first to use the language in a commercial product."* — *practicalsql*, p.26. *Security commentary*: this is also the decade where databases get networked, and the moment a database gets networked, you have an authentication problem.

**1990s — client-server, open source.** MySQL. PostgreSQL. The database stops being a thing that lives in a special room and starts being a thing every web app spins up. *Security commentary*: this is when **SQL injection** becomes a thing — because suddenly every random web form is a front end into the database.

**2000s — NoSQL.** MongoDB, Redis, Cassandra, the whole alphabet. The web was eating everything, scale was the new religion. The 10gen paper *Top 5 NoSQL Considerations* puts it cleanly — *"When compared to relational databases, many NoSQL systems share several key characteristics including a more flexible data model, higher scalability, and superior performance. But most of these NoSQL databases also discard the very foundation that has made relational databases so useful for generations of applications — expressive query language, secondary indexes and strong consistency."* — *10gen Top 5 NoSQL Considerations*, p.4. Note that "discarded the foundation" line. Hold onto it. We will come back to it in the security section, because *what got discarded* turns out to include some of the security mechanisms.

**2010s — cloud, NewSQL, distributed everything.** Spanner. Aurora. CockroachDB. *Security commentary*: now the database is somebody else's problem. Shared responsibility model. You still own the data; AWS owns the metal.

**2020s — vector databases for AI, serverless, SQLite-everywhere.** The latest wave. *Security commentary*: brand-new categories of attack — data poisoning, prompt injection through stored documents — and we'll close the talk on those.

[TRANSITION — "Okay, history tour over. Let's meet the family."]

---

## Section 4: The Big Families
*(target: ~7 minutes)*

[SLIDE 8 — Ten icons in a grid: Relational, Document, Key-Value, Column-Family, Graph, Search, Time-Series, Vector, Embedded, Data Lake]

There are ten families of database you will run into in the wild. I'm going to give you the same four things for each one — what it stores, when to use it, two or three products, and one security gotcha. Take notes on the gotchas — those are the ones that show up in interview questions and on engagements.

[SLIDE 9 — **1. Relational / SQL**]

**Number one — relational, SQL.** Rows and columns. Strong schema. SQL as the query language. Products — **PostgreSQL, MySQL/MariaDB, Microsoft SQL Server, Oracle**. Use it when your data has clear relationships and you care about consistency — anything financial, anything regulated. Security gotcha — **SQL injection** when developers concatenate user input into queries. We're devoting fifteen minutes to that later. *PostgreSQL Development Essentials* puts the value plainly: *"PostgreSQL is an advanced SQL database server, available on a wide range of platforms."* — p.18. It's the workhorse.

[SLIDE 10 — **2. Document stores**]

**Number two — document stores.** Instead of rows, they store **JSON documents**. Schema is flexible — every document can look different. Products — **MongoDB, Couchbase, Firestore**. Use it when your data is naturally nested and the shape changes over time. The MongoDB Cookbook calls it out: *"MongoDB is a document-oriented, leading NoSQL database, which offers linear scalability, thus making it a good contender for high-volume, high-performance systems."* — *MongoDB Cookbook*, p.14. Security gotcha — **NoSQL injection via query operators** like `$ne`, `$gt`, `$where`. We'll see the exploit later. Default install used to bind to `0.0.0.0` with no auth — that's where Shodan got fun.

[SLIDE 11 — **3. Key-value stores**]

**Number three — key-value.** The simplest possible database. A giant dictionary. Key in, value out. Products — **Redis, Memcached, DynamoDB**. Use it for caches, session stores, rate limiters, leaderboards. Blazing fast. Security gotcha — **default no-auth on Redis**, and the `CONFIG SET` command historically let attackers write SSH keys to disk on the database host. If you ever get a Redis on a pentest and it's open — that's not a finding, that's a foothold.

[SLIDE 12 — **4. Column-family stores**]

**Number four — column-family**, sometimes called wide-column. Designed for massive scale across many machines. Products — **Apache Cassandra, HBase, ScyllaDB**. Use it when you have so much data that one machine can't hold it and you don't need complex joins. Netflix, Apple, and Uber run on Cassandra. Security gotcha — clusters often trust each other implicitly on the gossip protocol port; getting on the management network is sometimes equivalent to root.

[SLIDE 13 — **5. Graph databases**]

**Number five — graph.** Nodes and edges. The data *is* the relationships. Products — **Neo4j, Amazon Neptune, ArangoDB**. Use it for social networks, fraud detection, **identity and access analysis**. If you're in security and you have not played with BloodHound, which is built on Neo4j, please go do that this weekend. Security gotcha — query languages like Cypher are injectable too. NoSQL injection is not just MongoDB.

[SLIDE 14 — **6. Search engines**]

**Number six — search.** Built for full-text query. Products — **Elasticsearch, OpenSearch, Solr**. Use it for log search, your SIEM, e-commerce site search. Your SOC is almost certainly built on one of these. Security gotcha — Elasticsearch, before recent versions, had **no built-in auth in the free tier**. Internet-exposed Elastic clusters with billions of records have been *the* recurring news story for ten years. Pair that with Shodan and you have a research project for the weekend — *only on systems you own*, please.

[SLIDE 15 — **7. Time-series databases**]

**Number seven — time series.** Optimized for "lots of data points, indexed by time." Products — **InfluxDB, TimescaleDB, Prometheus**. Use it for metrics, observability, IoT telemetry. Security gotcha — these are usually inside the perimeter and often unauthenticated, which means an attacker who lands inside the network can read every CPU graph you have, which tells them which boxes are doing the interesting work.

[SLIDE 16 — **8. Vector databases**]

**Number eight — vector databases.** These are the AI ones. They store **embeddings** — long lists of numbers that represent the *meaning* of a chunk of text or an image. Products — **Pinecone, Milvus, Weaviate**, and **pgvector**, which is the extension that lets PostgreSQL play this game. Use it for retrieval-augmented generation, recommendation engines, semantic search. Security gotcha — *data poisoning*. If an attacker can sneak a malicious document into your vector store, the LLM on top of it will happily quote that document back to your users as truth. Whole new attack surface. We'll come back to it.

[SLIDE 17 — **9. Embedded / Edge**]

**Number nine — embedded and edge databases.** The database lives **inside the application**, in a file, not on a server. Products — **SQLite, DuckDB, LevelDB**. SQLite is the most-deployed database on Earth. It's in your browser, your phone, and even in aircraft avionics — Airbus confirms it's in the flight software of the A350. Security gotcha — when the database is just a file, the attack is *steal the file*. Mobile pentesters live in this world.

[SLIDE 18 — **10. Data Lakes / Lakehouses**]

**Number ten — data lakes and lakehouses.** Instead of structuring data on the way in, you dump everything into cheap object storage and structure it on the way out. Products — **AWS S3 with Athena, Delta Lake, Apache Iceberg, Databricks, Snowflake**. The technical term is **schema-on-read** versus **schema-on-write**. Old-school relational was schema-on-write — you commit to the shape up front. Lakes are schema-on-read — you commit to the shape later, when you query. Security gotcha — **giant pools of data sitting in S3 with overly broad IAM**, no encryption-at-rest enforcement, no auditing of who read what. It's the modern equivalent of leaving the filing cabinet unlocked, except the filing cabinet is now the size of a building.

[TRANSITION — "Most of these now live in the cloud. Let's look at where."]

---

## Section 5: Cloud DB Services — AWS, GCP, Azure
*(target: ~5 minutes)*

[SLIDE 19 — Three columns labeled AWS, GCP, Azure]

If you walk into any environment built in the last five years, the databases probably don't live in a server room. They live in a cloud account. So you need to know the cloud-vendor names for these things, because that's how they'll appear in alerts, in IAM policies, in incident response.

[SLIDE 20 — Side-by-side comparison table]

Here's the cheat sheet.

**Relational managed.** AWS calls it **RDS** — that's the umbrella for managed Postgres, MySQL, SQL Server, Oracle. AWS also has **Aurora**, which is their custom relational engine that's wire-compatible with Postgres and MySQL but faster and pricier. GCP has **Cloud SQL** and **AlloyDB**. Azure calls theirs **Azure SQL Database** and **Azure Database for PostgreSQL/MySQL**.

**Document / NoSQL.** AWS has **DynamoDB** for key-value/document and **DocumentDB** which is their MongoDB-compatible thing. GCP has **Firestore** and **Cloud Bigtable**. Azure has **Cosmos DB**, which is a real shape-shifter — it speaks MongoDB, Cassandra, Gremlin, and table API all at once. As Sharma writes in *Cosmos DB for MongoDB Developers* — *"In the cloud, having a massive compute-capacity PaaS is the most desirable option, as, in this case, one needn't worry about scalability, performance, and availability."* — p.25. That's the pitch. Whether it lives up to it depends on the team.

**Data warehouse.** AWS has **Redshift** and **S3 + Athena** for ad-hoc. GCP has **BigQuery**, which is gorgeous. Azure has **Synapse Analytics**.

**Cache.** AWS has **ElastiCache** for Redis and Memcached. GCP has **Memorystore**. Azure has **Azure Cache for Redis**.

**Graph.** AWS has **Neptune**. Azure has graph mode in **Cosmos DB**. GCP — they keep telling us "soon."

**Time-series.** AWS has **Timestream**. Most everyone else assumes you'll bring your own.

**Object storage / data lake foundation.** AWS **S3**, GCP **Cloud Storage**, Azure **Blob Storage**. These are not databases by themselves, but every modern data lake sits on top of them.

[SLIDE 21 — **Shared Responsibility Model**: cloud-provider owns the platform; you own configuration, data, access]

Now the most important slide in this section — the **shared responsibility model**. The cloud vendor patches the hypervisor, runs the metal, and keeps the database engine itself updated. You — the customer — own the configuration, the access policies, and the data. *AWS Administration: The Definitive Guide* puts it directly: *"as an end user, all you need to worry about from the security point of view is how is your data going to be protected at rest or in transit, whether you are going to use encryption/decryption techniques, and so on; this is your part of the responsibility now."* — *AWS Administration*, p.44. Translate that into security speak: *almost every cloud database breach is a customer-side misconfiguration*, not the cloud vendor getting hacked. Public S3 bucket. Wide-open security group. Snapshot shared to the wrong account. We'll itemize those in the security section.

[SLIDE 22 — **Common DB ports cheat sheet**:
MySQL 3306 • PostgreSQL 5432 • MS SQL 1433 • MongoDB 27017 • Redis 6379 • Elasticsearch 9200 • Cassandra 9042]

And finally — the ports. Burn these into your brain. SOC analysts use them every day, pentesters scan for them every day.

- **MySQL — 3306**
- **PostgreSQL — 5432**
- **Microsoft SQL Server — 1433**
- **MongoDB — 27017**
- **Redis — 6379**
- **Elasticsearch — 9200**
- **Cassandra — 9042**

If you see any of those exposed to the internet in a real environment, that is a finding. Every single time. Note that one down. As *Fundamentals of Azure* reminds us in its chapter on hardening, **Network Security Groups** are the cloud equivalent of "close the port that does not need to be open." — *Fundamentals of Azure*, p.174. Same idea, every cloud.

[TRANSITION — pause. "Now a brief detour into a kind of database that didn't exist five years ago."]

---

## Section 6: Markdown and Obsidian as Knowledge Stores for LLMs
*(target: ~4 minutes)*

[SLIDE 23 — Header: "Your notes are a database now"]

I have to talk about something weird before we get to the security finale, because it's going to be on your radar in the next twelve months whether you like it or not.

**Markdown files are now a database.** Not metaphorically — literally. The kind of database an LLM reads from.

Here's the pattern. You take a folder full of `.md` files. Maybe it's an **Obsidian vault** — Obsidian being a popular note-taking tool that uses linked markdown files and tags and YAML frontmatter. Maybe it's your company's internal wiki exported to markdown. Maybe it's a folder of meeting notes. You feed those files into an **embedding model** — that's the model that turns text into those long lists of numbers we talked about, the vectors. You store the vectors in a **vector database** — Pinecone, pgvector, whatever. Now when somebody asks the LLM a question, the system does a **semantic search** over your markdown, pulls back the most relevant chunks, and stuffs them into the LLM's prompt as context.

That pattern has a name — **RAG**, retrieval-augmented generation. It is how almost every "chat with your docs" product on the market works. And from a database-thinking perspective, it's important to see what it really is — *your markdown notes are now the source of truth that an AI is going to repeat to your users.*

[SLIDE 24 — Diagram: .md files → embedder → vector DB → LLM prompt → answer to user]

Now look at that diagram and put your security hat on. Where is the trust boundary?

The trust boundary is **between whatever process writes the markdown and the embedder.** If anyone can edit those markdown files — and "anyone" includes "the intern", "the open-source contributor", "the customer-support ticket that gets logged as a `.md` file", "the GitHub pull request from an untrusted user that adds a doc" — then anyone can write content that will eventually be quoted as authoritative by your AI assistant.

This is called **RAG data poisoning**. We'll come back to it in the security section. For now, the takeaway is — *if your organization is doing any kind of internal AI assistant, the markdown files feeding it are now infrastructure, and they need to be treated like infrastructure.* Access control. Code review. Diff tracking. The intern can no longer just push to the docs folder.

[SLIDE 25 — Bullet: "Treat markdown like a database. Because to the LLM, it is."]

Treat markdown like a database. Because to the LLM, it is. Schneier put it well in *Secrets and Lies* — *"the goal was to prevent attacks: through cryptography, access control, firewalls, antivirus, and all sorts of other technologies."* — *Secrets and Lies*, p.9. Access control over markdown files is now part of that toolkit. Welcome to 2026.

[TRANSITION — long pause, drink water, change tone. "Now — the part you came for."]

---

## Section 7: THE SECURITY SECTION
*(target: ~15 minutes — this is 33% of the talk)*

[SLIDE 26 — Big header: "SECURITY" / Subtitle: "What's actually getting hit in 2026"]

Okay. Real talk. This is the part you came for. The next fifteen minutes are about how databases actually get attacked in the real world *right now*, in 2026. I want you to come out of this section with a vocabulary that lets you walk into a war room and not feel like the new kid.

Schneier — Bruce Schneier — in *Secrets and Lies* — *"My chapters on cryptography and its limits, on authentication and authorization, and on threats, attacks, and adversaries could largely have been written yesterday."* — *Secrets and Lies*, p.9. The fundamentals don't change. The packaging does. Let me show you both.

### 7.1 — SQL Injection: A Success Story
*(target: about 1 minute on this — don't dwell)*

[SLIDE 27 — Stylized version of xkcd #327 / "Did you really name your son Robert'); DROP TABLE Students;--?" / URL: https://xkcd.com/327/]

Let's start with the most famous database attack of all time. **SQL injection.** If you haven't seen the xkcd **"Bobby Tables"** comic — number 327, the URL is `https://xkcd.com/327/` — go look it up right after this talk. It perfectly captures why SQL injection was such a problem. A mom names her kid `Robert'); DROP TABLE Students;--` and the school's database disappears because someone built a query by gluing strings together.

Here's the thing I want you to hear — **SQL injection is a security success story.** Listen carefully because nobody says this out loud. *Justin Clarke et al.*, in *SQL Injection Attacks and Defense*, lay out the mechanism: *"SQL injection is an attack in which the SQL code is inserted or appended into application/user input parameters that are later passed to a back-end SQL server for parsing and execution. The primary form of SQL injection consists of direct insertion of code into parameters that are concatenated with SQL commands and executed."* — *SQL Injection Attacks and Defense*, p.24. The cause was concatenation. The fix is **parameterized queries**. Same book, p.33 — *"developers can achieve the same result in a much more secure fashion if they use parameterized queries. Parameterized queries are queries that have one or more embedded parameters in the SQL statement."*

The OWASP Top 10 hammered this for years. Tanya Janca, in *Alice and Bob Learn Application Security*, p.88: *"Writing inline SQL creates a potential SQL Injection vulnerability. Only using parameterized queries instead reliably mitigates this vulnerability."* And modern ORMs — Hibernate, Entity Framework, Django ORM, SQLAlchemy — they parameterize by default. So the industry actually fixed the bug.

Does SQLi still happen? Yes. In legacy code, in raw queries, in stored procedures, in edge cases. You should know how to find it and how to test for it. But — and this is the important bit — **the attack surface has not shrunk; it has *expanded* into new shapes.**

[SLIDE 28 — Big text: **"The attack surface has expanded, not shrunk."**]

So for the next thirteen minutes, I'm going to give you eleven categories of *current* database attack. These are the things that are putting people on the front page of *Krebs* in 2026.

### 7.2 — NoSQL Injection

[SLIDE 29 — Header: "NoSQL Injection"]

When the industry moved to NoSQL — MongoDB, Couchbase, Elasticsearch — a lot of developers thought, "great, no SQL means no SQL injection." Wrong. The injection just changed languages.

In MongoDB, queries are JSON. If you take JSON from a web form and shove it directly into a query, an attacker can replace a string with a **query operator**. The classic — your login is checking `{"username": "alice", "password": "hunter2"}`. The attacker submits `{"username": "alice", "password": {"$ne": "x"}}` — *not equal to x*. The query becomes "find the user named alice whose password is not equal to x" — and since alice's password is not equal to x, that returns alice. Boom. Logged in.

There's also `$where`, which historically let you inject JavaScript directly into the database. And **N1QL** in Couchbase is essentially a SQL-flavored query language for documents, which means classic SQL injection patterns *do* apply there. The OWASP Top 10 — in the current 2025 edition — captures the general principle: *"Dynamic queries or non-parameterized calls without context-aware escaping are used directly in the interpreter."* — *OWASP Top 10:2025*, A05:2025 Injection. Doesn't say SQL. Says *interpreter*. That's any query engine. The principle is universal.

### 7.3 — Exposed and Misconfigured Databases

[SLIDE 30 — Screenshot/mock of Shodan results page with port 27017 hits redacted]

If you've ever spent ten minutes on **Shodan** or **Censys**, you know that the internet is full of databases that should not be on the internet. MongoDB instances bound to `0.0.0.0` with no auth. Elasticsearch clusters with no auth. Redis with no auth. Postgres with `host all all 0.0.0.0/0 trust` in the `pg_hba.conf`.

These are not exotic findings. There have been *waves* of compromises where someone scans the internet, finds an open MongoDB, dumps the data, deletes the database, and leaves a ransom note. Look up the **Meow attacks** of 2020 — bots that just wiped open databases for fun. No ransom, no demands, just deletion. Thousands of databases. *Cybersecurity Attack and Defense Strategies*, p.21, makes the broader point: *"While the use of IoT to launch a massive cyber attack is something new, the vulnerabilities in those devices are not."* Same logic for databases — the bugs are old; the exposure pattern is what's new.

If you only take one action item from this whole talk, it's this — **find out what your org has bound to public interfaces and confirm none of it is a database.** Half a day of work, career-saving.

### 7.4 — Cloud Misconfigurations

[SLIDE 31 — Header: "Cloud misconfigs"]

In cloud, the bug is rarely the database itself. It is almost always the **policy around it.**

The greatest hits:

- **Public S3 buckets containing database dumps.** An engineer takes a snapshot for testing, dumps it to S3, forgets to lock the bucket. Years go by. Then one day a researcher indexes it — Accenture, Verizon, and dozens of others got caught exactly this way.
- **Over-permissioned roles reachable from outside.** This is how Capital One actually went down in 2019 — and it was *not* a public bucket. An attacker hit a misconfigured web-application firewall with a server-side request forgery, tricked it into coughing up its own AWS credentials from the instance metadata service, and those credentials had broad S3 read access. About a hundred million records walked out. The bug was the IAM policy, not the bucket.
- **Snapshots shared to the wrong AWS account.** RDS snapshots can be marked public. Sometimes they get marked public by an engineer who's debugging at 2 a.m. and never gets un-marked.
- **Overly permissive IAM.** A Lambda that needs read access to one bucket is given `s3:*` on `*` because that's what worked the first time. Now any code execution in that Lambda is "exfiltrate everything we have."
- **Wide-open security groups.** `0.0.0.0/0` on port 5432.

The AWS book says it best, p.67: *"Get rid of the Root Account, use IAM wherever necessary… Create separate IAM users for your organization, each with their own sets of access and Secret Keys."* — *AWS Administration*, p.67. This is hygiene, not rocket science. Most cloud breaches are *hygiene failures*, not zero-days.

### 7.5 — Privilege Escalation Inside the Database

[SLIDE 32 — Header: "Privilege escalation: database to OS"]

When an attacker gets *any* database account — even a low-privilege one — there are a few classic moves to escalate from "I can run queries" to "I can run shell commands on the host."

- **`xp_cmdshell` on Microsoft SQL Server.** A built-in stored procedure that lets a sufficiently-privileged user run shell commands. Disabled by default since SQL Server 2005. Still found enabled in legacy environments. If you find it, that's a critical finding.
- **`COPY ... TO PROGRAM` in PostgreSQL.** Postgres has a `COPY` command for bulk data loading. If you have superuser privileges, you can pipe `COPY` output to an arbitrary shell command. Database account becomes OS account.
- **MySQL UDFs — User Defined Functions.** Historically, if you could write a shared object file to a specific directory on the database host, you could load it as a SQL function and call it. End result — `sys_exec` on the OS.

Pattern across all three — **the database engine has features that touch the operating system.** Those features exist for legitimate admin reasons. They are also a beautiful attack surface. *Web Application Hacker's Handbook* puts it broadly: *"In terms of attack surface, the session management mechanism is highly dependent on the security of its tokens."* — p.56. Different mechanism, same principle. Every privileged feature is part of the attack surface.

### 7.6 — Data Lake Security Gaps

[SLIDE 33 — Header: "Data lakes — the giant unfenced field"]

Data lakes are the soft target of the modern era. The pitch is "dump everything in S3, query it later." The result is — *everything is in S3*, including the things you didn't mean to put there. Customer PII. Internal financial data. Source code that contains credentials. All sitting in object storage that was originally configured for a marketing analytics use case.

Three categories of failure:

1. **Permissive IAM** — the lake's compute layer often needs broad read access, and that read access leaks to humans through console roles and assume-role chains.
2. **No encryption at rest enforcement** — `aws:SecureTransport` is checked, `bucket-key-enabled` is not.
3. **No data validation on the way in** — anyone with write access can drop a poisoned file that gets ingested into downstream analytics.

If you do nothing else, when you walk into an org, ask "**who can write to the lake?**" and "**who can read from it?**" If the answer to either is "we're not entirely sure," you have your first finding.

### 7.7 — Ransomware Targeting Databases

[SLIDE 34 — Header: "Ransomware loves databases"]

Modern ransomware crews have figured out that hitting the database is more leveraged than hitting endpoints. Why? Because the database is *the thing the business needs back*. *Cybersecurity Attack and Defense Strategies*, p.29: *"In May 2017, the world was shocked by the biggest ransomware attack in history, called Wannacry. This ransomware exploited a known Windows SMBv1 vulnerability that had a patch released in March 2017 (59 days prior to the attack)."* — p.29. Patch was available. Sixty days. Still got everybody.

The modern playbook:

- Encrypt the live database.
- Encrypt the **backups** — because if you only encrypt the live database, the customer just restores.
- Exfil a copy first, so you can also extort with disclosure even if they restore.
- Ransomware-as-a-Service makes this scalable to crews that can't write their own code.

Defensive moves — *offline, immutable* backups. Test restores. Network segmentation so the database host can't reach the backup host with admin creds. Schneier again, *Secrets and Lies*: identification and authentication, then access control, then audit. *Secrets and Lies*, p.164. Same three steps for backups as for the live system.

### 7.8 — Credential Attacks

[SLIDE 35 — Header: "Default creds & leaked connection strings"]

Two flavors here.

**Default credentials.** Redis used to ship with no password. Elasticsearch shipped with no auth in the free tier for years. MongoDB historically did not require auth on `localhost`. Many embedded systems still ship with `admin/admin` or `sa/<blank>` for SQL Server. From *Cybersecurity Attack and Defense Strategies*, p.24: *"the report states that stolen credentials is the preferred attack vector for financial motivation or organized crime."* — p.24. Default credentials are stolen credentials with a head start.

**Leaked connection strings.** Connection strings — the things that look like `postgres://user:password@host:5432/dbname` — get committed to Git. They get pasted into Slack. They get baked into Docker images. There are continuous scrapers crawling GitHub for these. If your team is not running pre-commit hooks for secret detection, that's something you can fix this week.

Tanya Janca in *Alice and Bob Learn Application Security*, p.88, emphasizes the discipline: *"Your application should also only use a service account to call APIs, parameterized queries, or any other call that requires an account."* Service accounts. Not personal accounts. Not the root account. Service accounts with the minimum privilege needed.

### 7.9 — Supply Chain Attacks on the Database Layer

[SLIDE 36 — Header: "Supply chain — the database libraries you trust"]

You don't write your database driver from scratch. You install it from npm, PyPI, Maven, NuGet, or somewhere similar. So does every developer in your org. So when an attacker compromises a popular library, they're a `pip install` away from execution on your database client. OWASP saw the same shift: in the 2025 Top 10 they promoted software supply chain failures to a category all its own — A03, right up near the top of the list.

Three real-world patterns:

- **Malicious or trojanized npm packages** posing as ORMs or database connectors. Several incidents per year.
- **Compromised Docker images** for popular databases on Docker Hub — an unofficial mirror with a crypto-miner snuck in.
- **Database extension supply chain** — PostgreSQL extensions, MySQL plugins, MongoDB community packages. Once installed, they run with database privileges, which is usually a *lot*.

Adam Shostack in *Threat Modeling: Designing for Security* talks about boundaries: *"Threats tend to cluster around trust boundaries… The trust boundaries delineate the attack surface between principals."* — *Threat Modeling*, p.87. The boundary between "code we wrote" and "code we installed" is one of those boundaries. Treat it like one.

### 7.10 — LLM and RAG Data Poisoning

[SLIDE 37 — Header: "RAG poisoning — the new injection"]

Remember section six? Markdown is a database now. Here's the attack.

If an attacker can write into the knowledge base your RAG pipeline reads from — a customer support ticket, a shared doc, a wiki page, a public GitHub repo your scraper pulls from — they can plant content the LLM will retrieve and quote as truth.

Examples:

- A poisoned support article that says "to reset your password, send your current password to this email address." The LLM repeats it to the next customer who asks about resets.
- A poisoned section of internal docs that says "the company's policy is to wire transfer requests to the following account…"
- **Prompt injection through stored data** — instructions embedded in a document that hijack the LLM's reasoning when retrieved.

This is **stored XSS for the AI era.** The data is at rest, it looks innocuous, it gets activated when consumed. And the timing is tidy: in the 2025 Top 10, OWASP folded cross-site scripting straight into the injection category — *"Injection includes Cross-site Scripting (high frequency/low impact) with more than 30k CVEs."* — *OWASP Top 10:2025*, A05:2025 Injection. The old stored-XSS mechanic still holds — untrusted input stored now, viewed later by another user. Swap "viewed later by another user" for "retrieved later by an LLM" and you have the modern version.

Defenses are still being figured out, but the basics are — **strict access control on writes**, **provenance tagging on retrieved chunks**, and **never let the LLM act on instructions found in retrieved content** without a human in the loop.

### 7.11 — Insider Threats and Lateral Movement Through Databases

[SLIDE 38 — Header: "Insider threats & DB-to-DB lateral movement"]

Two scenarios.

**Insider threats.** The person inside who already has database access doesn't need to exploit anything. They just need *more privilege than their job requires*. Over-permissioned service accounts. Engineers with prod read because "we'll fix it later." DBAs with no audit trail. *Web Application Hacker's Handbook*, p.68: *"poorly protected audit logs can provide a gold mine of information to an attacker, disclosing a host of sensitive information such as session tokens and request parameters."* — *Web Application Hacker's Handbook*, p.68. Logs are evidence; they need to be protected like data.

**Database links and lateral movement.** Many databases let one database talk to another over a configured link — Oracle's `DB_LINK`, SQL Server's linked servers, foreign data wrappers in Postgres. These often store credentials for the remote database. Compromise database A, find the link, jump to database B. *Cybersecurity Attack and Defense Strategies*, p.16: *"Lateral Movement describes how attackers perform lateral movement once they compromise one system."* — p.16. Don't think of databases as endpoints. They're nodes in a graph, and the edges are credentials.

### 7.12 — Backup and Snapshot Exposure

[SLIDE 39 — Header: "Backups: the same data, half the love"]

Last one. Backups. People secure the production database. They lock down the firewall. They turn on encryption. Then they back it up to a network share with default permissions, or to an S3 bucket with broad read.

Backup exposures are the same data as production exposures, with about half the love.

The pattern:

- Unencrypted database backups on a file share readable by Domain Users.
- Cloud snapshots shared cross-account for "convenience" during a migration and never un-shared.
- Off-site backups sent to a third-party vendor whose security posture you have not verified.

Schneier's three-step from *Secrets and Lies* — identify, authenticate, authorize, audit — *Secrets and Lies*, p.164 — applies to backups exactly like it applies to live data. If anything, *more so*, because backups are *the thing of last resort.*

[TRANSITION — pause, breath, slow down. "Okay. Almost done. Let me bring it home."]

---

## Section 8: Wrap-Up — What to Learn Next
*(target: ~3 minutes)*

[SLIDE 40 — Header: "Your mental map"]

Let's recap the mental map.

A database is **organized storage plus a way to ask questions.**

There are **ten families** of database in the wild. Relational, document, key-value, column-family, graph, search, time-series, vector, embedded, and data lake. You know what each one is for and the headline security gotcha for each.

Almost all of them now live in the **cloud**, where the bug is rarely the engine and almost always the **configuration**. Shared responsibility model. You own the policy. AWS owns the metal.

Markdown is a database for LLMs now, and **RAG poisoning** is the new stored XSS.

And the security landscape — SQL injection got *mostly* fixed, but the surface expanded into eleven other categories, from exposed services to ransomware to supply chain to backup exposure.

[SLIDE 41 — Header: "What to do next week"]

Five concrete things you can do next week:

1. **Install PostgreSQL locally.** Free. Five minutes. Spin up a table. Write a `SELECT`. Touching the thing demystifies it forever. *practicalsql*, p.20: *"Building our data infrastructure was a complex, multistep process powered by a PostgreSQL database at its heart."* Start small.
2. **Do the PortSwigger SQL injection labs.** They're free. They are the best on-ramp to web app security on the internet. You will write a working exploit by the end of an afternoon.
3. **Browse Shodan or Censys *legally* — only systems you own or have written authorization for.** Watch a default-config database show up in your local network. Internalize what "exposed" looks like.
4. **Read a breach report.** Cosy up with the Capital One write-up, the Equifax post-mortem, or the MOVEit timeline. *Cybersecurity Attack and Defense Strategies*, p.15: *"learn the attack methods and patterns to recognize abnormal behavior within your organization."* — p.15. Real breaches are the textbooks.
5. **Find out what databases your own org runs.** SOC analysts almost never know. GRC folks often have a list but not a real one. Spend an afternoon making the *real* list. That alone makes you more valuable than half the people on the team.

[SLIDE 42 — Resources list:
PortSwigger Web Security Academy
SQLBolt
Use The Index, Luke
DB-Engines.com
OWASP Top 10]

Resources worth bookmarking — **PortSwigger Web Security Academy** for SQLi labs. **SQLBolt** for learning SQL the fun way. **Use The Index, Luke** for the deep how-databases-work magic. **DB-Engines.com** for the popularity rankings of every database that exists. **OWASP Top 10** for the canonical web vuln list.

[SLIDE 43 — Closing card: **"Databases are where the money is. Literally. Now you know where to look."** / Ronin 48 logo]

I'll leave you with this. *"Why do you rob banks?"* The line attributed to Willie Sutton is *"because that's where the money is."* In 2026, the money is in databases. Customer records, financial records, healthcare records, intellectual property, model weights, vector embeddings, source code, secrets — all of it is in some database, somewhere. Attackers know that. Now you know it too.

Thank you. I'm going to take five minutes of questions. Hit me.

[SLIDE 44 — Q&A]

---

## REFERENCES

Books cited throughout this talk:

- Beaulieu, Alan. *Learning SQL, 2nd Edition.* O'Reilly.
- Clarke, Justin et al. *SQL Injection Attacks and Defense.* Syngress.
- Crowther, Peter. *Concise Guide to Databases.* Springer, 2013.
- DeBarros, Anthony. *Practical SQL.* No Starch Press.
- Diogenes, Yuri and Erdal Ozkaya. *Cybersecurity — Attack and Defense Strategies.* Packt, 2018.
- Janca, Tanya. *Alice and Bob Learn Application Security.* Wiley.
- Mishra, Manpreet Singh and Bikash Chandra Singh. *PostgreSQL Development Essentials.* Packt.
- *MongoDB Cookbook.* Packt.
- *10gen — Top 5 NoSQL Considerations.* 10gen / MongoDB Inc.
- OWASP. *OWASP Top 10:2025.* https://owasp.org/Top10/2025/ (Injection category: https://owasp.org/Top10/2025/A05_2025-Injection/)
- Sharma, Manish. *Cosmos DB for MongoDB Developers.* Apress, 2018.
- Schneier, Bruce. *Secrets and Lies — Digital Security in a Networked World.* Wiley.
- Anderson, Ross. *Security Engineering, Second Edition.* Wiley.
- Stuttard, Dafydd and Marcus Pinto. *The Web Application Hacker's Handbook (2nd Edition).* Wiley.
- Shostack, Adam. *Threat Modeling — Designing for Security.* Wiley.
- *AWS Administration — The Definitive Guide.* Packt.
- *Fundamentals of Azure, 2nd Edition.* Microsoft Press.
- Ackerman, Pascal. *Industrial Cybersecurity.* Packt.

Web references:

- xkcd #327, "Exploits of a Mom" (Bobby Tables): https://xkcd.com/327/
- OWASP Top 10: https://owasp.org/Top10/
- PortSwigger Web Security Academy: https://portswigger.net/web-security
- SQLBolt: https://sqlbolt.com/
- Use The Index, Luke: https://use-the-index-luke.com/
- DB-Engines Ranking: https://db-engines.com/

---

*Talk prepared for **Ronin 48**. Total runtime: approximately 45 minutes of script plus 5 minutes Q&A.*
