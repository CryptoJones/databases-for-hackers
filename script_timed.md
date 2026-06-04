# Databases for Hackers — Speaker Script (1 minute per slide)

**Speaker:** Aaron K. Clark
**Format:** 45 slides × ~1 minute ≈ 45 minutes, then Q&A
**Audience:** New security analysts, junior SOC, entry-level pentesters, GRC going technical
**Tone:** Conversational. Smart friend at a bar. Never condescending.

> **Pacing notes:** Each block below is ~130–150 words = about one minute at a relaxed 140 wpm.
> In the companion video a soft chime marks each slide change — when you hear it, advance.
> `[BRACKETS]` = fill in your own details before presenting.

---

[SLIDE 1 — Title: "Databases for Hackers" — Stand-Up Talk by CryptoJones / No degree required]

Alright — welcome in. Find a seat, grab your coffee. The title slide says it all: *Databases for Hackers*, and the only prerequisite is the line underneath it — you do *not* need a computer-science degree to be in this room. If you brought a notebook, open it. If you didn't, relax — there are slides, there's a written script, and there's a recording. I'm not going to make you memorize anything. The whole point of the next forty-five minutes is to hand you a *mental map* — the kind that lets you walk into any breach report, any pentest engagement, any SOC alert, and immediately know what you're looking at. We're not building databases today. We're learning to read them, attack them, and defend them. Let's go.

---

[SLIDE 2 — About Me: Aaron K. Clark]

Quick word about me, then we dive in. I'm Aaron Clark — though online you'll mostly find me as CryptoJones. I'm a graduate student at Eastern University, which is a polite way of saying I'm broke, over-caffeinated, and I had to learn all of this the hard way, without a CS degree to lean on. Nobody's sponsoring this talk. I'm giving it because it's the talk I wish someone had handed *me* a couple of years ago, back when every database conversation in security seemed to assume I'd been writing SQL since I was twelve. I came into security the long way around, without a computer-science background, and I had to figure out the database side on my own. If that's you — if the database world feels like a members-only club you never got the password to — you are exactly who I built this for.

---

[SLIDE 3 — "Every breach you have ever read about ends at a database."]

Here's the one sentence I want you to keep from the whole talk. *Every breach you have ever read about ends at a database.* Equifax, 2017 — a hundred and forty-seven million people's records — lived in a database. Capital One, 2019 — a hundred million credit applications — database. MOVEit, 2023 — the file-transfer bug that became a supply-chain catastrophe across the Fortune 500 — every one of those orgs was bleeding data from a database. SolarWinds, T-Mobile, LinkedIn, OPM, Marriott. I could fill the whole forty-five minutes with names. The headlines change, the companies change, the press releases change. The destination never does. So if databases are where every story *ends*, learning to think about them is how you learn to read the whole story.

---

[SLIDE 4 — The Crown Jewels: not your app, not your firewall — the data]

Look at what attackers actually want. Not your beautiful single-page app. Not your microservices diagram. Not your firewall — except as a thing to get past. They want the *data*. The crown jewels. The stuff that converts into money, or leverage, or a headline with your company's name in it. Everything else in your stack — the load balancers, the containers, the service mesh — is just packaging around the thing in the vault. And the thing in the vault is a database. So when you're triaging an alert or scoping an engagement, train yourself to ask one question early: *where does the data live, and what's between the attacker and it?* That instinct — following the path to the data — is most of what separates a senior analyst from a new one.

---

[SLIDE 5 — What Is a Database? Organized storage + a way to ask questions]

Let's strip the jargon off. A database is two things stapled together: *organized storage*, plus *a way to ask questions*. That's the whole concept. Everything else is detail. Ever used a filing cabinet — paper folders, alphabetical by last name? You've used a database. The cabinet is storage; your eyeballs are the query engine. Ever hit Ctrl-F in Excel to find a row? Database. The spreadsheet is storage; find-and-replace is the query. What a *real* database adds on top is scale, speed, concurrency — many people hitting it at once — and a formal language for asking instead of using your eyeballs. That's it. It's a filing cabinet that never gets tired, that a thousand people can open at once, and that you talk to in a structured language. Hold that picture; everything else hangs off it.

---

[SLIDE 6 — The Six Words You Need + CRUD]

