# Datenbanken für Hacker — Vortragsskript (eine Minute pro Folie)

**Vortragender:** Aaron K. Clark
**Format:** 45 Folien × ~1 Minute ≈ 45 Minuten, danach Fragerunde
**Publikum:** Neue Sicherheitsanalysten, Einsteiger-SOC, angehende Pentester, GRC-Leute im Wechsel ins Technische
**Ton:** Locker. Ein kluger Freund an der Bar. Nie herablassend.

> **Hinweise zum Tempo:** Jeder Block unten hat ~130-150 Wörter = etwa eine Minute bei entspannten 140 Wörtern pro Minute.
> Im begleitenden Video markiert ein leiser Klang jeden Folienwechsel — wenn du ihn hörst, blättere weiter.
> `[KLAMMERN]` = trage vor der Präsentation deine eigenen Angaben ein.

---

[FOLIE 1 — Titel: „Datenbanken für Hacker" — Eigenständiger Vortrag von CryptoJones / Kein Informatikstudium nötig]

Also gut — herzlich willkommen. Sucht euch einen Platz, schnappt euch den Kaffee. Der Titel sagt alles: *Datenbanken für Hacker*, und die einzige Voraussetzung steht in der Zeile darunter — ihr braucht *kein* Informatikstudium, um in diesem Raum zu sein. Wenn ihr ein Notizbuch dabeihabt, schlagt es auf. Wenn nicht, entspannt euch — es gibt Folien, ein geschriebenes Skript und eine Aufzeichnung. Ich lasse euch nichts auswendig lernen. Das ganze Ziel der nächsten fünfundvierzig Minuten ist es, euch eine *mentale Landkarte* zu geben — die Art, mit der ihr in jeden Breach-Bericht, jeden Pentest-Auftrag, jede SOC-Warnung hineingehen und sofort wisst, was ihr vor euch habt. Wir bauen heute keine Datenbanken. Wir lernen, sie zu lesen, anzugreifen und zu verteidigen. Los geht's.

---

[FOLIE 2 — Über mich: Aaron K. Clark]

Kurz zu mir, dann tauchen wir ein. Ich bin Aaron Clark — online findet ihr mich allerdings meistens als CryptoJones. Ich bin Masterstudent an der Eastern University, was eine höfliche Art ist zu sagen, dass ich pleite bin, überkoffeiniert, und dass ich das alles auf die harte Tour lernen musste, ohne ein Informatikstudium als Stütze. Niemand sponsert diesen Vortrag. Ich halte ihn, weil es der Vortrag ist, den ich mir vor ein paar Jahren selbst gewünscht hätte, als jedes Datenbankgespräch in der Sicherheit anzunehmen schien, ich würde seit meinem zwölften Lebensjahr SQL schreiben. Ich kam auf dem langen Weg in die Sicherheit, ohne informatischen Hintergrund, und musste mir die Datenbankseite selbst erarbeiten. Wenn das auf dich zutrifft — wenn die Datenbankwelt sich anfühlt wie ein Privatclub, dessen Passwort dir nie jemand gegeben hat — bist du genau die Person, für die ich das gebaut habe.

---

[FOLIE 3 — „Jeder Breach, von dem du je gelesen hast, endet in einer Datenbank."]

Hier ist der eine Satz, den ihr aus dem ganzen Vortrag behalten sollt. *Jeder Breach, von dem ihr je gelesen habt, endet in einer Datenbank.* Equifax, 2017 — die Daten von hundertsiebenundvierzig Millionen Menschen — lagen in einer Datenbank. Capital One, 2019 — hundert Millionen Kreditanträge — Datenbank. MOVEit, 2023 — der Dateiübertragungsfehler, der zur Lieferketten-Katastrophe über die ganzen Fortune 500 wurde — jede dieser Organisationen verlor Daten aus einer Datenbank. SolarWinds, T-Mobile, LinkedIn, OPM, Marriott. Ich könnte die ganzen fünfundvierzig Minuten allein mit Namen füllen. Die Schlagzeilen ändern sich, die Firmen ändern sich, die Pressemitteilungen ändern sich. Das Ziel ändert sich nie. Wenn Datenbanken also der Ort sind, wo jede Geschichte *endet*, dann ist das Denken über sie zu lernen die Art, wie man die ganze Geschichte lesen lernt.

---

[FOLIE 4 — Die Kronjuwelen: nicht deine App, nicht deine Firewall — die Daten]

Schaut euch an, was Angreifer wirklich wollen. Nicht eure schöne Single-Page-App. Nicht euer Microservices-Diagramm. Nicht eure Firewall — außer als etwas, das es zu überwinden gilt. Sie wollen die *Daten*. Die Kronjuwelen. Das, was sich in Geld, in Druckmittel oder in eine Schlagzeile mit dem Namen eurer Firma verwandelt. Alles andere in eurem Stack — die Lastverteiler, die Container, das Service-Mesh — ist nur die Verpackung um das Ding im Tresor. Und das Ding im Tresor ist eine Datenbank. Wenn ihr also eine Warnung triagiert oder einen Auftrag absteckt, trainiert euch, früh eine Frage zu stellen: *Wo leben die Daten, und was steht zwischen dem Angreifer und ihnen?* Dieser Instinkt — dem Pfad zu den Daten zu folgen — ist fast alles, was einen erfahrenen Analysten von einem neuen unterscheidet.

---

[FOLIE 5 — Was ist eine Datenbank? Organisierte Speicherung + eine Möglichkeit, Fragen zu stellen]

Streifen wir den Fachjargon ab. Eine Datenbank sind zwei zusammengetackerte Dinge: *organisierte Speicherung* plus *eine Möglichkeit, Fragen zu stellen*. Das ist das ganze Konzept. Alles andere ist Detail. Habt ihr je einen Aktenschrank benutzt — Papiermappen, alphabetisch nach Nachname? Dann habt ihr eine Datenbank benutzt. Der Schrank ist die Speicherung; eure Augen sind die Abfrage-Engine. Habt ihr je in Excel Strg-F gedrückt, um eine Zeile zu finden? Datenbank. Die Tabelle ist die Speicherung; Suchen-und-Ersetzen ist die Abfrage. Was eine *echte* Datenbank obendrauf liefert, ist Skalierung, Geschwindigkeit, Nebenläufigkeit — viele Leute greifen gleichzeitig zu — und eine formale Sprache zum Fragen statt der Augen. Das war's. Es ist ein Aktenschrank, der nie müde wird, den tausend Leute gleichzeitig öffnen können und mit dem man in einer strukturierten Sprache spricht. Haltet dieses Bild fest; alles andere hängt daran.

---

[FOLIE 6 — Die sechs Wörter, die ihr braucht + CRUD]

Hier ist das gesamte Vokabular, das ihr braucht, um ein echtes Gespräch mit einem Datenbankadministrator zu führen. Sechs Wörter. Eine **Tabelle** ist ein Tabellenblatt — Kunden, Bestellungen, Login-Ereignisse. Eine **Zeile** ist ein Datensatz — ein Kunde, eine Warnung. Eine **Spalte** ist ein Attribut — E-Mail, Quell-IP, Summe. Eine **Abfrage** ist die Frage, die ihr stellt: „Zeig mir jedes Login von außerhalb des Landes in der letzten Stunde." Ein **Schema** ist die *Form* der Daten — die Spalten, ihre Typen, die Regeln; und die Lücke zwischen „diese Spalte enthält E-Mails" und „diese Spalte enthält, was auch immer die App da reingekippt hat" ist genau dort, wo Schwachstellen leben. Ein **Index** ist ein Lesezeichen, das Suchen sofort macht — und auch, wie Angreifer Blind-Injection timen. Dazu **CRUD** — Create, Read, Update, Delete — die vier Verben, die jede Datenbank ausführt. Beherrscht diese sechs, und ihr seid fließend genug.

---

[FOLIE 7 — Geschichtstour: Fossilien, die ihr in der Produktion seht]

Kurze Geschichtstour — nicht weil ich Geschichte liebe, sondern weil jedes seltsame Ding in einer realen Umgebung ein *Fossil* aus einer dieser Ären ist. **1960er, Flachdateien:** Daten in einer Datei; Berechtigungen waren die einzige Zugriffskontrolle. **Späte 60er, hierarchisch** (IBMs IMS): Daten in einem Baum, Mainframe-Bedrohungsmodell — physischer Zugang. **1970er, Netzwerk/CODASYL:** Datensätze über Zeiger verknüpft; brummt noch im Hinterzimmer eurer Bank. **1970, Codds relationales Modell:** Tabellen und Mathematik — und Zugriffskontrolle *innerhalb* der Datenbank, Rechte und Rollen. **1980er:** Oracle, DB2, SQL Server — Datenbanken werden vernetzt, also gibt es jetzt ein Authentifizierungsproblem. **1990er, Client-Server und Open Source:** Jedes Webformular wird zur Tür — SQL-Injection ist geboren. **2000er, NoSQL:** Skalierung als Religion. **2010er, Cloud:** geteilte Verantwortung. **2020er, Vektor und Serverless:** Datenvergiftung und Prompt-Injection. Erkenne die Ära, sage den Bug voraus.

---

[FOLIE 8 — Zehn Datenbankfamilien]

Es gibt zehn Datenbankfamilien, denen ihr in freier Wildbahn begegnet, und ich gebe euch für jede dieselben vier Dinge: was sie speichert, wann ihr sie nutzt, ein paar reale Produkte und *einen* Sicherheitshaken. Relational, Dokument, Schlüssel-Wert, Spaltenfamilie, Graph, Suche, Zeitreihen, Vektor, eingebettet und Data Lake. Macht euch besonders Notizen zu den Haken — das sind die Zeilen, die in Bewerbungsgesprächen und bei Aufträgen auftauchen. Versucht nicht, die Produktnamen auswendig zu lernen; die saugt ihr durch Erfahrung auf. Was hängenbleiben soll, ist die *Form* jeder Familie, denn die Form sagt euch den Angriff. Eine starre Tabelle versagt anders als ein lockeres JSON-Dokument, das anders versagt als ein riesiger Bucket in der Cloud. Zehn Formen, zehn Versagensarten. Auf geht's — eine pro Minute.

---

[FOLIE 9 — 1. Relational / SQL]

Nummer eins, relational — SQL. Zeilen und Spalten, ein starkes Schema und SQL als Abfragesprache. Produkte: **PostgreSQL, MySQL/MariaDB, SQL Server, Oracle.** Nutzt sie, wenn eure Daten klare Beziehungen haben und euch Konsistenz wirklich wichtig ist — alles Finanzielle, alles Regulierte. Das ist das Arbeitspferd der ganzen Branche; im Zweifel liegen die Daten hier. Sicherheitshaken — der berühmte: **SQL-Injection**, die passiert, wenn Entwickler Abfragen bauen, indem sie Benutzereingaben direkt in eine Zeichenkette kleben. Dem widmen wir später echte Zeit, also legt es vorerst ab. Beaulieu führt in *Learning SQL* aus, warum diese Familie nicht stirbt: Eine gut entworfene relationale Datenbank kann enorme Datenmengen verarbeiten und dabei konsistent halten. Langweilig, verlässlich, überall — und immer noch der Ort Nummer eins, an dem Anfänger echte Bugs finden.

---

[FOLIE 10 — 2. Dokumentenspeicher]

Nummer zwei, Dokumentenspeicher. Statt starrer Zeilen speichern sie **JSON-Dokumente**, und jedes Dokument darf ein bisschen anders aussehen — flexibles Schema. Produkte: **MongoDB, Couchbase, Firestore.** Nutzt sie, wenn eure Daten natürlich verschachtelt sind und ihre Form sich mit der Zeit ändert — Produktkataloge, Benutzerprofile, Inhalte. Es ist die Familie, die einen großen Teil der „schnell-vorwärts"-Web-Ära antrieb. Sicherheitshaken — **NoSQL-Injection** über Abfrageoperatoren wie `$ne`, `$gt` und `$where`; die Injection verschwand nicht, als SQL ging, sie wechselte nur die Sprache, und wir werden sie später ausnutzen. Der andere Klassiker: Jahrelang band die Standardinstallation an alle Schnittstellen *ohne Authentifizierung*, was genau der Grund ist, warum Shodan voller offener MongoDBs wurde. Flexible Daten, flexible — manchmal *fehlende* — Sicherheitsstandards.

---

[FOLIE 11 — 3. Schlüssel-Wert-Speicher]

Nummer drei, Schlüssel-Wert — die einfachste Datenbank, die es gibt. Es ist ein riesiges Wörterbuch: Schlüssel rein, Wert raus, nichts Komplizierteres. Produkte: **Redis, Memcached, DynamoDB.** Nutzt sie für Caches, Sitzungsspeicher, Ratenbegrenzer, Bestenlisten — alles, wo ihr rasende Geschwindigkeit und eine einfache Suche braucht. Redis im Besonderen ist überall in modernen Web-Stacks, direkt hinter der App. Sicherheitshaken — Jahrelang wurde Redis **ohne Passwort standardmäßig** ausgeliefert, und sein `CONFIG SET`-Befehl ließ historisch einen Angreifer Dateien — etwa einen SSH-Schlüssel — direkt auf die Festplatte des Datenbank-Hosts schreiben. Ein offenes Redis bei einem Pentest ist also nicht nur ein Fund; es ist häufig ein *Standbein* — ein Weg auf die Maschine selbst. Geschwindigkeit-zuerst-Design, Sicherheit-danach-Standards. Achtet darauf, wie sich dieses Muster durch diese Familien wiederholt.

---

[FOLIE 12 — 4. Spaltenfamilie]

Nummer vier, Spaltenfamilie — manchmal Wide-Column genannt. Gebaut für *massive* Skalierung, verteilt über viele Maschinen. Produkte: **Apache Cassandra, HBase, ScyllaDB.** Nutzt sie, wenn ihr so viele Daten habt, dass keine einzelne Maschine sie fassen kann, und ihr keine komplexen Joins braucht — denkt an Netflix, Apple und Instagram, alle auf Cassandra. Der Preis für diese Skalierung sind die relationalen Annehmlichkeiten; ihr entwerft vorab um eure Abfragen herum. Sicherheitshaken — die Knoten in diesen Clustern *vertrauen einander typischerweise implizit* auf dem Port des Gossip-Protokolls. Übersetzung: Ins Verwaltungsnetz des Clusters zu kommen, ist oft gleichbedeutend mit Root über den gesamten Datensatz. Wenn ihr also einen davon absteckt, ist die interessante Frage nicht die Vordertür — sondern ob das interne Cluster-Netz vom Rest segmentiert ist. Meistens ist es das nicht.

---

[FOLIE 13 — 5. Graphdatenbanken]

Nummer fünf, Graphdatenbanken. Hier *sind* die Daten die Beziehungen — Knoten und Kanten, keine Zeilen. Produkte: **Neo4j, Amazon Neptune, ArangoDB.** Nutzt sie für soziale Netzwerke, Betrugserkennung und — aufgepasst, Sicherheitsleute — **Identitäts- und Zugriffsanalyse.** Wenn ihr noch nie mit **BloodHound** gespielt habt, dem Active-Directory-Angriffspfad-Tool, macht das dieses Wochenende; es ist buchstäblich eine Graphdatenbank, die euch zeigt: „Wer kann Domänenadministrator werden, und wie." Sicherheitshaken — Graph-Abfragesprachen wie **Cypher sind auch injizierbar.** Ich will hier einen Mythos töten: NoSQL-Injection ist *kein* reines MongoDB-Problem. Immer wenn nicht vertrauenswürdige Eingaben in eine Abfragesprache verkettet werden — irgendeine Abfragesprache — habt ihr eine Injection-Klasse. Graphdatenbanken sind eine schöne Erinnerung daran, dass das Prinzip universell ist, nicht an SQL gebunden.

---

[FOLIE 14 — 6. Suchmaschinen]

Nummer sechs, Suchmaschinen — gebaut für schnelle Volltextabfragen über riesige Texthaufen. Produkte: **Elasticsearch, OpenSearch, Solr.** Nutzt sie für Log-Suche, E-Commerce-Site-Suche und — das geht euch an — das **Rückgrat der meisten SIEMs.** Euer SOC durchsucht sehr wahrscheinlich jeden einzelnen Tag einen Elasticsearch- oder OpenSearch-Cluster, auch wenn ihr ihn nie direkt seht. Sicherheitshaken — historisch wurden sie **ohne eingebaute Authentifizierung** in der kostenlosen Stufe ausgeliefert, und internet-exponierte Cluster mit *Milliarden* von Datensätzen sind seit einem geschlagenen Jahrzehnt eine wiederkehrende Nachricht. Verknüpft diese Tatsache mit Shodan, und ihr habt ein Wochenend-Forschungsprojekt — *auf Systemen, die euch gehören oder die ihr testen dürft*, und nur auf diesen. Das Werkzeug, das euren Erkennungs-Stack antreibt, ist ironischerweise eine der am stärksten exponierten Datenbankfamilien im Internet.

---

[FOLIE 15 — 7. Zeitreihen]

Nummer sieben, Zeitreihendatenbanken — optimiert für eine Sache: jede Menge Datenpunkte, indiziert nach Zeit. Produkte: **InfluxDB, TimescaleDB, Prometheus.** Nutzt sie für Metriken, Observability-Dashboards, IoT- und Sensortelemetrie — alles, was im Grunde „eine Zahl, jede Sekunde, für immer" ist. Wenn eure Organisation eine Wand aus Grafana-Dashboards hat, steckt eine davon darunter. Sicherheitshaken — sie leben fast immer *innerhalb des Perimeters* und sind *oft ohne Authentifizierung*, weil die Annahme lautet „nur unsere eigenen Dienste sprechen mit ihr". Ein Angreifer, der im Netz landet, kann also jede CPU-, Speicher- und Verkehrsgrafik lesen, die ihr habt — was ihm leise verrät, welche Maschinen die *interessante* Arbeit machen, wo die ausgelastete Datenbank steht, wann der Backup-Job läuft. Es ist Gold für die Aufklärung, sperrangelweit offen, weil niemand Metriken für sensibel hält.

---

[FOLIE 16 — 8. Vektordatenbanken]

Nummer acht, Vektordatenbanken — die KI-Datenbanken, und die jüngste Familie auf der Liste. Sie speichern **Embeddings**: lange Zahlenlisten, die die *Bedeutung* eines Textstücks oder eines Bildes erfassen, sodass ihr nach Ähnlichkeit statt nach exakter Übereinstimmung suchen könnt. Produkte: **Pinecone, Milvus, Weaviate** und **pgvector**, die Erweiterung, mit der ein ganz normales PostgreSQL bei diesem Spiel mitmacht. Nutzt sie für Retrieval-Augmented Generation, Empfehlungsmaschinen und semantische Suche. Sicherheitshaken — **Datenvergiftung.** Wenn ein Angreifer ein bösartiges Dokument in euren Vektorspeicher einschleusen kann, wird das darauf sitzende Sprachmodell es bereitwillig abrufen und euren Nutzern *als Wahrheit* zitieren. Das ist eine völlig neue Angriffsfläche, die es vor fünf Jahren kaum gab, und wir kommen am Ende darauf zurück, weil viele von euch genau dort landen werden.

---

[FOLIE 17 — 9. Eingebettet / Edge]

Nummer neun, eingebettete und Edge-Datenbanken. Hier lebt die Datenbank *innerhalb der Anwendung* — sie ist eine Datei auf der Festplatte, kein Server, mit dem ihr euch über das Netz verbindet. Produkte: **SQLite, DuckDB, LevelDB.** SQLite allein ist die am weitesten verbreitete Datenbank der Erde: Sie steckt in eurem Browser, eurem Telefon, eurem Auto und im Grunde in jedem Flugzeug, das in den letzten zwanzig Jahren gebaut wurde. Nutzt sie für lokale In-App-Speicherung, wo das Hochfahren eines Servers übertrieben wäre. Sicherheitshaken — wenn die Datenbank nur eine *Datei* ist, schrumpft der ganze Angriff auf „stiehl die Datei". Kein Netzwerk-Exploit, keine Injection — kopiert die Datei vom Gerät und lest sie in aller Ruhe. Das ist der Alltag von Mobile-Pentestern: Die halbe Mission besteht darin, die SQLite-Datei zu finden, die eine App mit sensiblen Daten herumliegen ließ, unverschlüsselt.

---

[FOLIE 18 — 10. Data Lakes / Lakehouses]

Nummer zehn, Data Lakes und Lakehouses. Statt Daten beim *Hinein*kommen zu strukturieren, kippt ihr alles in billigen Objektspeicher und strukturiert es beim *Hinaus*gehen. Produkte: **S3 + Athena, Delta Lake, Apache Iceberg, Snowflake.** Der Fachjargon lautet **Schema-on-Read** gegen **Schema-on-Write** — das alte Relationale legte sich vorab auf die Form fest; Lakes legen sich später fest, zur Abfragezeit. Nutzt sie, wenn ihr jetzt horten und später entscheiden wollt, was es bedeutet. Sicherheitshaken — riesige Datenbecken in S3 mit zu breitem IAM, ohne erzwungene Verschlüsselung im Ruhezustand und ohne Audit, wer was gelesen hat. Es ist das moderne Äquivalent dazu, den Aktenschrank unverschlossen zu lassen — nur dass der Aktenschrank jetzt die Größe eines Gebäudes hat und niemand ganz sicher ist, was alles hineingeworfen wurde. Wir treffen lake-spezifische Fehler im Sicherheitsabschnitt wieder.

---

[FOLIE 19 — Cloud-Datenbankdienste: das Lagebild]

Geht in eine in den letzten fünf Jahren gebaute Umgebung, und die Datenbanken leben nicht in einem Serverraum — sie leben in einem Cloud-Konto. Ihr braucht also die Anbieternamen, denn so tauchen diese Dinge in Warnungen, in IAM-Richtlinien, in Incident-Response-Tickets auf. Über **AWS, GCP und Azure** seht ihr dieselben Kategorien unter verschiedenen Markennamen: verwaltet relational, Dokument/NoSQL, Data Warehouse, Cache, Graph, Zeitreihen und Objektspeicher. AWS hat die breiteste Auswahl — RDS, DynamoDB, Redshift, ElastiCache, Neptune, Timestream, S3. GCP stützt sich auf Cloud SQL, Firestore, Bigtable und das wirklich reizvolle BigQuery. Azure leitet vieles über Azure SQL und **Cosmos DB**, einen Gestaltwandler, der mehrere Datenbankdialekte zugleich spricht. Ihr müsst dieses Raster nicht auswendig lernen — ihr müsst die Namen erkennen, wenn sie in einem Krisenraum vorbeifliegen.

---

[FOLIE 20 — Cloud-Datenbank-Spickzettel]

Hier ist der Spickzettel in einer Tabelle — macht einen Screenshot dieser Folie. **Relational:** AWS ist RDS und Aurora, GCP ist Cloud SQL und AlloyDB, Azure ist Azure SQL Database. **Dokument/NoSQL:** DynamoDB und DocumentDB bei AWS, Firestore und Bigtable bei GCP, Cosmos DB bei Azure. **Warehouse:** Redshift und Athena gegen BigQuery gegen Synapse. **Cache:** ElastiCache, Memorystore, Azure Cache for Redis. **Graph:** Neptune bei AWS, der Graph-Modus von Cosmos bei Azure, und GCP, das ewig „bald" sagt. **Objektspeicher:** S3, Cloud Storage, Blob Storage. Warum das für die Sicherheit zählt: Jedes davon ist eine *andere IAM-Oberfläche* mit *anderen Standardeinstellungen*. Der Angriff ist selten die Engine — es ist die Richtlinie, die sie umhüllt, und die Richtlinie lebt in der Spalte dieser Tabelle, in der ihr gerade steht. Kennt die Spalte, wisst, wo ihr schauen müsst.

---

[FOLIE 21 — Modell der geteilten Verantwortung]

Das ist die wichtigste Folie im Cloud-Abschnitt. Das **Modell der geteilten Verantwortung.** Der Cloud-Anbieter besitzt die Teile unter der Wasserlinie: den Hypervisor, das Blech, die physische Sicherheit und das Patchen der Datenbank-*Engine* selbst. Ihr — der Kunde — besitzt alles darüber: die **Konfiguration**, die **Zugriffsrichtlinien** und IAM, die **Daten** und eure **Verschlüsselungsentscheidungen.** Die AWS-Dokumentation sagt es unverblümt — sobald ihr Kunde seid, ist der Schutz eurer Daten im Ruhezustand und während der Übertragung jetzt *euer* Teil der Verantwortung. Übersetzt das in Sicherheitssprache, und es wird zum nützlichsten Satz der ganzen Cloud-Sicherheit: **Fast jeder Cloud-Datenbank-Breach ist eine kundenseitige Fehlkonfiguration**, nicht der gehackte Anbieter. Öffentlicher Bucket, sperrangelweit offene Sicherheitsgruppe, ein an das falsche Konto geteilter Snapshot. Der Anbieter versagt selten. *Wir* konfigurieren das Versagen.

---

[FOLIE 22 — Gängige DB-Ports — brennt sie euch ein]

Merkt euch diese sieben Portnummern. SOC-Analysten nutzen sie jeden Tag; Pentester scannen jeden Tag nach ihnen. **MySQL, 3306. PostgreSQL, 5432. Microsoft SQL Server, 1433. MongoDB, 27017. Redis, 6379. Elasticsearch, 9200. Cassandra, 9042.** Das ist die Menge. Und hier die Regel dazu: Wenn ihr je *irgendeinen* davon direkt zum Internet hin exponiert seht, ist das ein **Fund** — jedes einzelne Mal, ohne Ausnahme, schreibt ihn auf. Ein zum Internet hin auf `0.0.0.0` offener Datenbankport ist das Cloud-Äquivalent dazu, die Tresortür zur Straße hin offen stehen zu lassen. Netzwerksicherheitsgruppen, Firewall-Regeln, Sicherheitslisten — jede Cloud nennt es leicht anders, aber die Aufgabe ist identisch: Schließt den Port, der nicht offen sein muss. Wenn ihr heute keine andere Zahl lernt, lernt diese sieben.

---

[FOLIE 23 — Eure Notizen sind jetzt eine Datenbank]

Kurzer Abstecher vor dem Sicherheits-Finale, denn das wird innerhalb eines Jahres auf eurem Radar sein, ob es euch gefällt oder nicht. **Markdown-Dateien sind jetzt eine Datenbank** — nicht als Metapher, buchstäblich, die Art, aus der ein LLM liest. Hier ist das Muster. Ihr nehmt einen Ordner mit `.md`-Dateien — ein Obsidian-Vault, einen Wiki-Export, einen Stapel Besprechungsnotizen, die GitHub-Dokumente eures Teams. Ihr schickt sie durch ein *Embedding-Modell*, das Text in Vektoren verwandelt, und ihr speichert diese Vektoren in einer Vektordatenbank. Wenn nun jemand eurem KI-Assistenten eine Frage stellt, durchsucht das System eure Notizen semantisch, greift sich die relevantesten Stücke und stopft sie in den Prompt des Modells. Euer bescheidener Notizordner ist gerade zur *Quelle der Wahrheit* geworden, die eine KI euren Nutzern nachplappert. Setzt euch einen Moment damit auseinander, wie seltsam — und wie exponiert — das ist.

---

[FOLIE 24 — RAG-Pipeline: Wo ist die Vertrauensgrenze?]

Dieses Muster hat einen Namen: **RAG** — Retrieval-Augmented Generation. `.md`-Dateien, zu einem Embedder, in eine Vektor-DB, in den Prompt des LLM, raus als Antwort. So funktioniert nahezu jedes „Chatte mit deinen Dokumenten"-Produkt. Setzt jetzt euren Sicherheitshut auf und findet die **Vertrauensgrenze.** Sie liegt genau zwischen *was auch immer den Markdown schreibt* und dem Embedder. Denn wenn irgendjemand diese Dateien bearbeiten kann — und „irgendjemand" schließt den Praktikanten ein, den Open-Source-Beitragenden, das als `.md` automatisch protokollierte Support-Ticket, den Pull Request eines nicht vertrauenswürdigen Nutzers — dann kann irgendjemand Inhalte pflanzen, die die KI später *als maßgeblich* zitiert. Das Modell hat keine Ahnung, dass das Dokument feindlich ist; es ruft einfach das relevanteste Stück ab und spricht. Es ist der Verfasser des Dokuments, nicht der Fragesteller, dem ihr vertrauen müsst. Kartiert diese Grenze; dort lebt der Angriff.

---

[FOLIE 25 — Die Erkenntnis: Behandelt Markdown wie eine Datenbank]

Hier also die Erkenntnis, und sie ist ein einziger Satz: **Behandelt Markdown wie eine Datenbank — denn für das LLM ist es eine.** Das bedeutet, die langweiligen, bewährten Kontrollen, die ihr schon kennt, gelten direkt. Zugriffskontrolle auf den Dokumentenordner: Nicht jeder sollte in das schreiben können, woraus die KI liest. Code-Review für `.md`-Änderungen, genauso wie ihr eine Konfigurationsänderung prüfen würdet, denn eine Dokumentbearbeitung ist jetzt eine Verhaltensänderung. Diff-Nachverfolgung im Wiki, damit ihr „wer hat das wann geändert" beantworten könnt. Schneiers alter Satz über das Schichten von Kryptografie, Zugriffskontrolle und all den anderen Technologien, um Angriffe zu *verhindern* — dieser Werkzeugkasten erstreckt sich jetzt auf eure Notizen. Der Praktikant kann nicht mehr einfach ungeprüft in den Dokumentenordner pushen. Willkommen in 2026, wo eure Besprechungsnotizen Produktionsinfrastruktur sind.

---

[FOLIE 26 — SICHERHEIT: Was 2026 wirklich getroffen wird]

Okay. Tief durchatmen. Das ist der Teil, für den ihr gekommen seid. Der nächste Abschnitt handelt davon, wie Datenbanken *wirklich* in der realen Welt gerade jetzt angegriffen werden — nicht in der Theorie, nicht in einem Lehrbuch von 2009, sondern 2026. Mein Ziel ist, dass ihr hier mit genug Vokabular rausgeht, um in einem Krisenraum zu stehen und euch nicht wie der Neue zu fühlen. Ein Rahmen, den ihr durch alles mitnehmt, mit freundlicher Genehmigung von Bruce Schneier: Die Grundlagen — Authentifizierung, Autorisierung, Bedrohungen, Gegner — ändern sich von Jahr zu Jahr kaum. Was sich ändert, ist die *Verpackung.* Dieselbe Handvoll Fehler kommt immer wieder in neuen Kleidern zurück. Ich zeige euch also beides: das beständige Prinzip darunter und die glänzende neue Form, die es dieses Jahr trägt. Zwölf Kategorien kommen. Los.

---

[FOLIE 27 — xkcd #327, Bobby Tables]

Wir beginnen mit dem berühmtesten Datenbankangriff aller Zeiten: **SQL-Injection.** Wenn ihr xkcd Nummer 327 — „Bobby Tables" — noch nie gesehen habt, schlagt es nach, sobald das hier endet. Eine Mutter nennt ihren Sohn `Robert'); DROP TABLE Students;--` und die Schülerdatenbank der Schule verschwindet, weil jemand eine Abfrage durch Zusammenkleben von Zeichenketten gebaut hat. Dieser Comic ist der ganze Mechanismus in einem Panel: **Zeichenkettenverkettung in Abfragen.** Aber hier ist der Teil, den niemand laut sagt — SQL-Injection ist eine *Erfolgsgeschichte* der Sicherheit. Die Ursache war Verkettung; die Lösung sind **parametrisierte Abfragen**, bei denen die Daten nie mit Code verwechselt werden können. Moderne ORMs — Django, SQLAlchemy, Hibernate, Entity Framework — parametrisieren standardmäßig. Die Branche hat den klassischen Bug wirklich behoben. Gibt es Legacy-SQLi noch? Absolut. Aber die Schlagzeile ist größer und seltsamer als „patcht eure Abfragen".

---

[FOLIE 28 — Die Angriffsfläche hat sich ausgeweitet, nicht geschrumpft]

Hier ist die Schlagzeile. Wir haben SQL-Injection behoben, und die Angriffsfläche wurde nicht kleiner — sie **weitete sich aus.** Wir schlossen eine Tür, und dem Gebäude wuchsen elf neue. Das gilt es zu verinnerlichen, bevor wir weitergehen: Sicherheit ist kein Spiel, das man gewinnt und dann weggeht; sie ist eine Fläche, die ständig ihre Form ändert, während sich die Technologie darunter ändert. Jede neue Datenbankfamilie, jedes neue Bereitstellungsmodell, jede neue Abstraktionsschicht, die wir der Bequemlichkeit halber hinzufügten, kam mit ihrer eigenen frischen Art zu versagen. Für den Rest dieses Abschnitts führe ich euch also durch elf *aktuelle* Kategorien von Datenbankangriffen — die, die Leute dieses Jahr auf die Titelseite von Krebs bringen. Manche sind uralte Bugs in neuen Kleidern; manche existierten vor ein paar Jahren wirklich nicht. Alle sind gerade jetzt aktiv.

---

[FOLIE 29 — NoSQL-Injection]

Als die Branche zu NoSQL wechselte, dachten viele Entwickler: „Kein SQL heißt keine SQL-Injection." Falsch. Die Injection wechselte nur die Sprache. In MongoDB *sind* Abfragen JSON — wenn ihr also JSON von einem Webformular nehmt und es direkt in eine Abfrage schiebt, kann ein Angreifer eine Zeichenkette gegen einen **Abfrageoperator** tauschen. Der klassische Login-Bypass: Statt eines Passworts senden sie `{ "$ne": "x" }` — *ungleich x.* Die Abfrage wird zu „finde alice, deren Passwort nicht x ist", und da ihr Passwort nicht der buchstäbliche Buchstabe x ist, trifft es zu. Sie sind drin. Es gibt auch `$where`, das historisch erlaubte, rohes JavaScript in die Datenbank-Engine zu injizieren. Und Couchbases N1QL hat SQL-Geschmack, also gelten die alten Muster direkt. Das Prinzip, direkt aus OWASP: *Jeder* Interpreter kann injiziert werden — nicht nur SQL. Die Klasse ist universell; nur die Syntax wanderte.

---

[FOLIE 30 — Exponierte und fehlkonfigurierte Datenbanken]

Verbringt zehn Minuten auf **Shodan** oder **Censys**, und ihr seht es: Das Internet ist voll von Datenbanken, die nicht im Internet sein sollten. MongoDB an `0.0.0.0` gebunden ohne Authentifizierung. Sperrangelweit offene Elasticsearch-Cluster. Redis ohne Passwort. Postgres mit `host all all 0.0.0.0/0 trust` in seiner Konfiguration. Das sind keine exotischen, schwer errungenen Funde — sie sind *überall.* Und Leute automatisieren die Ernte: Schlagt die **Meow-Angriffe** von 2020 nach, bei denen Bots durchs Internet streiften und Tausende offener Datenbanken zum *Spaß* löschten — kein Lösegeld, keine Forderungen, nur Löschung. Die Bugs sind alt; die *Exposition* ist der neue Teil. Hier also der eine Handlungspunkt, den ich euch eintätowieren würde: Findet heraus, was eure eigene Organisation an öffentliche Schnittstellen gebunden hat, und bestätigt, dass nichts davon eine Datenbank ist. Ein halber Tag Arbeit. Wirklich karriererettend.

---

[FOLIE 31 — Cloud-Fehlkonfigurationen]

In der Cloud ist der Bug selten die Datenbank-Engine — es ist die **Richtlinie darum herum.** Die größten Hits: **öffentliche S3-Buckets voller Datenbank-Dumps** — ein Ingenieur snapshottet die Produktion zum Testen, legt sie in S3 ab, vergisst den Bucket zu sperren; Accenture, Verizon und Dutzende mehr wurden genau so erwischt. **Capital One, 2019** — und hört zu, denn der Mythos ist falsch: Es war *kein* öffentlicher Bucket. Ein Angreifer traf eine fehlkonfigurierte Web Application Firewall mit einer Server-Side Request Forgery, brachte sie dazu, ihre eigenen AWS-Anmeldedaten aus dem Instance-Metadata-Dienst herauszugeben, und diese Anmeldedaten hatten breiten S3-Lesezugriff. Etwa hundert Millionen Datensätze spazierten hinaus. Der Bug war die *IAM-Richtlinie.* Dann **zu breite Lambda-Rollen** — `s3:*` auf `*`, weil es das erste Mal funktionierte — und **Sicherheitsgruppen, die zu `0.0.0.0/0` auf 5432 offen sind.** Die meisten Cloud-Breaches sind Hygienefehler, keine Zero-Days.

---

[FOLIE 32 — Rechteausweitung: DB → OS]

Hier ein Zug, der neue Analysten überrascht: Ein *Datenbank*-Konto kann zu *Shell*-Zugriff auf dem Host werden. Drei Klassiker. **Microsoft SQL Servers `xp_cmdshell`** — eine eingebaute gespeicherte Prozedur, die Betriebssystembefehle als der Datenbankprozess ausführt; seit 2005 standardmäßig deaktiviert, in Legacy-Läden immer noch eingeschaltet vorgefunden, und ein sofortiger kritischer Fund, wenn ihr ihn entdeckt. **PostgreSQLs `COPY ... TO PROGRAM`** — `COPY` ist für Massenladen gedacht, aber ein Superuser kann seine Ausgabe an einen beliebigen Shell-Befehl weiterleiten. **MySQLs benutzerdefinierte Funktionen** — schreibt eine Shared-Object-Datei ins richtige Verzeichnis, ladet sie als SQL-Funktion, und ihr habt `sys_exec` auf dem OS. Das Muster unter allen dreien: Jedes privilegierte Datenbankfeature, das das Betriebssystem berührt, existiert aus einem legitimen Admin-Grund *und* ist Teil eurer Angriffsfläche. Komfortfeatures sind Exploit-Features. Immer beides.

---

[FOLIE 33 — Sicherheitslücken in Data Lakes]

Data Lakes sind das weiche Ziel der modernen Ära. Der Pitch lautet „kippt alles in S3, fragt es später ab" — und das Ergebnis ist, dass *alles* in S3 landet, einschließlich der Dinge, die ihr nie hineinlegen wolltet: Kunden-PII, Finanzdaten, Quellcode mit eingebackenen Anmeldedaten, alles zusammengeführt in einem Speicher, der ursprünglich für irgendeinen Marketing-Analytics-Job eingerichtet wurde. Drei Versagensarten. **Freizügiges IAM** — die Compute-Schicht des Lake braucht breiten Lesezugriff, und dieser Lesezugriff sickert über Konsolenrollen und Assume-Role-Ketten zu Menschen durch. **Keine erzwungene Verschlüsselung im Ruhezustand** auf den Bucket-Schlüsseln. Und **keine schreibseitige Validierung** — jeder mit Schreibzugriff kann eine vergiftete Datei ablegen, die die nachgelagerte Analytik bereitwillig aufnimmt. Wenn ihr also in eine Organisation kommt, stellt zwei Fragen: *Wer kann in den Lake schreiben, und wer kann aus ihm lesen?* Wenn die Antwort auf eine von beiden „wir sind nicht sicher" lautet, ist das euer erster Fund.

---

[FOLIE 34 — Ransomware liebt Datenbanken]

Moderne Ransomware-Banden haben herausgefunden, dass es besser ist, die Datenbank zu treffen als die Endpunkte, weil die Datenbank *das ist, was das Unternehmen zurückbraucht* — maximaler Hebel. Erinnert ihr euch an WannaCry 2017? Es nutzte einen bekannten Windows-SMB-Bug aus, dessen Patch *neunundfünfzig Tage* zuvor erschienen war. Die Lösung existierte seit zwei Monaten, und es legte trotzdem die Welt lahm. Das moderne Datenbank-Playbook hat vier Züge: **die laufende Datenbank verschlüsseln.** Dann **die Backups verschlüsseln** — denn wenn ihr es nicht tut, stellt der Kunde einfach wieder her und lacht euch aus. Dann **zuerst eine Kopie exfiltrieren**, damit ihr mit öffentlicher Offenlegung erpressen könnt, selbst wenn sie *wiederherstellen.* Und Ransomware-as-a-Service macht all das für Banden verfügbar, die keine Zeile davon selbst schreiben könnten. Die Verteidigung ist unglamourös und wirksam: **Offline-, unveränderliche Backups**, plus Wiederherstellungen, die ihr tatsächlich *getestet* habt. Ein ungetestetes Backup ist eine Hoffnung, keine Kontrolle.

---

[FOLIE 35 — Angriffe auf Anmeldedaten]

Zwei alte, beständige Bugs hier. **Standard-Anmeldedaten.** Redis wurde jahrelang ohne Passwort ausgeliefert. Elasticsearch hatte in seiner kostenlosen Stufe keine Authentifizierung, ebenfalls jahrelang. Viele Systeme werden immer noch mit `admin/admin` oder einem leeren `sa`-Passwort auf SQL Server ausgeliefert. Und laut den Breach-Berichten sind *gestohlene Anmeldedaten* der bevorzugte Angriffsvektor für finanziell motivierte und organisierte Kriminalität — Standard-Anmeldedaten sind nur gestohlene Anmeldedaten mit Vorsprung. **Geleakte Verbindungszeichenketten.** Die Dinger, die wie `postgres://user:password@host:5432/dbname` aussehen, werden in Git committet, in Slack eingefügt und in Docker-Images eingebacken — und es gibt Bots, die rund um die Uhr GitHub danach durchkämmen. Die Lösung ist billig, und ihr könnt sie diese Woche ausliefern: **Secret-Scanning beim Pre-Commit**, plus eine Regel, dass Anwendungen sich mit *Dienstkonten* authentifizieren, die das minimale Recht haben, das sie brauchen — nie ein persönliches Login, nie Root.

---

[FOLIE 36 — Lieferkette: die DB-Bibliotheken, denen ihr vertraut]

Ihr schreibt euren Datenbanktreiber nicht von Grund auf — ihr macht `npm install` oder `pip install`, und jeder andere Entwickler in eurer Organisation auch. Das bedeutet: Wenn ein Angreifer eine beliebte Bibliothek kompromittiert, ist er eine Installation davon entfernt, Code auf eurem Datenbank-Client auszuführen. Drei reale Muster. **Bösartige npm-Pakete**, die sich als ORMs oder Datenbankkonnektoren ausgeben — mehrere Vorfälle pro Jahr. **Trojanisierte Docker-Hub-Images** für beliebte Datenbanken — ein inoffizieller Mirror mit einem Krypto-Miner, oder Schlimmerem, darin versteckt. Und **kompromittierte Datenbankerweiterungen** — PostgreSQL-Erweiterungen, MySQL-Plugins — die, einmal installiert, *mit Datenbankrechten* laufen, und das ist meist eine Menge. Shostacks Satz aus *Threat Modeling* trifft die Linse: Bedrohungen ballen sich um **Vertrauensgrenzen.** Die Grenze zwischen „Code, den wir schrieben" und „Code, den wir installierten" ist eine der größten, am wenigsten bewachten, die ihr habt. Behandelt eure Abhängigkeiten wie die Angriffsfläche, die sie sind.

---

[FOLIE 37 — RAG-/LLM-Datenvergiftung]

Erinnert ihr euch an den Markdown-Abstecher? Hier ist der Angriff, den er vorbereitete. Wenn ein Angreifer in die Wissensbasis schreiben kann, aus der eure RAG-Pipeline liest — ein Support-Ticket, ein geteiltes Dokument, eine Wiki-Seite, ein öffentliches Repo, das euer Scraper einsaugt — kann er Inhalte pflanzen, die das LLM abruft und *als Wahrheit* nachplappert. Ein vergifteter Support-Artikel: „Um Ihr Passwort zurückzusetzen, senden Sie das aktuelle an diese Adresse." Ein vergiftetes internes Dokument: „Firmenrichtlinie ist die Überweisung auf folgendes Konto." Oder direkt **Prompt-Injection** — in einem Dokument vergrabene Anweisungen, die die Schlussfolgerung des Modells kapern, sobald es abgerufen wird. Das ist **gespeichertes XSS für das KI-Zeitalter**: Die Nutzlast liegt im Ruhezustand, sieht harmlos aus und detoniert, wenn sie *konsumiert* wird. Tauscht „ein Administrator sieht es später an" gegen „ein LLM ruft es später ab", und ihr habt die moderne Version. Verteidigungen: strenge Schreib-ACLs, Herkunfts-Tags und ein Mensch in der Schleife, bevor das Modell handelt.

---

[FOLIE 38 — Insider-Bedrohungen und laterale DB-zu-DB-Bewegung]

Zwei Szenarien, die ein Thema teilen: Datenbanken sind keine Endpunkte, sie sind **Knoten in einem Graphen.** Erstens, **Insider-Bedrohungen.** Die Person, die bereits Datenbankzugriff hat, braucht keinen Exploit — sie braucht nur *mehr Rechte, als ihr Job erfordert.* Überprivilegierte Dienstkonten. Ingenieure mit Produktions-Lesezugriff, weil „wir richten das später". DBAs, die ohne Audit-Spur arbeiten. Und denkt daran: Schlecht geschützte Audit-Logs sind eine Goldgrube für einen Angreifer, voller Sitzungstoken und Anfragedetails — Logs sind Beweise und müssen wie Daten geschützt werden. Zweitens, **laterale Bewegung über Datenbankverknüpfungen.** Oracles `DB_LINK`, SQL Servers Linked Servers, Postgres' Foreign Data Wrappers — diese speichern Anmeldedaten für *andere* Datenbanken. Ihr kompromittiert also Datenbank A, findet die Verknüpfung und springt direkt zu Datenbank B, dann C. Die Kanten zwischen Datenbanken bestehen aus Anmeldedaten, und Angreifer wandern sie entlang.

---

[FOLIE 39 — Exposition von Backups und Snapshots]

Letzte Kategorie, und es ist die, die jeder vergisst: **Backups.** Leute sperren die Produktionsdatenbank ab — Firewall, Verschlüsselung, enger Zugriff — und sichern sie dann auf eine Netzwerkfreigabe mit Standardberechtigungen oder einen S3-Bucket mit breitem Lesezugriff. Es sind dieselben Kronjuwelen-Daten wie in der Produktion, geschützt mit halb so viel Liebe. Das Muster: unverschlüsselte Backups auf einer Freigabe, lesbar für *Domänenbenutzer.* Cloud-Snapshots „nur für die Migration" kontoübergreifend geteilt und nie ent-geteilt. Off-Site-Backups, einem Anbieter übergeben, dessen Sicherheitslage nie jemand prüfte. Wendet dieselbe Disziplin, die ihr auf Live-Daten anwendet — identifizieren, authentifizieren, autorisieren, auditieren — auf jedes Backup und jeden Snapshot an. Wenn überhaupt, wendet sie *härter* an, denn das Backup ist das Mittel der *letzten Instanz.* Wenn alles andere versagt hat und ihr nach dem Backup greift, ist das der schlechtestmögliche Moment, um zu entdecken, dass es sperrangelweit offen war.

---

[FOLIE 40 — Eure mentale Landkarte]

Ziehen wir die Karte wieder zusammen. Eins: Eine Datenbank ist **organisierte Speicherung plus eine Möglichkeit, Fragen zu stellen** — Aktenschrank, Excel oder ein Cluster mit hundert Millionen Zeilen, dieselbe Idee. Zwei: Es gibt **zehn Familien**, jede mit ihrem eigenen Vorzeige-Haken — und ihr kennt jetzt alle zehn. Drei: Fast alles lebt in der **Cloud**, wo der Bug selten die Engine und fast immer die **Konfiguration** ist — geteilte Verantwortung, euch gehören die Richtlinie und die Daten. Vier: **Markdown ist jetzt eine Datenbank für LLMs**, und RAG-Vergiftung ist das neue gespeicherte XSS. Fünf: **SQL-Injection wurde behoben, und die Angriffsfläche weitete sich** trotzdem in elf andere Formen aus. Das ist der ganze Vortrag in fünf Zeilen. Wenn ihr euch nichts anderes merkt, merkt euch: Den Daten zu folgen ist die Aufgabe, und die Daten sind immer in einer Datenbank.

---

[FOLIE 41 — Was nächste Woche zu tun ist]

Fünf konkrete Dinge, die ihr *nächste Woche* tun könnt — nicht irgendwann, nächste Woche. Eins: **Installiert PostgreSQL lokal**, macht eine Tabelle, schreibt ein `SELECT`. Das Ding anzufassen entmystifiziert es für immer; es hört auf, beängstigend zu sein, sobald es auf eurem Laptop läuft. Zwei: Macht die **PortSwigger-SQL-Injection-Labs** — sie sind kostenlos, und ihr schreibt bis zum Ende eines Nachmittags einen funktionierenden Exploit. Drei: **Durchstöbert Shodan oder Censys** — legal, nur Systeme, die euch gehören oder die ihr testen dürft — und seht, wie „exponiert" wirklich aussieht. Vier: **Lest einen Breach-Bericht** von Anfang bis Ende — Capital One, Equifax oder MOVEit; echte Breaches sind die besten Lehrbücher, die es gibt. Fünf: **Findet heraus, welche Datenbanken eure eigene Organisation betreibt.** Die meisten SOC-Analysten können das nicht beantworten. Verbringt einen Nachmittag damit, die echte Liste zu erstellen, und ihr seid sofort nützlicher als die Hälfte des Teams.

---

[FOLIE 42 — Lesenswerte Lesezeichen]

Fünf Lesezeichen zum Mitnehmen. **PortSwigger Web Security Academy** — portswigger.net/web-security — die beste kostenlose Auffahrt zur Web-App-Sicherheit überhaupt, und wo ihr euch an echter Injection die Zähne ausbeißt. **SQLBolt** — sqlbolt.com — lernt SQL interaktiv, im Browser, auf die unterhaltsame Art, ohne Installation. **Use The Index, Luke** — use-the-index-luke.com — wenn ihr bereit seid für die tiefe Magie davon, wie Indizes und Abfrageleistung wirklich funktionieren. **DB-Engines Ranking** — db-engines.com — die laufende Beliebtheitsrangliste praktisch jeder existierenden Datenbank, großartig, um zu sehen, was sich zu lernen lohnt. Und die **OWASP Top 10** — owasp.org/Top10 — die kanonische Liste der Web-Schwachstellen, einschließlich der Injection- und Fehlkonfigurationsklassen, die wir heute getroffen haben. Setzt diese fünf als Lesezeichen, und ihr habt monatelanges selbstgesteuertes Lernen in der Warteschlange, kostenlos.

---

[FOLIE 43 — Datenbanken sind, wo das Geld ist. Buchstäblich.]

Ich lasse euch hiermit zurück. Es gibt einen alten Satz, der dem Bankräuber Willie Sutton zugeschrieben wird. Gefragt, warum er Banken ausraubte, soll er gesagt haben: *weil dort das Geld ist.* In 2026 ist das Geld in **Datenbanken.** Kundendaten, Finanzdaten, Gesundheitsdaten, geistiges Eigentum, Modellgewichte, Vektor-Embeddings, Quellcode, Geheimnisse — all das lebt in irgendeiner Datenbank, irgendwo. Die Angreifer wissen das bereits; deshalb endet jede Breach-Geschichte dort, wo sie endet. Das Einzige, was sich in der letzten Stunde geändert hat, ist, dass *ihr es jetzt auch wisst* — und, wichtiger, ihr habt die Karte, um es zu finden, zu benennen und darüber nachzudenken, wie es versagt. Ihr braucht kein Informatikstudium, um hier gefährlich zu sein. Ihr brauchtet die Karte. Ihr habt sie. Jetzt wisst ihr, wo ihr schauen müsst.

---

[FOLIE 44 — Quellen: zitierte Bücher]

Fast geschafft — die Belege. Alles, was ich euch heute erzählt habe, steht auf den Schultern von Leuten, die es ordentlich aufgeschrieben haben, und diese Folie listet die Bücher, auf die ich mich gestützt habe — Beaulieus *Learning SQL*, Clarkes *SQL Injection Attacks and Defense*, Schneiers *Secrets and Lies*, Shostacks *Threat Modeling*, das *Web Application Hacker's Handbook*, *Cybersecurity Attack and Defense Strategies*, Tanya Jancas *Alice and Bob Learn Application Security* und die OWASP Top 10 — die aktuelle Ausgabe von 2025 — unter anderen. Ihr müsst nicht alle lesen — aber wenn euch heute eine einzige Kategorie angezündet hat, wartet auf dieser Folie ein ganzes Buch darauf, euch tiefer zu führen. Fotografiert sie, bevor sie verschwindet. Das sind die Schultern, auf denen der ganze Vortrag steht — und mit ihnen dort auf der Leinwand: eröffnen wir die Fragerunde.

---

[FOLIE 45 — Fragerunde: Legt los]

Und das war der Vortrag — danke, dass ihr die ganzen fünfundvierzig Minuten bei mir geblieben seid. Diese letzte Folie ist, wo wir öffnen, also ist das eure Zeit: Werft mir eure Fragen zu, eure Kriegsgeschichten, das Ding aus eurer eigenen Umgebung, das euch die ganze Zeit, in der ich sprach, beschäftigt hat. Keine Frage ist hier zu grundlegend — denkt daran, die ganze Prämisse dieses Vortrags ist, dass niemand das alles wissend geboren wird, und die Leute, die die „offensichtlichen" Fragen stellen, sind meist die, die leise für die halbe Halle sprechen. Starrt mich nicht alle gleichzeitig an. Wenn uns die Zeit ausgeht oder eure Frage ein Whiteboard braucht, schnappt mich danach oder meldet euch — ihr findet mich auf github.com/CryptoJones, oder CryptoJones@infosec.exchange. Während die ersten Hände hochgehen: Was hat euch am meisten überrascht? Für viele ist es, dass Markdown-Notizen jetzt eine lebende Datenbank sind. Also — legt los. Und wann immer wir hier fertig sind: geht herausfinden, welche Datenbanken *eure* Organisation betreibt. Im Ernst. Geht.

---

*Etwa 45 Minuten Skript über 45 Folien, abschließend mit offener Fragerunde. Ein eigenständiger Vortrag von CryptoJones (Aaron K. Clark).*
