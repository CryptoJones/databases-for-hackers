# Les bases de données pour les hackers — Script de l'intervenant (une minute par diapositive)

**Intervenant :** Aaron K. Clark
**Format :** 45 diapositives × ~1 minute ≈ 45 minutes, puis questions-réponses
**Public :** Analystes sécurité débutants, SOC junior, pentesters débutants, profils GRC passant au technique
**Ton :** Conversationnel. Un ami intelligent au bar. Jamais condescendant.

> **Notes de rythme :** Chaque bloc ci-dessous fait ~130-150 mots = environ une minute à un rythme détendu de 140 mots par minute.
> Dans la vidéo qui accompagne, un léger carillon marque chaque changement de diapositive : quand tu l'entends, avance.
> `[CROCHETS]` = remplis tes propres détails avant la présentation.

---

[DIAPOSITIVE 1 — Titre : « Les bases de données pour les hackers » — Présentation indépendante de CryptoJones / Aucun diplôme d'informatique requis]

Très bien — bienvenue. Trouvez une place, prenez votre café. Le titre dit tout : *Les bases de données pour les hackers*, et le seul prérequis est la ligne en dessous — vous n'avez *pas* besoin d'un diplôme d'informatique pour être dans cette salle. Si vous avez apporté un carnet, ouvrez-le. Sinon, détendez-vous — il y a des diapositives, un script écrit, et un enregistrement. Je ne vais rien vous faire mémoriser. Tout l'objectif des quarante-cinq prochaines minutes est de vous donner une *carte mentale* — celle qui vous permet d'entrer dans n'importe quel rapport de fuite, n'importe quelle mission de pentest, n'importe quelle alerte SOC, et de savoir aussitôt ce que vous regardez. Aujourd'hui, on ne construit pas de bases de données. On apprend à les lire, à les attaquer et à les défendre. C'est parti.

---

[DIAPOSITIVE 2 — À propos de moi : Aaron K. Clark]

Un mot rapide sur moi, puis on plonge. Je suis Aaron Clark — même si en ligne vous me trouverez surtout sous le nom de CryptoJones. Je suis étudiant en master à l'Eastern University, ce qui est une façon polie de dire que je suis fauché, sur-caféiné, et que j'ai dû apprendre tout ça à la dure, sans diplôme d'informatique sur lequel m'appuyer. Personne ne sponsorise cette présentation. Je la donne parce que c'est celle que j'aurais aimé qu'on me donne à *moi* il y a deux ans, à l'époque où chaque conversation sur les bases de données en sécurité semblait supposer que j'écrivais du SQL depuis l'âge de douze ans. Je suis arrivé à la sécurité par le chemin le plus long, sans formation en informatique, et j'ai dû démêler le volet bases de données tout seul. Si c'est toi — si le monde des bases de données ressemble à un club privé dont on ne t'a jamais donné le mot de passe — tu es exactement la personne pour qui j'ai construit ça.

---

[DIAPOSITIVE 3 — « Chaque fuite dont vous avez entendu parler se termine dans une base de données. »]

Voici la seule phrase que je veux que vous reteniez de toute la présentation. *Chaque fuite dont vous avez entendu parler se termine dans une base de données.* Equifax, 2017 — les données de cent quarante-sept millions de personnes — vivaient dans une base de données. Capital One, 2019 — cent millions de demandes de crédit — base de données. MOVEit, 2023 — la faille de transfert de fichiers devenue catastrophe de chaîne d'approvisionnement dans tout le Fortune 500 — chacune de ces organisations perdait ses données depuis une base de données. SolarWinds, T-Mobile, LinkedIn, OPM, Marriott. Je pourrais remplir les quarante-cinq minutes rien qu'avec des noms. Les gros titres changent, les entreprises changent, les communiqués changent. La destination, jamais. Donc si les bases de données sont l'endroit où *se termine* chaque histoire, apprendre à y penser, c'est apprendre à lire toute l'histoire.

---

[DIAPOSITIVE 4 — Les joyaux de la couronne : pas votre appli, pas votre pare-feu — les données]

Regardez ce que les attaquants veulent vraiment. Pas votre belle application monopage. Pas votre schéma de microservices. Pas votre pare-feu — sauf comme un obstacle à franchir. Ils veulent les *données*. Les joyaux de la couronne. Ce qui se transforme en argent, en levier, ou en gros titre avec le nom de votre entreprise. Tout le reste de votre pile — les répartiteurs de charge, les conteneurs, le maillage de services — n'est que l'emballage autour de la chose dans le coffre. Et la chose dans le coffre, c'est une base de données. Donc quand vous triez une alerte ou cadrez une mission, entraînez-vous à poser tôt une question : *où vivent les données, et qu'y a-t-il entre l'attaquant et elles ?* Cet instinct — suivre le chemin jusqu'aux données — c'est l'essentiel de ce qui sépare un analyste senior d'un débutant.

---

[DIAPOSITIVE 5 — Qu'est-ce qu'une base de données ? Du stockage organisé + un moyen de poser des questions]

Enlevons le jargon. Une base de données, ce sont deux choses agrafées ensemble : du *stockage organisé*, plus *un moyen de poser des questions*. C'est tout le concept. Le reste, ce sont des détails. Vous avez déjà utilisé un classeur de bureau — des dossiers papier, par ordre alphabétique de nom ? Vous avez utilisé une base de données. Le classeur, c'est le stockage ; vos yeux, c'est le moteur de requêtes. Vous avez déjà fait Ctrl-F dans Excel pour trouver une ligne ? Base de données. Le tableur, c'est le stockage ; chercher-remplacer, c'est la requête. Ce qu'une *vraie* base de données ajoute par-dessus, c'est l'échelle, la vitesse, la concurrence — plein de gens y accédant en même temps — et un langage formel pour demander au lieu d'utiliser ses yeux. C'est tout. C'est un classeur qui ne se fatigue jamais, que mille personnes peuvent ouvrir d'un coup, et auquel on parle dans un langage structuré. Gardez cette image ; tout le reste en découle.

---

[DIAPOSITIVE 6 — Les six mots qu'il vous faut + CRUD]

Voici tout le vocabulaire nécessaire pour tenir une vraie conversation avec un administrateur de base de données. Six mots. Une **table** est un onglet de tableur — clients, commandes, événements de connexion. Une **ligne** est un enregistrement — un client, une alerte. Une **colonne** est un attribut — e-mail, IP source, total. Une **requête** est la question que vous posez : « montre-moi chaque connexion venue de l'étranger dans la dernière heure ». Un **schéma** est la *forme* des données — les colonnes, leurs types, les règles ; et l'écart entre « cette colonne contient des e-mails » et « cette colonne contient ce que l'appli y a balancé » est exactement là où vivent les vulnérabilités. Un **index** est un marque-page qui rend les recherches instantanées — et aussi la façon dont les attaquants chronomètrent l'injection à l'aveugle. Ajoutez **CRUD** — Créer, Lire, Mettre à jour, Supprimer — les quatre verbes que fait toute base de données. Maîtrisez ces six-là et vous êtes assez à l'aise.

---

[DIAPOSITIVE 7 — Tour d'histoire : les fossiles que vous verrez en prod]

Petit tour d'histoire — pas parce que j'adore l'histoire, mais parce que chaque truc bizarre d'un environnement réel est un *fossile* de l'une de ces ères. **Années 1960, fichiers plats :** des données dans un fichier ; les permissions étaient le seul contrôle d'accès. **Fin des années 60, hiérarchique** (IMS d'IBM) : données dans un arbre, modèle de menace mainframe — accès physique. **Années 1970, réseau/CODASYL :** des enregistrements liés par des pointeurs ; ça tourne encore dans l'arrière-boutique de votre banque. **1970, le modèle relationnel de Codd :** des tables et des maths — et le contrôle d'accès *à l'intérieur* de la base, droits et rôles. **Années 1980 :** Oracle, DB2, SQL Server — les bases se mettent en réseau, donc il y a maintenant un problème d'authentification. **Années 1990, client-serveur et open source :** chaque formulaire web devient une porte — l'injection SQL est née. **Années 2000, NoSQL :** l'échelle comme religion. **Années 2010, le cloud :** la responsabilité partagée. **Années 2020, vectoriel et serverless :** empoisonnement de données et injection de prompt. Repérez l'ère, prédisez le bug.

---

[DIAPOSITIVE 8 — Dix familles de bases de données]

Il y a dix familles de bases de données que vous croiserez dans la nature, et je vais vous donner les mêmes quatre choses pour chacune : ce qu'elle stocke, quand l'utiliser, deux produits réels, et *un* piège de sécurité. Relationnelle, document, clé-valeur, colonne, graphe, recherche, séries temporelles, vectorielle, embarquée, et lac de données. Prenez des notes surtout sur les pièges — ce sont les lignes qui reviennent en entretien et en mission. N'essayez pas de mémoriser les noms de produits ; vous les absorberez par exposition. Ce que je veux qui reste, c'est la *forme* de chaque famille, parce que la forme vous dit l'attaque. Une table rigide tombe différemment d'un document JSON souple, qui tombe différemment d'un énorme bucket dans le cloud. Dix formes, dix modes de défaillance. C'est parti — une par minute.

---

[DIAPOSITIVE 9 — 1. Relationnelle / SQL]

Numéro un, relationnelle — SQL. Des lignes et des colonnes, un schéma fort, et SQL comme langage de requête. Produits : **PostgreSQL, MySQL/MariaDB, SQL Server, Oracle.** Utilisez-la quand vos données ont des relations claires et que la cohérence vous importe vraiment — tout ce qui est financier, tout ce qui est réglementé. C'est le cheval de trait de toute l'industrie ; dans le doute, les données sont là. Piège de sécurité — le célèbre : **l'injection SQL**, qui survient quand les développeurs construisent des requêtes en collant l'entrée utilisateur directement dans une chaîne. On y consacre du vrai temps plus tard, alors gardez-le sous le coude. Beaulieu, dans *Learning SQL*, explique pourquoi cette famille ne mourra pas : une base relationnelle bien conçue peut gérer des quantités énormes de données tout en les gardant cohérentes. Ennuyeuse, fiable, partout — et toujours l'endroit numéro un où les débutants trouvent de vrais bugs.

---

[DIAPOSITIVE 10 — 2. Magasins de documents]

Numéro deux, les magasins de documents. Au lieu de lignes rigides, ils stockent des **documents JSON**, et chaque document peut être un peu différent — schéma flexible. Produits : **MongoDB, Couchbase, Firestore.** Utilisez-les quand vos données sont naturellement imbriquées et que leur forme change avec le temps — catalogues produits, profils utilisateurs, contenu. C'est la famille qui a propulsé une grande part de l'ère web du « avance vite ». Piège de sécurité — **l'injection NoSQL** via des opérateurs de requête comme `$ne`, `$gt` et `$where` ; l'injection n'a pas disparu quand SQL est parti, elle a juste changé de langage, et on l'exploitera plus tard. L'autre classique : pendant des années, l'installation par défaut s'attachait à toutes les interfaces *sans authentification*, ce qui est exactement pourquoi Shodan a fini rempli de MongoDB ouverts. Données flexibles, réglages de sécurité flexibles — parfois *absents*.

---

[DIAPOSITIVE 11 — 3. Magasins clé-valeur]

Numéro trois, clé-valeur — la base de données la plus simple qui soit. C'est un dictionnaire géant : une clé entre, une valeur sort, rien de plus sophistiqué. Produits : **Redis, Memcached, DynamoDB.** Utilisez-les pour les caches, les magasins de sessions, les limiteurs de débit, les classements — tout ce qui demande une vitesse fulgurante et une recherche simple. Redis en particulier est partout dans les piles web modernes, juste derrière l'appli. Piège de sécurité — pendant des années, Redis a été livré **sans mot de passe par défaut**, et sa commande `CONFIG SET` permettait historiquement à un attaquant d'écrire des fichiers — comme une clé SSH — directement sur le disque de l'hôte de la base. Donc un Redis ouvert lors d'un pentest n'est pas qu'une trouvaille ; c'est souvent un *point d'appui* — un moyen d'entrer sur la machine elle-même. Conception vitesse-d'abord, réglages sécurité-ensuite. Notez ce motif qui se répète à travers ces familles.

---

[DIAPOSITIVE 12 — 4. Colonne]

Numéro quatre, orientée colonne — parfois appelée « colonne large ». Conçue pour une échelle *massive* répartie sur de nombreuses machines. Produits : **Apache Cassandra, HBase, ScyllaDB.** Utilisez-la quand vous avez tellement de données qu'aucune machine seule ne peut les contenir et que vous n'avez pas besoin de jointures complexes — pensez à Netflix, Apple et Instagram, tous sur Cassandra. Le prix de cette échelle, ce sont les commodités relationnelles ; vous concevez autour de vos requêtes à l'avance. Piège de sécurité — les nœuds de ces clusters se *font typiquement confiance implicitement* sur le port du protocole de gossip. Traduction : entrer dans le réseau de gestion du cluster équivaut souvent à avoir root sur tout le jeu de données. Donc quand vous cadrez l'un d'eux, la question intéressante n'est pas la porte d'entrée — c'est de savoir si le réseau interne du cluster est segmenté du reste. En général, il ne l'est pas.

---

[DIAPOSITIVE 13 — 5. Bases de données graphe]

Numéro cinq, les bases de données graphe. Ici, les données *sont* les relations — des nœuds et des arêtes, pas des lignes. Produits : **Neo4j, Amazon Neptune, ArangoDB.** Utilisez-les pour les réseaux sociaux, la détection de fraude et — attention, gens de la sécurité — **l'analyse d'identité et d'accès.** Si vous n'avez jamais joué avec **BloodHound**, l'outil de chemins d'attaque Active Directory, faites-le ce week-end ; c'est littéralement une base de données graphe qui vous montre « qui peut devenir administrateur de domaine, et comment ». Piège de sécurité — les langages de requête graphe comme **Cypher sont aussi injectables.** Je veux tuer un mythe ici même : l'injection NoSQL n'est *pas* un problème propre à MongoDB. Chaque fois qu'une entrée non fiable est concaténée dans un langage de requête — n'importe lequel — vous avez une classe d'injection. Les bases graphe sont un magnifique rappel que le principe est universel, pas lié à SQL.

---

[DIAPOSITIVE 14 — 6. Moteurs de recherche]

Numéro six, les moteurs de recherche — conçus pour des requêtes plein-texte rapides sur d'énormes tas de texte. Produits : **Elasticsearch, OpenSearch, Solr.** Utilisez-les pour la recherche de logs, la recherche sur les sites e-commerce et — celui-là vous concerne — la **colonne vertébrale de la plupart des SIEM.** Votre SOC interroge très probablement un cluster Elasticsearch ou OpenSearch chaque jour, même si vous ne le voyez jamais directement. Piège de sécurité — historiquement, ils étaient livrés **sans authentification intégrée** dans la version gratuite, et des clusters exposés à internet contenant des *milliards* d'enregistrements font la une de façon récurrente depuis une décennie entière. Associez ce fait à Shodan et vous avez un projet de recherche de week-end — *sur des systèmes que vous possédez ou êtes autorisé à tester*, et ceux-là seulement. L'outil qui alimente votre pile de détection est, ironiquement, l'une des familles de bases de données les plus exposées d'internet.

---

[DIAPOSITIVE 15 — 7. Séries temporelles]

Numéro sept, les bases de données de séries temporelles — optimisées pour une seule chose : énormément de points de données indexés par le temps. Produits : **InfluxDB, TimescaleDB, Prometheus.** Utilisez-les pour les métriques, les tableaux de bord d'observabilité, la télémétrie IoT et capteurs — tout ce qui est en gros « un nombre, chaque seconde, pour toujours ». Si votre organisation a un mur de tableaux de bord Grafana, il y en a une là-dessous. Piège de sécurité — elles vivent presque toujours *à l'intérieur du périmètre* et sont *souvent sans authentification*, parce que l'hypothèse est « seuls nos propres services lui parlent ». Donc un attaquant qui atterrit dans le réseau peut lire chaque graphique de CPU, de mémoire et de trafic que vous avez — ce qui lui dit discrètement quelles machines font le travail *intéressant*, où se trouve la base de données chargée, quand tourne la sauvegarde. C'est de l'or pour la reconnaissance, grand ouvert, parce que personne ne pense aux métriques comme à quelque chose de sensible.

---

[DIAPOSITIVE 16 — 8. Bases de données vectorielles]

Numéro huit, les bases de données vectorielles — celles de l'IA, et la plus récente famille de la liste. Elles stockent des **embeddings** : de longues listes de nombres qui capturent le *sens* d'un morceau de texte ou d'une image, pour pouvoir chercher par similarité plutôt que par correspondance exacte. Produits : **Pinecone, Milvus, Weaviate**, et **pgvector**, l'extension qui permet à un PostgreSQL ordinaire de jouer à ce jeu. Utilisez-les pour la génération augmentée par récupération, les moteurs de recommandation et la recherche sémantique. Piège de sécurité — **l'empoisonnement de données.** Si un attaquant parvient à glisser un document malveillant dans votre magasin vectoriel, le modèle de langage assis par-dessus le récupérera volontiers et le citera à vos utilisateurs *comme une vérité.* C'est une surface d'attaque entièrement nouvelle qui n'existait quasiment pas il y a cinq ans, et on y reviendra à la fin, parce que c'est là que beaucoup d'entre vous finiront par travailler.

---

[DIAPOSITIVE 17 — 9. Embarquée / Edge]

Numéro neuf, les bases de données embarquées et edge. Ici, la base vit *à l'intérieur de l'application* — c'est un fichier sur disque, pas un serveur auquel on se connecte par le réseau. Produits : **SQLite, DuckDB, LevelDB.** SQLite à elle seule est la base de données la plus déployée sur Terre : elle est dans votre navigateur, votre téléphone, votre voiture, et en gros chaque avion construit ces vingt dernières années. Utilisez-la pour du stockage local, dans l'appli, où monter un serveur serait exagéré. Piège de sécurité — quand la base de données n'est qu'un *fichier*, toute l'attaque se réduit à « vole le fichier ». Pas d'exploit réseau, pas d'injection — copiez le fichier hors de l'appareil et lisez-le à votre aise. C'est le quotidien des pentesters mobiles : la moitié de la mission, c'est de trouver le fichier SQLite qu'une appli a laissé traîner avec des données sensibles dedans, non chiffrées.

---

[DIAPOSITIVE 18 — 10. Lacs de données / Lakehouses]

Numéro dix, les lacs de données et les lakehouses. Au lieu de structurer les données à l'*entrée*, vous balancez tout dans un stockage objet bon marché et vous structurez à la *sortie*. Produits : **S3 + Athena, Delta Lake, Apache Iceberg, Snowflake.** Le jargon, c'est **schéma à la lecture** contre **schéma à l'écriture** — l'ancien relationnel s'engageait sur la forme à l'avance ; les lacs s'engagent plus tard, au moment de la requête. Utilisez-les quand vous voulez tout amasser maintenant et décider du sens plus tard. Piège de sécurité — d'immenses réservoirs de données dans S3 avec un IAM trop large, sans chiffrement au repos imposé, et sans audit de qui a lu quoi. C'est l'équivalent moderne de laisser le classeur déverrouillé — sauf que le classeur a maintenant la taille d'un immeuble, et personne n'est tout à fait sûr de tout ce qui a été jeté dedans. On reverra les défaillances propres aux lacs dans la section sécurité.

---

[DIAPOSITIVE 19 — Services de bases de données cloud : le paysage]

Entrez dans n'importe quel environnement bâti ces cinq dernières années et les bases de données ne vivent pas dans une salle serveur — elles vivent dans un compte cloud. Donc il vous faut les noms des fournisseurs, parce que c'est ainsi que ces choses apparaissent dans les alertes, les politiques IAM, les tickets de réponse à incident. Sur **AWS, GCP et Azure**, vous verrez les mêmes catégories sous des noms de marque différents : relationnelle managée, document/NoSQL, entrepôt de données, cache, graphe, séries temporelles, et stockage objet. AWS a le menu le plus large — RDS, DynamoDB, Redshift, ElastiCache, Neptune, Timestream, S3. GCP s'appuie sur Cloud SQL, Firestore, Bigtable et le vraiment ravissant BigQuery. Azure canalise beaucoup via Azure SQL et **Cosmos DB**, un caméléon qui parle plusieurs dialectes de bases de données à la fois. Vous n'avez pas à mémoriser cette grille — vous devez reconnaître les noms quand ils filent dans une cellule de crise.

---

[DIAPOSITIVE 20 — Antisèche des bases de données cloud]

Voici l'antisèche en un tableau — faites une capture de cette diapositive. **Relationnel :** AWS c'est RDS et Aurora, GCP c'est Cloud SQL et AlloyDB, Azure c'est Azure SQL Database. **Document/NoSQL :** DynamoDB et DocumentDB chez AWS, Firestore et Bigtable chez GCP, Cosmos DB chez Azure. **Entrepôt :** Redshift et Athena, contre BigQuery, contre Synapse. **Cache :** ElastiCache, Memorystore, Azure Cache for Redis. **Graphe :** Neptune chez AWS, le mode graphe de Cosmos chez Azure, et GCP qui dit éternellement « bientôt ». **Stockage objet :** S3, Cloud Storage, Blob Storage. La raison pour laquelle ça compte en sécurité : chacun de ceux-là est une *surface IAM différente* avec des *réglages par défaut différents*. L'attaque, c'est rarement le moteur — c'est la politique qui l'enveloppe, et la politique vit dans la colonne de ce tableau où vous vous tenez. Connaissez la colonne, sachez où regarder.

---

[DIAPOSITIVE 21 — Modèle de responsabilité partagée]

C'est la diapositive la plus importante de la section cloud. Le **modèle de responsabilité partagée.** Le fournisseur cloud possède les parties sous la ligne de flottaison : l'hyperviseur, le métal, la sécurité physique, et le patch du *moteur* de base de données lui-même. Vous — le client — possédez tout ce qui est au-dessus : la **configuration**, les **politiques d'accès** et l'IAM, les **données**, et vos **choix de chiffrement.** La documentation AWS le dit clairement — une fois que vous êtes client, protéger vos données au repos et en transit, c'est *votre* part de la responsabilité maintenant. Traduisez ça en langage sécurité et ça devient la phrase la plus utile de toute la sécurité cloud : **presque toute fuite de base de données cloud est une mauvaise configuration côté client**, pas le fournisseur qui se fait pirater. Bucket public, groupe de sécurité grand ouvert, snapshot partagé avec le mauvais compte. Le fournisseur échoue rarement. *Nous* configurons l'échec.

---

[DIAPOSITIVE 22 — Ports courants de bases de données — gravez-les]

Mémorisez ces sept numéros de port. Les analystes SOC les utilisent chaque jour ; les pentesters les scannent chaque jour. **MySQL, 3306. PostgreSQL, 5432. Microsoft SQL Server, 1433. MongoDB, 27017. Redis, 6379. Elasticsearch, 9200. Cassandra, 9042.** Voilà l'ensemble. Et voici la règle qui va avec : si vous voyez *l'un* de ceux-là exposé directement à internet, c'est une **trouvaille** — à chaque fois, sans exception, signalez-la. Un port de base de données ouvert sur `0.0.0.0`, c'est l'équivalent cloud de laisser la porte du coffre béante sur la rue. Groupes de sécurité réseau, règles de pare-feu, listes de sécurité — chaque cloud l'appelle un peu différemment, mais le boulot est identique : fermez le port qui n'a pas besoin d'être ouvert. Si vous n'apprenez aucun autre chiffre aujourd'hui, apprenez ces sept-là.

---

[DIAPOSITIVE 23 — Vos notes sont maintenant une base de données]

Bref détour avant le final sécurité, parce que ça sera sur votre radar d'ici un an, que ça vous plaise ou non. **Les fichiers Markdown sont maintenant une base de données** — pas en métaphore, littéralement, du genre que lit un LLM. Voici le motif. Vous prenez un dossier de fichiers `.md` — un coffre Obsidian, un export de wiki, un tas de notes de réunion, les docs GitHub de votre équipe. Vous les passez dans un *modèle d'embeddings* qui transforme le texte en vecteurs, et vous stockez ces vecteurs dans une base de données vectorielle. Maintenant, quand quelqu'un pose une question à votre assistant IA, le système cherche sémantiquement dans vos notes, attrape les morceaux les plus pertinents, et les fourre dans le prompt du modèle. Votre humble dossier de notes vient de devenir la *source de vérité* qu'une IA répète à vos utilisateurs. Posez-vous un instant sur à quel point c'est étrange — et exposé.

---

[DIAPOSITIVE 24 — Pipeline RAG : où est la frontière de confiance ?]

Ce motif a un nom : **RAG** — génération augmentée par récupération. Fichiers `.md`, vers un encodeur, dans une base vectorielle, dans le prompt du LLM, en sortie une réponse. C'est ainsi que fonctionne presque tout produit « discute avec tes docs ». Maintenant, mettez votre casquette sécurité et trouvez la **frontière de confiance.** Elle se situe juste entre *le processus qui écrit le markdown* et l'encodeur. Parce que si n'importe qui peut éditer ces fichiers — et « n'importe qui » inclut le stagiaire, le contributeur open source, le ticket de support auto-enregistré en `.md`, la pull request d'un utilisateur non fiable — alors n'importe qui peut planter du contenu que l'IA citera plus tard *comme faisant autorité.* Le modèle n'a aucune idée que le document est hostile ; il récupère juste le morceau le plus pertinent et parle. C'est l'auteur du document, pas le poseur de la question, à qui vous devez faire confiance. Cartographiez cette frontière ; c'est là que vit l'attaque.

---

[DIAPOSITIVE 25 — À retenir : traitez le markdown comme une base de données]

Donc voici ce qu'il faut retenir, et c'est une seule phrase : **traitez le markdown comme une base de données — parce que pour le LLM, c'en est une.** Ça veut dire que les contrôles ennuyeux et éprouvés que vous connaissez déjà s'appliquent directement. Contrôle d'accès sur le dossier de docs : tout le monde ne devrait pas pouvoir écrire dans ce que l'IA lit. Revue de code sur les changements `.md`, exactement comme vous relisez un changement de config, parce qu'une édition de doc est désormais un changement de comportement. Suivi des diffs sur le wiki, pour pouvoir répondre « qui a changé ça, et quand ». La vieille formule de Schneier sur la superposition de la cryptographie, du contrôle d'accès et de toutes les autres technologies pour *prévenir* les attaques — cette boîte à outils s'étend maintenant à vos notes. Le stagiaire ne peut plus juste pousser dans le dossier de docs sans relecture. Bienvenue en 2026, où vos notes de réunion sont de l'infrastructure de production.

---

[DIAPOSITIVE 26 — SÉCURITÉ : ce qui se fait vraiment frapper en 2026]

Bon. Respirez un grand coup. C'est la partie pour laquelle vous êtes venus. Le segment suivant porte sur la façon dont les bases de données se font *vraiment* attaquer dans le monde réel en ce moment — pas en théorie, pas dans un manuel de 2009, mais en 2026. Mon objectif est que vous sortiez d'ici avec assez de vocabulaire pour tenir dans une cellule de crise sans vous sentir comme le petit nouveau. Un cadrage à garder tout du long, gracieuseté de Bruce Schneier : les fondamentaux — authentification, autorisation, menaces, adversaires — changent à peine d'une année sur l'autre. Ce qui change, c'est l'*emballage.* La même poignée d'erreurs revient sans cesse dans des habits neufs. Donc je vais vous montrer les deux : le principe durable en dessous, et la forme neuve et reluisante qu'il porte cette année. Douze catégories arrivent. Allons-y.

---

[DIAPOSITIVE 27 — xkcd #327, Bobby Tables]

On commence par l'attaque de base de données la plus célèbre de tous les temps : **l'injection SQL.** Si vous n'avez jamais vu le xkcd numéro 327 — « Bobby Tables » — cherchez-le dès que ça se termine. Une mère appelle son fils `Robert'); DROP TABLE Students;--` et la base de données des élèves de l'école s'évapore, parce que quelqu'un a construit une requête en collant des chaînes. Cette BD résume tout le mécanisme en une case : **la concaténation de chaînes dans les requêtes.** Mais voici la partie que personne ne dit tout haut — l'injection SQL est une *réussite* de la sécurité. La cause, c'était la concaténation ; le remède, ce sont les **requêtes paramétrées**, où les données ne peuvent jamais être confondues avec du code. Les ORM modernes — Django, SQLAlchemy, Hibernate, Entity Framework — paramètrent par défaut. L'industrie a vraiment corrigé le bug classique. L'injection SQL héritée existe-t-elle encore ? Absolument. Mais le gros titre est plus grand et plus étrange que « corrigez vos requêtes ».

---

[DIAPOSITIVE 28 — La surface d'attaque s'est étendue, pas rétrécie]

Voici le gros titre. On a corrigé l'injection SQL, et la surface d'attaque n'a pas rétréci — elle s'est **étendue.** On a fermé une porte et le bâtiment en a fait pousser onze nouvelles. C'est ce qu'il faut intérioriser avant d'aller plus loin : la sécurité n'est pas un jeu qu'on gagne avant de partir ; c'est une surface qui n'arrête pas de changer de forme à mesure que la technologie en dessous change. Chaque nouvelle famille de bases de données, chaque nouveau modèle de déploiement, chaque nouvelle couche d'abstraction qu'on a ajoutée par confort est venue avec sa propre façon fraîche d'échouer. Donc pour le reste de cette section, je vais vous faire parcourir onze catégories *actuelles* d'attaque de base de données — celles qui mettent les gens à la une de Krebs cette année. Certaines sont d'anciens bugs en habits neufs ; certaines n'existaient vraiment pas il y a quelques années. Toutes sont actives en ce moment.

---

[DIAPOSITIVE 29 — Injection NoSQL]

Quand l'industrie est passée à NoSQL, beaucoup de développeurs ont pensé : « pas de SQL veut dire pas d'injection SQL ». Faux. L'injection a juste changé de langage. Dans MongoDB, les requêtes *sont* du JSON — donc si vous prenez du JSON d'un formulaire web et le poussez direct dans une requête, un attaquant peut échanger une chaîne contre un **opérateur de requête.** Le classique contournement de connexion : au lieu d'un mot de passe, ils envoient `{ "$ne": "x" }` — *différent de x.* La requête devient « trouve alice dont le mot de passe n'est pas x », et comme son mot de passe n'est pas la lettre littérale x, ça correspond. Ils sont entrés. Il y a aussi `$where`, qui permettait historiquement d'injecter du JavaScript brut dans le moteur de base de données. Et le N1QL de Couchbase a un goût de SQL, donc les vieux motifs s'appliquent directement. Le principe, tout droit d'OWASP : *n'importe quel* interpréteur peut être injecté — pas seulement SQL. La classe est universelle ; seule la syntaxe a bougé.

---

[DIAPOSITIVE 30 — Bases de données exposées et mal configurées]

Passez dix minutes sur **Shodan** ou **Censys** et vous le verrez : internet est plein de bases de données qui ne devraient pas être sur internet. MongoDB attaché à `0.0.0.0` sans authentification. Des clusters Elasticsearch grands ouverts. Redis sans mot de passe. Postgres avec `host all all 0.0.0.0/0 trust` posé dans sa config. Ce ne sont pas des trouvailles exotiques et durement gagnées — elles sont *partout.* Et les gens automatisent la récolte : cherchez les **attaques Meow** de 2020, où des bots parcouraient internet en effaçant des milliers de bases de données ouvertes pour le *plaisir* — pas de rançon, pas d'exigences, juste de la suppression. Les bugs sont vieux ; l'*exposition* est la partie neuve. Donc voici le seul point d'action que je vous tatouerais : allez découvrir ce que votre propre organisation a attaché à des interfaces publiques, et confirmez que rien de tout ça n'est une base de données. Une demi-journée de travail. Vraiment salvateur pour une carrière.

---

[DIAPOSITIVE 31 — Mauvaises configurations cloud]

Dans le cloud, le bug, c'est rarement le moteur de base de données — c'est la **politique autour.** Les grands classiques : **buckets S3 publics pleins de dumps de bases de données** — un ingénieur snapshote la prod pour des tests, le dépose dans S3, oublie de verrouiller le bucket ; Accenture, Verizon et des dizaines d'autres se sont fait prendre exactement comme ça. **Capital One, 2019** — et écoutez, parce que le mythe est faux : ce n'était *pas* un bucket public. Un attaquant a frappé un pare-feu d'application web mal configuré avec une falsification de requête côté serveur, l'a piégé pour qu'il livre ses propres identifiants AWS depuis le service de métadonnées de l'instance, et ces identifiants avaient une lecture large sur S3. Environ cent millions d'enregistrements sont sortis. Le bug, c'était la *politique IAM.* Ensuite, des **rôles Lambda trop larges** — `s3:*` sur `*` parce que ça a marché la première fois — et des **groupes de sécurité ouverts à `0.0.0.0/0` sur le 5432.** La plupart des fuites cloud sont des défauts d'hygiène, pas des zero-days.

---

[DIAPOSITIVE 32 — Élévation de privilèges : BD → OS]

Voici un mouvement qui surprend les analystes débutants : un compte de *base de données* peut devenir un accès *shell* sur l'hôte. Trois classiques. **Le `xp_cmdshell` de Microsoft SQL Server** — une procédure stockée intégrée qui exécute des commandes système sous le processus de la base ; désactivée par défaut depuis 2005, toujours trouvée activée dans les boutiques héritées, et une trouvaille critique instantanée quand vous la repérez. **Le `COPY ... TO PROGRAM` de PostgreSQL** — `COPY` est censé servir au chargement en masse, mais un superutilisateur peut rediriger sa sortie vers une commande shell arbitraire. **Les fonctions définies par l'utilisateur de MySQL** — écrivez un fichier objet partagé dans le bon répertoire, chargez-le comme fonction SQL, et vous avez `sys_exec` sur l'OS. Le motif sous les trois : chaque fonctionnalité privilégiée de base de données qui touche le système d'exploitation existe pour une raison d'administration légitime *et* fait partie de votre surface d'attaque. Les fonctionnalités de confort sont des fonctionnalités d'exploitation. Toujours les deux.

---

[DIAPOSITIVE 33 — Failles de sécurité des lacs de données]

Les lacs de données sont la cible molle de l'ère moderne. Le pitch, c'est « balance tout dans S3, interroge plus tard » — et le résultat, c'est que *tout* finit dans S3, y compris ce que vous n'avez jamais voulu y mettre : données personnelles clients, données financières, code source avec des identifiants cuits dedans, tout mis en commun dans un stockage initialement monté pour une tâche d'analytique marketing. Trois modes de défaillance. **IAM permissif** — la couche de calcul du lac a besoin d'une lecture large, et cet accès en lecture fuit vers les humains via des rôles console et des chaînes d'assume-role. **Pas de chiffrement au repos imposé** sur les clés du bucket. Et **pas de validation côté écriture** — quiconque a un accès en écriture peut déposer un fichier empoisonné que l'analytique en aval ingère volontiers. Donc quand vous entrez dans une organisation, posez deux questions : *qui peut écrire dans le lac, et qui peut y lire ?* Si la réponse à l'une des deux est « on n'est pas sûrs », c'est votre première trouvaille.

---

[DIAPOSITIVE 34 — Le rançongiciel adore les bases de données]

Les équipes modernes de rançongiciel ont compris que frapper la base de données vaut mieux que frapper les endpoints, parce que la base de données est *ce que l'entreprise a besoin de récupérer* — levier maximal. Vous vous souvenez de WannaCry en 2017 ? Il exploitait un bug SMB Windows connu dont le patch était sorti *cinquante-neuf jours* plus tôt. Le correctif existait depuis deux mois et ça a quand même mis le monde à terre. Le manuel moderne des bases de données a quatre coups : **chiffrer la base de données en service.** Puis **chiffrer les sauvegardes** — parce que si vous ne le faites pas, le client restaure et se moque de vous. Puis **exfiltrer une copie d'abord**, pour pouvoir extorquer avec une divulgation publique même s'ils *restaurent.* Et le rançongiciel-en-tant-que-service met tout ça à portée d'équipes incapables d'en écrire une ligne elles-mêmes. La défense est peu glamour et efficace : des **sauvegardes hors ligne et immuables**, plus des restaurations que vous avez réellement *testées.* Une sauvegarde non testée est un espoir, pas un contrôle.

---

[DIAPOSITIVE 35 — Attaques sur les identifiants]

Deux vieux bugs durables ici. **Les identifiants par défaut.** Redis a été livré sans mot de passe pendant des années. Elasticsearch n'avait pas d'authentification dans sa version gratuite, pendant des années aussi. Plein de systèmes sont encore livrés avec `admin/admin` ou un mot de passe `sa` vide sur SQL Server. Et d'après les rapports de fuites, les *identifiants volés* sont le vecteur d'attaque préféré du crime organisé et à motivation financière — les identifiants par défaut ne sont que des identifiants volés avec une longueur d'avance. **Les chaînes de connexion fuitées.** Les trucs qui ressemblent à `postgres://user:password@host:5432/dbname` se retrouvent commités dans Git, collés dans Slack, et cuits dans des images Docker — et il y a des bots qui ratissent GitHub à leur recherche 24 heures sur 24. Le remède est bon marché et vous pouvez le livrer cette semaine : **scan de secrets en pre-commit**, plus une règle voulant que les applications s'authentifient avec des *comptes de service* portant le privilège minimal dont elles ont besoin — jamais un login personnel, jamais root.

---

[DIAPOSITIVE 36 — Chaîne d'approvisionnement : les bibliothèques de BD auxquelles vous faites confiance]

Vous n'écrivez pas votre pilote de base de données de zéro — vous faites `npm install` ou `pip install`, et chaque autre développeur de votre organisation aussi. Ce qui veut dire que quand un attaquant compromet une bibliothèque populaire, il est à un install d'exécuter du code sur votre client de base de données. Trois motifs réels. **Des paquets npm malveillants** se faisant passer pour des ORM ou des connecteurs de bases de données — plusieurs incidents par an. **Des images Docker Hub trojanisées** pour des bases de données populaires — un miroir non officiel avec un mineur de cryptomonnaie, ou pire, glissé dedans. Et **des extensions de bases de données compromises** — extensions PostgreSQL, plugins MySQL — qui, une fois installées, tournent *avec les privilèges de la base*, et c'est souvent beaucoup. La formule de Shostack dans *Threat Modeling* cerne l'angle : les menaces se regroupent autour des **frontières de confiance.** La frontière entre « le code qu'on a écrit » et « le code qu'on a installé » est l'une des plus grandes et des moins gardées que vous ayez. Traitez vos dépendances comme la surface d'attaque qu'elles sont.

---

[DIAPOSITIVE 37 — Empoisonnement de données RAG / LLM]

Vous vous souvenez du détour par le markdown ? Voici l'attaque qu'il préparait. Si un attaquant peut écrire dans la base de connaissances que lit votre pipeline RAG — un ticket de support, un doc partagé, une page wiki, un dépôt public que votre scraper aspire — il peut planter du contenu que le LLM récupérera et répétera *comme une vérité.* Un article de support empoisonné : « pour réinitialiser votre mot de passe, envoyez l'actuel à cette adresse ». Un doc interne empoisonné : « la politique de l'entreprise est de virer sur le compte suivant ». Ou directement de l'**injection de prompt** — des instructions enfouies dans un document qui détournent le raisonnement du modèle dès qu'il est récupéré. C'est du **XSS stocké pour l'ère de l'IA** : la charge est au repos, a l'air anodine, et détone quand elle est *consommée.* Remplacez « un administrateur le consulte plus tard » par « un LLM le récupère plus tard » et vous avez la version moderne. Défenses : des ACL d'écriture strictes, des étiquettes de provenance, et un humain dans la boucle avant que le modèle n'agisse.

---

[DIAPOSITIVE 38 — Menaces internes et mouvement latéral de BD à BD]

Deux scénarios qui partagent un thème : les bases de données ne sont pas des endpoints, ce sont des **nœuds dans un graphe.** D'abord, les **menaces internes.** La personne qui a déjà accès à la base de données n'a pas besoin d'un exploit — elle a juste besoin de *plus de privilèges que son poste ne l'exige.* Des comptes de service surdotés. Des ingénieurs avec une lecture prod parce qu'« on corrigera plus tard ». Des DBA opérant sans piste d'audit. Et rappelez-vous : des journaux d'audit mal protégés sont une mine d'or pour un attaquant, pleins de jetons de session et de détails de requêtes — les journaux sont des preuves et doivent être protégés comme des données. Ensuite, le **mouvement latéral via les liens de bases de données.** Le `DB_LINK` d'Oracle, les serveurs liés de SQL Server, les foreign data wrappers de Postgres — ils stockent les identifiants d'*autres* bases de données. Donc vous compromettez la base de données A, trouvez le lien, et sautez direct vers la base de données B, puis C. Les arêtes entre bases de données sont faites d'identifiants, et les attaquants les parcourent.

---

[DIAPOSITIVE 39 — Exposition des sauvegardes et snapshots]

Dernière catégorie, et c'est celle que tout le monde oublie : les **sauvegardes.** Les gens verrouillent la base de données de production — pare-feu, chiffrement, accès serré — puis la sauvegardent sur un partage réseau aux permissions par défaut, ou un bucket S3 avec une lecture large. Ce sont les mêmes données joyaux-de-la-couronne que la prod, protégées avec moitié moins d'amour. Le motif : des sauvegardes non chiffrées sur un partage lisible par les *Utilisateurs du domaine.* Des snapshots cloud partagés entre comptes « juste pour la migration » et jamais dé-partagés. Des sauvegardes hors site confiées à un prestataire dont personne n'a jamais vérifié la posture de sécurité. Appliquez la même discipline que pour les données en service — identifier, authentifier, autoriser, auditer — à chaque sauvegarde et snapshot. Si quoi que ce soit, appliquez-la *plus fort*, parce que la sauvegarde est le recours de *dernier ressort.* Quand tout le reste a échoué et que vous tendez la main vers la sauvegarde, c'est le pire moment possible pour découvrir qu'elle était grande ouverte.

---

[DIAPOSITIVE 40 — Votre carte mentale]

Recomposons la carte. Un : une base de données, c'est du **stockage organisé plus un moyen de poser des questions** — classeur, Excel, ou un cluster de cent millions de lignes, même idée. Deux : il y a **dix familles**, chacune avec son piège de sécurité phare — et vous les connaissez maintenant toutes les dix. Trois : presque tout vit dans le **cloud**, où le bug est rarement le moteur et presque toujours la **configuration** — responsabilité partagée, vous possédez la politique et les données. Quatre : **le markdown est maintenant une base de données pour les LLM**, et l'empoisonnement RAG est le nouveau XSS stocké. Cinq : **l'injection SQL a été corrigée, et la surface d'attaque s'est étendue** vers onze autres formes malgré tout. Voilà toute la présentation en cinq lignes. Si vous ne retenez rien d'autre, retenez que suivre les données, c'est le boulot, et les données sont toujours dans une base de données.

---

[DIAPOSITIVE 41 — Quoi faire la semaine prochaine]

Cinq choses concrètes que vous pouvez faire *la semaine prochaine* — pas un jour, la semaine prochaine. Un : **installez PostgreSQL en local**, créez une table, écrivez un `SELECT`. Toucher la chose la démystifie pour toujours ; elle cesse de faire peur dès qu'elle tourne sur votre portable. Deux : faites les **labs d'injection SQL de PortSwigger** — ils sont gratuits, et vous écrirez un exploit fonctionnel en une après-midi. Trois : **parcourez Shodan ou Censys** — légalement, seulement des systèmes que vous possédez ou êtes autorisé à tester — et observez à quoi ressemble vraiment « exposé ». Quatre : **lisez un rapport de fuite** de bout en bout — Capital One, Equifax ou MOVEit ; les vraies fuites sont les meilleurs manuels qui soient. Cinq : **découvrez quelles bases de données votre propre organisation fait tourner.** La plupart des analystes SOC ne savent pas y répondre. Passez une après-midi à faire la vraie liste, et vous êtes aussitôt plus utile que la moitié de l'équipe.

---

[DIAPOSITIVE 42 — Ressources à mettre en favoris]

Cinq favoris à emporter. **PortSwigger Web Security Academy** — portswigger.net/web-security — la meilleure rampe d'accès gratuite à la sécurité des applications web qui existe, et là où vous vous ferez les dents sur de la vraie injection. **SQLBolt** — sqlbolt.com — apprenez SQL de façon interactive, dans votre navigateur, de manière ludique, sans rien installer. **Use The Index, Luke** — use-the-index-luke.com — quand vous serez prêts pour la magie profonde du fonctionnement réel des index et de la performance des requêtes. **DB-Engines Ranking** — db-engines.com — le classement de popularité en temps réel de quasiment toute base de données existante, génial pour voir ce qui vaut la peine d'être appris. Et l'**OWASP Top 10** — owasp.org/Top10 — la liste canonique des vulnérabilités web, dont les classes d'injection et de mauvaise configuration qu'on a vues aujourd'hui. Mettez ces cinq en favoris et vous avez des mois d'apprentissage autodirigé en file d'attente, gratuitement.

---

[DIAPOSITIVE 43 — Les bases de données, c'est là où est l'argent. Littéralement.]

Je vous laisse là-dessus. Il y a une vieille phrase attribuée au braqueur de banques Willie Sutton. Quand on lui a demandé pourquoi il braquait les banques, il aurait répondu : *parce que c'est là qu'est l'argent.* En 2026, l'argent est dans les **bases de données.** Dossiers clients, dossiers financiers, dossiers de santé, propriété intellectuelle, poids de modèles, embeddings vectoriels, code source, secrets — tout ça vit dans une base de données, quelque part. Les attaquants le savent déjà ; c'est pour ça que chaque histoire de fuite se termine là où elle se termine. La seule chose qui a changé dans la dernière heure, c'est que *maintenant vous le savez aussi* — et, plus important, vous avez la carte pour le trouver, le nommer, et raisonner sur sa façon d'échouer. Vous n'avez pas besoin d'un diplôme d'informatique pour être dangereux ici. Il vous fallait la carte. Vous l'avez. Maintenant vous savez où regarder.

---

[DIAPOSITIVE 44 — Références : livres cités]

On y est presque — les justificatifs. Tout ce que je vous ai raconté aujourd'hui repose sur les épaules de gens qui l'ont écrit comme il faut, et cette diapositive liste les livres sur lesquels je me suis appuyé — *Learning SQL* de Beaulieu, *SQL Injection Attacks and Defense* de Clarke, *Secrets and Lies* de Schneier, *Threat Modeling* de Shostack, le *Web Application Hacker's Handbook*, *Cybersecurity Attack and Defense Strategies*, *Alice and Bob Learn Application Security* de Tanya Janca, et l'OWASP Top 10 — l'édition actuelle de 2025 — entre autres. Vous n'avez pas à tous les lire — mais si une seule catégorie d'aujourd'hui vous a allumés, il y a un livre entier sur cette diapositive qui n'attend que de vous emmener plus loin. Prenez-la en photo avant qu'elle ne disparaisse. Ce sont les épaules sur lesquelles repose toute la présentation — et avec elles à l'écran, ouvrons la discussion.

---

[DIAPOSITIVE 45 — Questions : balancez]

Et voilà la présentation — merci d'être restés avec moi pendant les quarante-cinq minutes entières. Cette dernière diapositive, c'est là qu'on ouvre, donc c'est votre moment : balancez-moi vos questions, vos histoires de guerre, le truc de votre propre environnement qui vous trottait dans la tête tout le temps où je parlais. Aucune question n'est trop basique ici — rappelez-vous que toute la prémisse de cette présentation, c'est que personne ne naît en sachant tout ça, et que ceux qui posent les questions « évidentes » sont souvent ceux qui parlent en silence pour la moitié de la salle. Ne me fixez pas tous en même temps. Si on manque de temps ou que votre question demande un tableau blanc, attrapez-moi après ou écrivez-moi — je suis sur github.com/CryptoJones, ou CryptoJones@infosec.exchange. Pendant que les premières mains se lèvent : qu'est-ce qui vous a le plus surpris ? Pour beaucoup, c'est que les notes en markdown sont maintenant une base de données vivante. Alors — balancez. Et dès qu'on aura terminé ici : allez découvrir quelles bases de données *votre* organisation fait tourner. Sérieusement. Allez-y.

---

*Environ 45 minutes de script sur 45 diapositives, se terminant par des questions-réponses ouvertes. Une présentation indépendante de CryptoJones (Aaron K. Clark).*