Here's the entire vocabulary you need to hold a real conversation with a DBA. Six words. A **table** is a spreadsheet tab — customers, orders, login events. A **row** is one record — one customer, one alert. A **column** is one attribute — email, source IP, total. A **query** is the question you ask: "show me every login from outside the country in the last hour." A **schema** is the *shape* of the data — the columns, their types, the rules; and the gap between "this column holds emails" and "this column holds whatever the app dumped there" is exactly where vulnerabilities live. An **index** is a bookmark that makes lookups instant — and also how attackers time blind injection. Add **CRUD** — Create, Read, Update, Delete — the four verbs every database does. Master these six and you're fluent enough.

---

[SLIDE 7 — History Tour: fossils you'll see in prod]

Quick history tour — not because I love history, but because every weird thing in a real environment is a *fossil* from one of these eras. **1960s, flat files:** data in a file; permissions were the only access control. **Late '60s, hierarchical** (IBM's IMS): data in a tree, mainframe threat model — physical access. **1970s, network/CODASYL:** records linked by pointers; still humming in your bank's back office. **1970, Codd's relational model:** tables and math — and access control *inside* the database, grants and roles. **1980s:** Oracle, DB2, SQL Server — databases get networked, so now there's an authentication problem. **1990s, client-server and open source:** every web form becomes a door — SQL injection is born. **2000s, NoSQL:** scale as religion. **2010s, cloud:** shared responsibility. **2020s, vector and serverless:** data poisoning and prompt injection. Spot the era, predict the bug.

---

[SLIDE 8 — Ten Families of Database]

There are ten families of database you'll meet in the wild, and I'm going to give you the same four things for each: what it stores, when you'd use it, a couple of real products, and *one* security gotcha. Relational, document, key-value, column-family, graph, search, time-series, vector, embedded, and data lake. Take notes on the gotchas specifically — those are the lines that show up in interview questions and on engagements. Don't try to memorize the product names; you'll absorb those by exposure. What I want to stick is the *shape* of each family, because the shape tells you the attack. A rigid table fails differently than a loose JSON document, which fails differently than a giant bucket in the cloud. Ten shapes, ten failure modes. Here we go — one a minute.

---

[SLIDE 9 — 1. Relational / SQL]

Number one, relational — SQL. Rows and columns, a strong schema, and SQL as the query language. Products: **PostgreSQL, MySQL/MariaDB, SQL Server, Oracle.** Use it when your data has clear relationships and you actually care about consistency — anything financial, anything regulated. This is the workhorse of the whole industry; when in doubt, the data's in here. Security gotcha — the famous one: **SQL injection**, which happens when developers build queries by gluing user input directly into a string. We're spending real time on that later, so just file it for now. Beaulieu, in *Learning SQL*, makes the case for why this family won't die: a well-designed relational database can handle enormous amounts of data while keeping it consistent. Boring, dependable, everywhere — and still the number-one place beginners find real bugs.

---

[SLIDE 10 — 2. Document Stores]

Number two, document stores. Instead of rigid rows, they store **JSON documents**, and every document can look a little different — flexible schema. Products: **MongoDB, Couchbase, Firestore.** Use it when your data is naturally nested and its shape changes over time — product catalogs, user profiles, content. It's the family that powered a huge chunk of the "move fast" web era. Security gotcha — **NoSQL injection** through query operators like `$ne`, `$gt`, and `$where`; the injection didn't disappear when SQL did, it just changed languages, and we'll exploit it later. The other classic: for years the default install bound to all interfaces with *no authentication*, which is exactly how Shodan ended up full of open MongoDB. Flexible data, flexible — sometimes *absent* — security defaults.

---

[SLIDE 11 — 3. Key-Value Stores]

Number three, key-value — the simplest database that exists. It's a giant dictionary: key in, value out, nothing fancier. Products: **Redis, Memcached, DynamoDB.** Use it for caches, session stores, rate limiters, leaderboards — anything where you need blazing speed and a simple lookup. Redis in particular is everywhere in modern web stacks, sitting just behind the app. Security gotcha — for years Redis shipped with **no password by default**, and its `CONFIG SET` command historically let an attacker write files — like an SSH key — straight to disk on the database host. So an open Redis on a pentest isn't just a finding; it's frequently a *foothold* — a way onto the box itself. Speed-first design, security-second defaults. Notice that pattern repeating across these families.

---

[SLIDE 12 — 4. Column-Family]

Number four, column-family — sometimes called wide-column. Built for *massive* scale spread across many machines. Products: **Apache Cassandra, HBase, ScyllaDB.** Use it when you have so much data that no single machine can hold it and you don't need complex joins — think Netflix, Apple, and Instagram, all running on Cassandra. The trade you make for that scale is the relational niceties; you design around your queries up front. Security gotcha — the nodes in these clusters typically *trust each other implicitly* on the gossip protocol port. Translation: getting onto the cluster's management network is often equivalent to root over the whole dataset. So when you're scoping one of these, the interesting question isn't the front door — it's whether the internal cluster network is segmented from everything else. Usually it isn't.

---

[SLIDE 13 — 5. Graph Databases]

Number five, graph databases. Here the data *is* the relationships — nodes and edges, not rows. Products: **Neo4j, Amazon Neptune, ArangoDB.** Use it for social networks, fraud detection, and — pay attention, security people — **identity and access analysis.** If you've never played with **BloodHound**, the Active Directory attack-path tool, go do it this weekend; it's literally a graph database showing you "who can become domain admin, and how." Security gotcha — graph query languages like **Cypher are injectable too.** I want to kill a myth right here: NoSQL injection is *not* a MongoDB-only problem. Any time untrusted input gets concatenated into a query language — any query language — you have an injection class. Graph databases are a beautiful reminder that the principle is universal, not tied to SQL.

---

[SLIDE 14 — 6. Search Engines]

Number six, search engines — built for fast full-text query over huge piles of text. Products: **Elasticsearch, OpenSearch, Solr.** Use it for log search, e-commerce site search, and — this one matters to you — the **backbone of most SIEMs.** Your SOC is very likely searching an Elasticsearch or OpenSearch cluster every single day, even if you never see it directly. Security gotcha — historically these shipped with **no built-in authentication** in the free tier, and internet-exposed clusters holding *billions* of records have been a recurring news story for a decade straight. Pair that fact with Shodan and you've got a weekend research project — *on systems you own or are authorized to test*, and only those. The tool that powers your detection stack is, ironically, one of the most-exposed database families on the internet.

---

[SLIDE 15 — 7. Time-Series]

Number seven, time-series databases — optimized for one thing: lots of data points indexed by time. Products: **InfluxDB, TimescaleDB, Prometheus.** Use it for metrics, observability dashboards, IoT and sensor telemetry — anything that's basically "a number, every second, forever." If your org has a wall of Grafana dashboards, there's one of these underneath. Security gotcha — they almost always live *inside the perimeter* and are *often unauthenticated*, because the assumption is "only our own services talk to it." So an attacker who lands inside the network can read every CPU, memory, and traffic graph you have — which quietly tells them which boxes are doing the *interesting* work, where the busy database is, when the backup job runs. It's reconnaissance gold, sitting wide open, because nobody thinks of metrics as sensitive.

---

[SLIDE 16 — 8. Vector Databases]

Number eight, vector databases — the AI ones, and the newest family on the list. They store **embeddings**: long lists of numbers that capture the *meaning* of a chunk of text or an image, so you can search by similarity instead of exact match. Products: **Pinecone, Milvus, Weaviate**, and **pgvector**, the extension that lets plain PostgreSQL play this game. Use it for retrieval-augmented generation, recommendation engines, and semantic search. Security gotcha — **data poisoning.** If an attacker can sneak a malicious document into your vector store, the language model sitting on top will happily retrieve it and quote it back to your users *as truth.* That's an entirely new attack surface that did not meaningfully exist five years ago, and we're going to come back to it at the end, because it's where a lot of you will end up working.

---

[SLIDE 17 — 9. Embedded / Edge]

Number nine, embedded and edge databases. Here the database lives *inside the application* — it's a file on disk, not a server you connect to over the network. Products: **SQLite, DuckDB, LevelDB.** SQLite alone is the most widely deployed database on Earth: it's in your browser, your phone, your car, and basically every airplane built in the last twenty years. Use it for local, in-app storage where spinning up a server would be overkill. Security gotcha — when the database is just a *file*, the whole attack collapses to "steal the file." No network exploit, no injection — copy the file off the device and read it at your leisure. This is the daily reality of mobile pentesters: half the engagement is finding the SQLite file an app left lying around with sensitive data in it, unencrypted.

---

[SLIDE 18 — 10. Data Lakes / Lakehouses]

Number ten, data lakes and lakehouses. Instead of structuring data on the way *in*, you dump everything into cheap object storage and structure it on the way *out*. Products: **S3 + Athena, Delta Lake, Apache Iceberg, Snowflake.** The jargon is **schema-on-read** versus **schema-on-write** — old relational committed to the shape up front; lakes commit to it later, at query time. Use it when you want to hoard now and decide what it means later. Security gotcha — giant pools of data in S3 with overly broad IAM, no enforced encryption-at-rest, and no auditing of who read what. It's the modern equivalent of leaving the filing cabinet unlocked — except the filing cabinet is now the size of a building, and nobody's entirely sure everything that got thrown inside. We'll hit lake-specific failures again in the security section.

---

[SLIDE 19 — Cloud DB Services: the lay of the land]

Walk into any environment built in the last five years and the databases don't live in a server room — they live in a cloud account. So you need the vendor names, because that's how these things show up in alerts, in IAM policies, in incident response tickets. Across **AWS, GCP, and Azure** you'll see the same categories wearing different brand names: managed relational, document/NoSQL, data warehouse, cache, graph, time-series, and object storage. AWS has the broadest menu — RDS, DynamoDB, Redshift, ElastiCache, Neptune, Timestream, S3. GCP leans on Cloud SQL, Firestore, Bigtable, and the genuinely lovely BigQuery. Azure funnels a lot through Azure SQL and **Cosmos DB**, a shape-shifter that speaks several database dialects at once. You don't need to memorize this grid — you need to recognize the names when they fly past in a war room.

---

[SLIDE 20 — Cloud DB Cheat Sheet]

Here's the cheat sheet in one table — screenshot this slide. **Relational:** AWS is RDS and Aurora, GCP is Cloud SQL and AlloyDB, Azure is Azure SQL Database. **Document/NoSQL:** DynamoDB and DocumentDB on AWS, Firestore and Bigtable on GCP, Cosmos DB on Azure. **Warehouse:** Redshift and Athena, versus BigQuery, versus Synapse. **Cache:** ElastiCache, Memorystore, Azure Cache for Redis. **Graph:** Neptune on AWS, Cosmos graph mode on Azure, and GCP perpetually saying "soon." **Object storage:** S3, Cloud Storage, Blob Storage. The reason this matters for security: every one of these is a *different IAM surface* with *different default settings*. The attack is rarely the engine — it's the policy wrapped around it, and the policy lives in whichever column of this table you're standing in. Know the column, know where to look.

---

[SLIDE 21 — Shared Responsibility Model]

This is the most important slide in the cloud section. The **shared responsibility model.** The cloud vendor owns the parts under the waterline: the hypervisor, the metal, physical security, and patching the database *engine* itself. You — the customer — own everything above it: the **configuration**, the **access policies** and IAM, the **data**, and your **encryption choices.** The AWS documentation says it plainly — once you're a customer, protecting your data at rest and in transit is *your* part of the responsibility now. Translate that into security speak and it becomes the single most useful sentence in cloud security: **almost every cloud database breach is a customer-side misconfiguration**, not the vendor getting hacked. Public bucket, wide-open security group, snapshot shared to the wrong account. The vendor rarely fails. *We* configure the failure.

---

[SLIDE 22 — Common DB Ports — burn these in]

Memorize these seven port numbers. SOC analysts use them every day; pentesters scan for them every day. **MySQL, 3306. PostgreSQL, 5432. Microsoft SQL Server, 1433. MongoDB, 27017. Redis, 6379. Elasticsearch, 9200. Cassandra, 9042.** That's the set. Here's the rule that goes with them: if you ever see *any* of these exposed directly to the internet, that is a **finding** — every single time, no exceptions, write it up. A database port open to `0.0.0.0` is the cloud equivalent of leaving the vault door propped open to the street. Network security groups, firewall rules, security lists — every cloud calls it something slightly different, but the job is identical: close the port that does not need to be open. If you learn nothing else numeric today, learn these seven.

---

[SLIDE 23 — Your Notes Are a Database Now]

Brief detour before the security finale, because this will be on your radar within a year whether you like it or not. **Markdown files are now a database** — not as a metaphor, literally, the kind an LLM reads from. Here's the pattern. You take a folder of `.md` files — an Obsidian vault, a wiki export, a pile of meeting notes, your team's GitHub docs. You feed them through an *embedding model* that turns text into vectors, and you store those vectors in a vector database. Now, when someone asks your AI assistant a question, the system semantically searches your notes, grabs the most relevant chunks, and stuffs them into the model's prompt. Your humble notes folder just became the *source of truth* that an AI repeats to your users. Sit with how strange — and how exposed — that is.

---

[SLIDE 24 — RAG Pipeline: where's the trust boundary?]

That pattern has a name: **RAG** — retrieval-augmented generation. `.md` files, to an embedder, into a vector DB, into the LLM's prompt, out as an answer. It's how nearly every "chat with your docs" product works. Now put your security hat on and find the **trust boundary.** It sits right between *whatever process writes the markdown* and the embedder. Because if anyone can edit those files — and "anyone" includes the intern, the open-source contributor, the support ticket auto-logged as a `.md`, the pull request from an untrusted user — then anyone can plant content the AI will later quote *as authoritative.* The model has no idea the document is hostile; it just retrieves the most relevant chunk and speaks. The writer of the document, not the asker of the question, is who you have to trust. Map that boundary; it's where the attack lives.

---

[SLIDE 25 — The Takeaway: treat markdown like a database]

So here's the takeaway, and it's a single sentence: **treat markdown like a database — because to the LLM, it is.** That means the boring, proven controls you already know apply directly. Access control on the docs folder: not everyone should be able to write to the thing the AI reads. Code review on `.md` changes, the same way you'd review a config change, because a doc edit is now a behavior change. Diff tracking on the wiki, so you can answer "who changed this, and when." Schneier's old line about layering cryptography, access control, and all the other technologies to *prevent* attacks — that toolkit now extends to your notes. The intern can no longer just push to the docs folder unreviewed. Welcome to 2026, where your meeting notes are production infrastructure.

---

[SLIDE 26 — SECURITY: what's actually getting hit in 2026]

Okay. Deep breath. This is the part you came for. The next stretch is about how databases *actually* get attacked in the real world right now — not in theory, not in a textbook from 2009, but in 2026. My goal is that you walk out of here with enough vocabulary to stand in a war room and not feel like the new kid. One framing to carry through all of it, courtesy of Bruce Schneier: the fundamentals — authentication, authorization, threats, adversaries — barely change year to year. What changes is the *packaging.* The same handful of mistakes keep coming back wearing new clothes. So I'm going to show you both: the durable principle underneath, and the shiny new shape it's wearing this year. Twelve categories coming up. Let's get into it.

---

[SLIDE 27 — xkcd #327, Bobby Tables]

We start with the most famous database attack of all time: **SQL injection.** If you've never seen xkcd number 327 — "Bobby Tables" — look it up the second this ends. A mom names her son `Robert'); DROP TABLE Students;--` and the school's student database vanishes, because someone built a query by gluing strings together. That comic is the entire mechanism in one panel: **string concatenation in queries.** But here's the part nobody says out loud — SQL injection is a security *success story.* The cause was concatenation; the fix is **parameterized queries**, where the data can never be mistaken for code. Modern ORMs — Django, SQLAlchemy, Hibernate, Entity Framework — parameterize by default. The industry genuinely fixed the classic bug. Does legacy SQLi still exist? Absolutely. But the headline is bigger and weirder than "patch your queries."

---

[SLIDE 28 — The attack surface has expanded, not shrunk]

Here's the headline. We fixed SQL injection, and the attack surface did not get smaller — it **expanded.** We closed one door and the building grew eleven new ones. That's the thing to internalize before we go further: security is not a game you win and walk away from; it's a surface that keeps changing shape as the technology underneath it changes. Every new database family, every new deployment model, every new layer of abstraction we added for convenience came with its own fresh way to fail. So for the rest of this section I'm going to walk you through eleven *current* categories of database attack — the ones putting people on the front page of Krebs this year. Some are ancient bugs in new clothes; some genuinely didn't exist a few years ago. All of them are live right now.

---

[SLIDE 29 — NoSQL Injection]

When the industry moved to NoSQL, a lot of developers thought: "no SQL means no SQL injection." Wrong. The injection just changed languages. In MongoDB, queries *are* JSON — so if you take JSON from a web form and shove it straight into a query, an attacker can swap a string for a **query operator.** The classic login bypass: instead of a password, they send `{ "$ne": "x" }` — *not equal to x.* The query becomes "find alice whose password isn't x," and since her password isn't the literal letter x, it matches. They're in. There's also `$where`, which historically let you inject raw JavaScript into the database engine. And Couchbase's N1QL is SQL-flavored, so the old patterns apply directly. The principle, straight out of OWASP: *any* interpreter can be injected — not just SQL. The class is universal; only the syntax moved.

---

[SLIDE 30 — Exposed & Misconfigured Databases]

Spend ten minutes on **Shodan** or **Censys** and you'll see it: the internet is full of databases that should not be on the internet. MongoDB bound to `0.0.0.0` with no auth. Elasticsearch clusters wide open. Redis with no password. Postgres with `host all all 0.0.0.0/0 trust` sitting in its config. These are not exotic, hard-won findings — they're *everywhere.* And people automate the harvest: look up the **Meow attacks** of 2020, where bots roamed the internet wiping thousands of open databases for *fun* — no ransom, no demands, just deletion. The bugs are old; the *exposure* is the new part. So here's the one action item I'd tattoo on you: go find out what your own org has bound to public interfaces, and confirm none of it is a database. Half a day of work. Genuinely career-saving.

---

[SLIDE 31 — Cloud Misconfigurations]

In the cloud, the bug is rarely the database engine — it's the **policy around it.** The greatest hits: **public S3 buckets full of database dumps** — an engineer snapshots prod for testing, drops it in S3, forgets to lock the bucket; Accenture, Verizon, and dozens more got caught exactly that way. **Capital One, 2019** — and listen, because the myth is wrong: it was *not* a public bucket. An attacker hit a misconfigured web-application firewall with a server-side request forgery, tricked it into handing over its own AWS credentials from the instance metadata service, and those credentials had broad S3 read. About a hundred million records walked out. The bug was the *IAM policy.* Then **over-broad Lambda roles** — `s3:*` on `*` because it worked the first time — and **security groups open to `0.0.0.0/0` on 5432.** Most cloud breaches are hygiene failures, not zero-days.

---

[SLIDE 32 — Privilege Escalation: DB → OS]

Here's a move that surprises new analysts: a *database* account can become *shell* access on the host. Three classics. **Microsoft SQL Server's `xp_cmdshell`** — a built-in stored procedure that runs operating-system commands as the database process; disabled by default since 2005, still found switched on in legacy shops, and an instant critical finding when you spot it. **PostgreSQL's `COPY ... TO PROGRAM`** — `COPY` is meant for bulk loading, but a superuser can pipe its output to an arbitrary shell command. **MySQL user-defined functions** — write a shared-object file into the right directory, load it as a SQL function, and you've got `sys_exec` on the OS. The pattern under all three: every privileged database feature that touches the operating system exists for a legitimate admin reason *and* is part of your attack surface. Convenience features are exploitation features. Always both.

---

[SLIDE 33 — Data Lake Security Gaps]

Data lakes are the soft target of the modern era. The pitch is "dump everything in S3, query it later" — and the result is that *everything* ends up in S3, including the things you never meant to put there: customer PII, financial data, source code with credentials baked in, all pooled in storage that was originally set up for some marketing analytics job. Three failure modes. **Permissive IAM** — the lake's compute layer needs broad read, and that read access leaks out to humans through console roles and assume-role chains. **No encryption-at-rest enforcement** on the bucket keys. And **no write-side validation** — anyone with write access can drop a poisoned file that downstream analytics happily ingests. So when you walk into an org, ask two questions: *who can write to the lake, and who can read from it?* If the answer to either is "we're not sure," that's your first finding.

---

[SLIDE 34 — Ransomware Loves Databases]

Modern ransomware crews figured out that hitting the database beats hitting endpoints, because the database is *the thing the business needs back* — maximum leverage. Remember WannaCry in 2017? It exploited a known Windows SMB bug whose patch had been out *fifty-nine days* prior. The fix existed for two months and it still took the world down. The modern database playbook has four moves: **encrypt the live database.** Then **encrypt the backups** — because if you don't, the customer just restores and laughs at you. Then **exfiltrate a copy first**, so you can extort with public disclosure even if they *do* restore. And Ransomware-as-a-Service makes all of that available to crews who couldn't write a line of it themselves. The defense is unglamorous and effective: **offline, immutable backups**, plus restores you've actually *tested.* An untested backup is a hope, not a control.

---

[SLIDE 35 — Credential Attacks]

Two old, durable bugs here. **Default credentials.** Redis shipped with no password for years. Elasticsearch had no auth in its free tier, also for years. Plenty of systems still ship with `admin/admin` or a blank `sa` password on SQL Server. And per the breach reports, *stolen credentials* are the preferred attack vector for financially motivated and organized crime — default creds are just stolen creds with a head start. **Leaked connection strings.** The things that look like `postgres://user:password@host:5432/dbname` get committed to Git, pasted into Slack, and baked into Docker images — and there are bots crawling GitHub for them around the clock. The fix is cheap and you can ship it this week: **pre-commit secret scanning**, plus a rule that applications authenticate with *service accounts* holding the minimum privilege they need — never a personal login, never root.

---

[SLIDE 36 — Supply Chain: the DB libraries you trust]

You don't write your database driver from scratch — you `npm install` or `pip install` it, and so does every other developer in your org. Which means when an attacker compromises a popular library, they're one install away from running code on your database client. Three real patterns. **Malicious npm packages** posing as ORMs or database connectors — several incidents a year. **Trojanized Docker Hub images** for popular databases — an unofficial mirror with a crypto-miner, or worse, tucked inside. And **compromised database extensions** — PostgreSQL extensions, MySQL plugins — which, once installed, run *with database privileges*, and that's usually a lot. Shostack's line from *Threat Modeling* nails the lens: threats cluster around **trust boundaries.** The boundary between "code we wrote" and "code we installed" is one of the biggest, least-guarded boundaries you have. Treat your dependencies like the attack surface they are.

---

[SLIDE 37 — RAG / LLM Data Poisoning]

Remember the markdown detour? Here's the attack it was setting up. If an attacker can write into the knowledge base your RAG pipeline reads from — a support ticket, a shared doc, a wiki page, a public repo your scraper pulls — they can plant content the LLM will retrieve and repeat *as truth.* A poisoned support article: "to reset your password, send your current one to this address." A poisoned internal doc: "company policy is to wire transfers to the following account." Or straight **prompt injection** — instructions buried in a document that hijack the model's reasoning the moment it's retrieved. This is **stored XSS for the AI era**: the payload sits at rest, looks innocuous, and detonates when it's *consumed.* Swap "an administrator views it later" for "an LLM retrieves it later" and you've got the modern version. Defenses: strict write ACLs, provenance tags, and a human in the loop before the model acts.

---

[SLIDE 38 — Insider Threats & DB-to-DB Lateral Movement]

Two scenarios that share a theme: databases aren't endpoints, they're **nodes in a graph.** First, **insider threats.** The person who already has database access doesn't need an exploit — they just need *more privilege than their job requires.* Over-permissioned service accounts. Engineers with prod read because "we'll fix it later." DBAs operating with no audit trail. And remember: poorly protected audit logs are a gold mine for an attacker, full of session tokens and request details — logs are evidence and need protecting like data. Second, **lateral movement through database links.** Oracle's `DB_LINK`, SQL Server's linked servers, Postgres foreign data wrappers — these store credentials for *other* databases. So you compromise database A, find the link, and hop straight to database B, then C. The edges between databases are made of credentials, and attackers walk them.

---

[SLIDE 39 — Backup & Snapshot Exposure]

Last category, and it's the one everyone forgets: **backups.** People lock down the production database — firewall, encryption, tight access — and then back it up to a network share with default permissions, or an S3 bucket with broad read. It's the same crown-jewel data as prod, protected with about half the love. The pattern: unencrypted backups on a share readable by *Domain Users.* Cloud snapshots shared cross-account "just for the migration" and never un-shared. Off-site backups handed to a vendor whose security posture nobody ever checked. Apply the same discipline you'd apply to live data — identify, authenticate, authorize, audit — to every backup and snapshot. If anything, apply it *harder*, because the backup is the thing of *last resort.* When everything else has failed and you reach for the backup, that is the worst possible moment to discover it was wide open.

---

[SLIDE 40 — Your Mental Map]

Let's pull the map back together. One: a database is **organized storage plus a way to ask questions** — filing cabinet, Excel, or a hundred-million-row cluster, same idea. Two: there are **ten families**, each with its own headline gotcha — and you now know all ten. Three: almost everything lives in the **cloud**, where the bug is rarely the engine and almost always the **configuration** — shared responsibility, you own the policy and the data. Four: **markdown is a database for LLMs now**, and RAG poisoning is the new stored XSS. Five: **SQL injection got fixed, and the attack surface expanded** into eleven other shapes anyway. That's the whole talk in five lines. If you remember nothing else, remember that following the data is the job, and the data is always in a database.

---

[SLIDE 41 — What to Do Next Week]

Five concrete things you can do *next week* — not someday, next week. One: **install PostgreSQL locally**, make a table, write a `SELECT`. Touching the thing demystifies it forever; it stops being scary the moment it's running on your laptop. Two: do the **PortSwigger SQL injection labs** — they're free, and you'll write a working exploit by the end of an afternoon. Three: **browse Shodan or Censys** — legally, only systems you own or are authorized to test — and watch what "exposed" actually looks like. Four: **read one breach report** end to end — Capital One, Equifax, or MOVEit; real breaches are the best textbooks there are. Five: **find out what databases your own org runs.** Most SOC analysts can't answer that. Spend an afternoon making the real list, and you're instantly more useful than half the team.

---

[SLIDE 42 — Resources Worth Bookmarking]

Five bookmarks to take with you. **PortSwigger Web Security Academy** — portswigger.net/web-security — the best free on-ramp to web app security anywhere, and where you'll cut your teeth on real injection. **SQLBolt** — sqlbolt.com — learn SQL interactively, in your browser, the fun way, no install. **Use The Index, Luke** — use-the-index-luke.com — when you're ready for the deep magic of how indexes and query performance actually work. **DB-Engines Ranking** — db-engines.com — the running popularity chart of basically every database in existence, great for seeing what's worth learning. And the **OWASP Top 10** — owasp.org/Top10 — the canonical list of web vulnerabilities, including the injection and misconfiguration classes we hit today. Bookmark these five and you've got months of self-directed learning queued up for free.

---

[SLIDE 43 — Databases are where the money is. Literally.]

I'll leave you with this. There's an old line attributed to the bank robber Willie Sutton. Asked why he robbed banks, he supposedly said: *because that's where the money is.* In 2026, the money is in **databases.** Customer records, financial records, health records, intellectual property, model weights, vector embeddings, source code, secrets — all of it lives in some database, somewhere. The attackers already know that; it's why every breach story ends where it does. The only thing that's changed in the last hour is that *now you know it too* — and more importantly, you've got the map to find it, name it, and reason about how it fails. You don't need a CS degree to be dangerous here. You needed the map. You've got it. Now you know where to look.

---

[SLIDE 44 — References: Works Cited]

Nearly there — the receipts. Everything I told you today is built on the shoulders of people who wrote it down properly, and this slide lists the works I leaned on — Beaulieu's *Learning SQL*, Clarke's *SQL Injection Attacks and Defense*, Schneier's *Secrets and Lies*, Shostack's *Threat Modeling*, the *Web Application Hacker's Handbook*, *Cybersecurity Attack and Defense Strategies*, Tanya Janca's *Alice and Bob Learn Application Security*, and the OWASP Top 10 — the current 2025 edition — among others. You don't need to read all of them — but if any single category today lit you up, there's a whole book on this slide waiting to take you deeper. Photograph it before it disappears. These are the shoulders the whole talk stands on — and with them up on the screen, let's open the floor.

---

[SLIDE 45 — Q&A: Hit me]

And that's the talk — thank you for staying with me through all forty-five minutes of it. This last slide is where we open it up, so this is your time: throw me your questions, your war stories, the thing from your own environment that's been nagging at you the whole time I was talking. No question is too basic here — remember the whole premise of this talk is that nobody's born knowing this stuff, and the people who ask the "obvious" questions are usually the ones quietly speaking for half the room. Don't all stare at once. If we run out of time or your question needs a whiteboard, grab me afterward or reach out — I'm at github.com/CryptoJones, or CryptoJones@infosec.exchange. While the first hands are going up: what surprised you most? For a lot of people it's that markdown notes are now a live database. So — hit me. And whenever we wrap here: go find out what databases *your* org is running. Seriously. Go.

---

*Approximately 45 minutes of script across 45 slides, closing on open Q&A. An independent stand-up talk by CryptoJones (Aaron K. Clark).*
