# Bases de datos para hackers — Guion del ponente (un minuto por diapositiva)

**Ponente:** Aaron K. Clark
**Formato:** 45 diapositivas × ~1 minuto ≈ 45 minutos, y después preguntas
**Público:** Analistas de seguridad noveles, SOC de nivel inicial, pentesters principiantes, perfiles GRC que se pasan a lo técnico
**Tono:** Conversacional. Un amigo listo en un bar. Nunca condescendiente.

> **Notas de ritmo:** Cada bloque de abajo tiene ~130-150 palabras = alrededor de un minuto a un ritmo relajado de 140 palabras por minuto.
> En el vídeo que acompaña, un suave tono marca cada cambio de diapositiva: cuando lo oigas, avanza.
> `[CORCHETES]` = rellena tus propios datos antes de presentar.

---

[DIAPOSITIVA 1 — Título: "Bases de datos para hackers" — Charla independiente de CryptoJones / No hace falta una carrera en informática]

Muy bien, bienvenidos. Buscad sitio, coged el café. El título lo dice todo: *Bases de datos para hackers*, y el único requisito es la línea de debajo: *no* necesitas una carrera en informática para estar en esta sala. Si has traído un cuaderno, ábrelo. Si no, tranquilo: hay diapositivas, hay un guion escrito y hay grabación. No voy a obligaros a memorizar nada. Todo el objetivo de los próximos cuarenta y cinco minutos es daros un *mapa mental*: ese que te permite entrar en cualquier informe de brecha, cualquier encargo de pentesting, cualquier alerta de SOC, y saber al instante qué estás mirando. Hoy no vamos a construir bases de datos. Vamos a aprender a leerlas, a atacarlas y a defenderlas. Vamos allá.

---

[DIAPOSITIVA 2 — Sobre mí: Aaron K. Clark]

Una palabra rápida sobre mí y nos lanzamos. Soy Aaron Clark — aunque en internet me encontraréis sobre todo como CryptoJones. Soy estudiante de posgrado en la Eastern University, que es una forma elegante de decir que estoy sin un duro, sobrecafeinado, y que tuve que aprender todo esto a las malas, sin una carrera de informática en la que apoyarme. Nadie patrocina esta charla. La doy porque es la charla que ojalá alguien me hubiera dado a *mí* hace un par de años, cuando toda conversación sobre bases de datos en seguridad parecía dar por sentado que llevaba escribiendo SQL desde los doce años. Llegué a la seguridad por el camino largo, sin una formación en informática, y tuve que desentrañar la parte de bases de datos por mi cuenta. Si eres tú — si el mundo de las bases de datos te parece un club privado cuya contraseña nunca te dieron — eres exactamente para quien hice esto.

---

[DIAPOSITIVA 3 — "Toda brecha de la que hayas leído termina en una base de datos."]

Aquí está la única frase que quiero que te lleves de toda la charla. *Toda brecha de la que hayas leído termina en una base de datos.* Equifax, 2017 — los datos de ciento cuarenta y siete millones de personas — vivían en una base de datos. Capital One, 2019 — cien millones de solicitudes de crédito — base de datos. MOVEit, 2023 — el fallo de transferencia de archivos que se convirtió en una catástrofe de cadena de suministro en toda la lista Fortune 500 — cada una de esas organizaciones perdía datos desde una base de datos. SolarWinds, T-Mobile, LinkedIn, OPM, Marriott. Podría llenar los cuarenta y cinco minutos solo con nombres. Cambian los titulares, cambian las empresas, cambian las notas de prensa. El destino nunca cambia. Así que si las bases de datos son donde *termina* cada historia, aprender a pensar en ellas es cómo aprendes a leer la historia entera.

---

[DIAPOSITIVA 4 — Las joyas de la corona: no tu aplicación, no tu cortafuegos, sino los datos]

Fíjate en lo que de verdad quieren los atacantes. No tu preciosa aplicación de página única. No tu diagrama de microservicios. No tu cortafuegos — salvo como algo que superar. Quieren los *datos*. Las joyas de la corona. Lo que se convierte en dinero, o en ventaja, o en un titular con el nombre de tu empresa. Todo lo demás en tu pila — los balanceadores de carga, los contenedores, la malla de servicios — no es más que el envoltorio de lo que está en la cámara acorazada. Y lo que está en la cámara es una base de datos. Así que cuando tries una alerta o defines el alcance de un encargo, entrénate para hacerte pronto una pregunta: *¿dónde viven los datos y qué hay entre el atacante y ellos?* Ese instinto — seguir el camino hasta los datos — es casi todo lo que separa a un analista senior de uno novel.

---

[DIAPOSITIVA 5 — ¿Qué es una base de datos? Almacenamiento organizado + una forma de hacer preguntas]

Quitémosle la jerga. Una base de datos son dos cosas grapadas juntas: *almacenamiento organizado*, más *una forma de hacer preguntas*. Ese es el concepto entero. Todo lo demás son detalles. ¿Has usado alguna vez un archivador — carpetas de papel, por orden alfabético de apellido? Has usado una base de datos. El archivador es el almacenamiento; tus ojos son el motor de consultas. ¿Has pulsado Ctrl-F en Excel para encontrar una fila? Base de datos. La hoja de cálculo es el almacenamiento; buscar y reemplazar es la consulta. Lo que una base de datos *de verdad* añade encima es escala, velocidad, concurrencia — mucha gente accediendo a la vez — y un lenguaje formal para preguntar en lugar de usar los ojos. Eso es todo. Es un archivador que nunca se cansa, que mil personas pueden abrir a la vez, y al que le hablas en un lenguaje estructurado. Quédate con esa imagen; todo lo demás cuelga de ella.

---

[DIAPOSITIVA 6 — Las seis palabras que necesitas + CRUD]

Aquí tienes todo el vocabulario que necesitas para mantener una conversación de verdad con un administrador de bases de datos. Seis palabras. Una **tabla** es una pestaña de hoja de cálculo — clientes, pedidos, eventos de inicio de sesión. Una **fila** es un registro — un cliente, una alerta. Una **columna** es un atributo — correo, IP de origen, total. Una **consulta** es la pregunta que haces: "muéstrame cada inicio de sesión desde fuera del país en la última hora". Un **esquema** es la *forma* de los datos — las columnas, sus tipos, las reglas; y el hueco entre "esta columna guarda correos" y "esta columna guarda lo que sea que la aplicación echó ahí" es exactamente donde viven las vulnerabilidades. Un **índice** es un marcador que hace las búsquedas instantáneas — y también cómo los atacantes cronometran la inyección a ciegas. Añade **CRUD** — Crear, Leer, Actualizar, Borrar — los cuatro verbos que hace toda base de datos. Domina estas seis y ya tienes soltura.

---

[DIAPOSITIVA 7 — Recorrido histórico: fósiles que verás en producción]

Recorrido histórico rápido — no porque me encante la historia, sino porque cada cosa rara de un entorno real es un *fósil* de una de estas eras. **Años 60, archivos planos:** datos en un fichero; los permisos eran el único control de acceso. **Finales de los 60, jerárquico** (el IMS de IBM): datos en un árbol, modelo de amenaza de mainframe — acceso físico. **Años 70, red/CODASYL:** registros enlazados por punteros; todavía zumbando en la trastienda de tu banco. **1970, el modelo relacional de Codd:** tablas y matemáticas — y control de acceso *dentro* de la base de datos, permisos y roles. **Años 80:** Oracle, DB2, SQL Server — las bases de datos se conectan en red, así que ahora hay un problema de autenticación. **Años 90, cliente-servidor y código abierto:** cada formulario web se vuelve una puerta — nace la inyección SQL. **Años 2000, NoSQL:** la escala como religión. **Años 2010, la nube:** responsabilidad compartida. **Años 2020, vectorial y serverless:** envenenamiento de datos e inyección de prompts. Identifica la era, predice el fallo.

---

[DIAPOSITIVA 8 — Diez familias de bases de datos]

Hay diez familias de bases de datos que te encontrarás en la naturaleza, y voy a darte las mismas cuatro cosas de cada una: qué almacena, cuándo la usarías, un par de productos reales, y *un* problema de seguridad. Relacional, documental, clave-valor, columnar, grafo, búsqueda, series temporales, vectorial, embebida, y lago de datos. Toma notas de los problemas de seguridad en concreto — esas son las líneas que aparecen en preguntas de entrevista y en encargos. No intentes memorizar los nombres de los productos; esos los absorberás por exposición. Lo que quiero que se te quede es la *forma* de cada familia, porque la forma te dice el ataque. Una tabla rígida falla de forma distinta a un documento JSON laxo, que falla de forma distinta a un gigantesco bucket en la nube. Diez formas, diez modos de fallo. Allá vamos — una por minuto.

---

[DIAPOSITIVA 9 — 1. Relacional / SQL]

Número uno, relacional — SQL. Filas y columnas, un esquema fuerte, y SQL como lenguaje de consulta. Productos: **PostgreSQL, MySQL/MariaDB, SQL Server, Oracle.** Úsala cuando tus datos tienen relaciones claras y de verdad te importa la consistencia — cualquier cosa financiera, cualquier cosa regulada. Este es el caballo de batalla de toda la industria; en la duda, los datos están aquí. Problema de seguridad — el famoso: **inyección SQL**, que ocurre cuando los desarrolladores construyen consultas pegando la entrada del usuario directamente en una cadena de texto. Le vamos a dedicar tiempo de verdad más adelante, así que de momento archívalo. Beaulieu, en *Learning SQL*, defiende por qué esta familia no va a morir: una base de datos relacional bien diseñada puede manejar cantidades enormes de datos manteniéndolos consistentes. Aburrida, fiable, en todas partes — y todavía el sitio número uno donde los principiantes encuentran bugs reales.

---

[DIAPOSITIVA 10 — 2. Almacenes de documentos]

Número dos, almacenes de documentos. En lugar de filas rígidas, guardan **documentos JSON**, y cada documento puede tener un aspecto un poco distinto — esquema flexible. Productos: **MongoDB, Couchbase, Firestore.** Úsala cuando tus datos son naturalmente anidados y su forma cambia con el tiempo — catálogos de productos, perfiles de usuario, contenido. Es la familia que impulsó buena parte de la era web del "muévete rápido". Problema de seguridad — **inyección NoSQL** a través de operadores de consulta como `$ne`, `$gt` y `$where`; la inyección no desapareció cuando se fue SQL, solo cambió de idioma, y la explotaremos más adelante. El otro clásico: durante años la instalación por defecto se ataba a todas las interfaces *sin autenticación*, que es exactamente cómo Shodan acabó lleno de MongoDB abiertos. Datos flexibles, ajustes de seguridad flexibles — a veces *ausentes*.

---

[DIAPOSITIVA 11 — 3. Almacenes clave-valor]

Número tres, clave-valor — la base de datos más simple que existe. Es un diccionario gigante: metes una clave, sacas un valor, nada más sofisticado. Productos: **Redis, Memcached, DynamoDB.** Úsala para cachés, almacenes de sesión, limitadores de tasa, tablas de clasificación — cualquier cosa donde necesites una velocidad brutal y una búsqueda simple. Redis en particular está en todas partes en las pilas web modernas, justo detrás de la aplicación. Problema de seguridad — durante años Redis venía **sin contraseña por defecto**, y su comando `CONFIG SET` históricamente permitía a un atacante escribir archivos — como una clave SSH — directamente en el disco del host de la base de datos. Así que un Redis abierto en un pentest no es solo un hallazgo; con frecuencia es un *punto de apoyo* — una forma de entrar en la propia máquina. Diseño que prioriza la velocidad, ajustes que ponen la seguridad en segundo lugar. Fíjate en que ese patrón se repite por todas estas familias.

---

[DIAPOSITIVA 12 — 4. Columnar]

Número cuatro, columnar — a veces llamada de columna ancha. Construida para escala *masiva* repartida entre muchas máquinas. Productos: **Apache Cassandra, HBase, ScyllaDB.** Úsala cuando tienes tantos datos que ninguna máquina sola puede contenerlos y no necesitas joins complejos — piensa en Netflix, Apple e Instagram, todos corriendo sobre Cassandra. El trato que haces por esa escala son las comodidades relacionales; diseñas en torno a tus consultas de antemano. Problema de seguridad — los nodos de estos clústeres normalmente *confían entre sí de forma implícita* en el puerto del protocolo de gossip. Traducción: meterse en la red de gestión del clúster suele equivaler a tener root sobre todo el conjunto de datos. Así que cuando defines el alcance de uno de estos, la pregunta interesante no es la puerta principal — es si la red interna del clúster está segmentada de todo lo demás. Normalmente no lo está.

---

[DIAPOSITIVA 13 — 5. Bases de datos de grafos]

Número cinco, bases de datos de grafos. Aquí los datos *son* las relaciones — nodos y aristas, no filas. Productos: **Neo4j, Amazon Neptune, ArangoDB.** Úsala para redes sociales, detección de fraude y — atención, gente de seguridad — **análisis de identidad y accesos.** Si nunca has jugado con **BloodHound**, la herramienta de rutas de ataque en Active Directory, hazlo este fin de semana; es literalmente una base de datos de grafos que te muestra "quién puede convertirse en administrador de dominio, y cómo". Problema de seguridad — lenguajes de consulta de grafos como **Cypher también son inyectables.** Quiero matar un mito aquí mismo: la inyección NoSQL *no* es un problema exclusivo de MongoDB. Cada vez que una entrada no confiable se concatena en un lenguaje de consulta — cualquier lenguaje de consulta — tienes una clase de inyección. Las bases de datos de grafos son un precioso recordatorio de que el principio es universal, no atado a SQL.

---

[DIAPOSITIVA 14 — 6. Motores de búsqueda]

Número seis, motores de búsqueda — construidos para consultas rápidas de texto completo sobre montañas enormes de texto. Productos: **Elasticsearch, OpenSearch, Solr.** Úsalos para búsqueda de logs, búsqueda en sitios de comercio electrónico y — esto te importa — la **columna vertebral de la mayoría de los SIEM.** Tu SOC muy probablemente busca cada día en un clúster de Elasticsearch u OpenSearch, aunque nunca lo veas directamente. Problema de seguridad — históricamente venían **sin autenticación integrada** en la versión gratuita, y los clústeres expuestos a internet con *miles de millones* de registros han sido una noticia recurrente durante una década entera. Junta ese hecho con Shodan y tienes un proyecto de investigación de fin de semana — *en sistemas que poseas o estés autorizado a probar*, y solo esos. La herramienta que impulsa tu pila de detección es, irónicamente, una de las familias de bases de datos más expuestas de internet.

---

[DIAPOSITIVA 15 — 7. Series temporales]

Número siete, bases de datos de series temporales — optimizadas para una sola cosa: muchísimos puntos de datos indexados por tiempo. Productos: **InfluxDB, TimescaleDB, Prometheus.** Úsalas para métricas, paneles de observabilidad, telemetría de IoT y sensores — cualquier cosa que sea básicamente "un número, cada segundo, para siempre". Si tu organización tiene un muro de paneles de Grafana, hay una de estas debajo. Problema de seguridad — casi siempre viven *dentro del perímetro* y *muchas veces sin autenticación*, porque la suposición es "solo nuestros propios servicios le hablan". Así que un atacante que aterriza dentro de la red puede leer cada gráfica de CPU, memoria y tráfico que tienes — lo cual le dice en voz baja qué máquinas hacen el trabajo *interesante*, dónde está la base de datos ocupada, cuándo corre la copia de seguridad. Es oro para el reconocimiento, abierto de par en par, porque nadie piensa en las métricas como algo sensible.

---

[DIAPOSITIVA 16 — 8. Bases de datos vectoriales]

Número ocho, bases de datos vectoriales — las de la IA, y la familia más nueva de la lista. Almacenan **embeddings**: largas listas de números que capturan el *significado* de un fragmento de texto o de una imagen, para que puedas buscar por similitud en lugar de por coincidencia exacta. Productos: **Pinecone, Milvus, Weaviate** y **pgvector**, la extensión que permite a un PostgreSQL normal jugar a este juego. Úsalas para generación aumentada por recuperación, motores de recomendación y búsqueda semántica. Problema de seguridad — **envenenamiento de datos.** Si un atacante consigue colar un documento malicioso en tu almacén vectorial, el modelo de lenguaje que se sienta encima lo recuperará encantado y se lo citará a tus usuarios *como si fuera verdad.* Esa es una superficie de ataque totalmente nueva que hace cinco años apenas existía, y vamos a volver a ella al final, porque es donde muchos de vosotros acabaréis trabajando.

---

[DIAPOSITIVA 17 — 9. Embebida / Edge]

Número nueve, bases de datos embebidas y de borde. Aquí la base de datos vive *dentro de la aplicación* — es un archivo en disco, no un servidor al que te conectas por la red. Productos: **SQLite, DuckDB, LevelDB.** SQLite por sí sola es la base de datos más desplegada de la Tierra: está en tu navegador, en tu teléfono, en tu coche, y básicamente en cada avión construido en los últimos veinte años. Úsala para almacenamiento local dentro de la aplicación, donde levantar un servidor sería una exageración. Problema de seguridad — cuando la base de datos es solo un *archivo*, todo el ataque se reduce a "roba el archivo". Sin exploit de red, sin inyección — copia el archivo del dispositivo y léelo con calma. Esta es la realidad diaria de los pentesters de móvil: la mitad del encargo es encontrar el archivo SQLite que una aplicación dejó tirado con datos sensibles dentro, sin cifrar.

---

[DIAPOSITIVA 18 — 10. Lagos de datos / Lakehouses]

Número diez, lagos de datos y lakehouses. En lugar de estructurar los datos al *entrar*, lo viertes todo en almacenamiento de objetos barato y lo estructuras al *salir*. Productos: **S3 + Athena, Delta Lake, Apache Iceberg, Snowflake.** La jerga es **esquema en lectura** frente a **esquema en escritura** — la vieja relacional se comprometía con la forma de antemano; los lagos se comprometen después, en el momento de la consulta. Úsalos cuando quieres acumular ahora y decidir qué significa después. Problema de seguridad — pozos gigantes de datos en S3 con IAM demasiado amplio, sin cifrado en reposo obligatorio, y sin auditoría de quién leyó qué. Es el equivalente moderno a dejar el archivador sin llave — salvo que el archivador es ahora del tamaño de un edificio, y nadie está del todo seguro de todo lo que se echó dentro. Volveremos a los fallos específicos de los lagos en la sección de seguridad.

---

[DIAPOSITIVA 19 — Servicios de bases de datos en la nube: el panorama]

Entra en cualquier entorno construido en los últimos cinco años y las bases de datos no viven en una sala de servidores — viven en una cuenta de la nube. Así que necesitas los nombres de los proveedores, porque así es como estas cosas aparecen en alertas, en políticas IAM, en tickets de respuesta a incidentes. En **AWS, GCP y Azure** verás las mismas categorías llevando nombres de marca distintos: relacional gestionada, documental/NoSQL, almacén de datos, caché, grafo, series temporales y almacenamiento de objetos. AWS tiene el menú más amplio — RDS, DynamoDB, Redshift, ElastiCache, Neptune, Timestream, S3. GCP se apoya en Cloud SQL, Firestore, Bigtable y la genuinamente preciosa BigQuery. Azure canaliza mucho a través de Azure SQL y **Cosmos DB**, un cambiaformas que habla varios dialectos de bases de datos a la vez. No necesitas memorizar esta cuadrícula — necesitas reconocer los nombres cuando pasen volando en una sala de crisis.

---

[DIAPOSITIVA 20 — Chuleta de bases de datos en la nube]

Aquí está la chuleta en una tabla — hazle una captura a esta diapositiva. **Relacional:** AWS es RDS y Aurora, GCP es Cloud SQL y AlloyDB, Azure es Azure SQL Database. **Documental/NoSQL:** DynamoDB y DocumentDB en AWS, Firestore y Bigtable en GCP, Cosmos DB en Azure. **Almacén de datos:** Redshift y Athena, frente a BigQuery, frente a Synapse. **Caché:** ElastiCache, Memorystore, Azure Cache for Redis. **Grafo:** Neptune en AWS, el modo grafo de Cosmos en Azure, y GCP diciendo eternamente "pronto". **Almacenamiento de objetos:** S3, Cloud Storage, Blob Storage. La razón por la que esto importa para la seguridad: cada uno de estos es una *superficie IAM distinta* con *ajustes por defecto distintos*. El ataque rara vez es el motor — es la política que lo envuelve, y la política vive en la columna de esta tabla donde estés parado. Conoce la columna, sabe dónde mirar.

---

[DIAPOSITIVA 21 — Modelo de responsabilidad compartida]

Esta es la diapositiva más importante de la sección de la nube. El **modelo de responsabilidad compartida.** El proveedor de la nube es dueño de las partes bajo la línea de flotación: el hipervisor, el metal, la seguridad física, y parchear el *motor* de la base de datos en sí. Tú — el cliente — eres dueño de todo lo que hay encima: la **configuración**, las **políticas de acceso** e IAM, los **datos**, y tus **decisiones de cifrado.** La documentación de AWS lo dice sin rodeos — una vez que eres cliente, proteger tus datos en reposo y en tránsito es *tu* parte de la responsabilidad ahora. Tradúcelo a lenguaje de seguridad y se convierte en la frase más útil de toda la seguridad en la nube: **casi toda brecha de base de datos en la nube es una mala configuración del lado del cliente**, no el proveedor siendo hackeado. Bucket público, grupo de seguridad abierto de par en par, snapshot compartido con la cuenta equivocada. El proveedor rara vez falla. *Nosotros* configuramos el fallo.

---

[DIAPOSITIVA 22 — Puertos comunes de bases de datos — grábatelos a fuego]

Memoriza estos siete números de puerto. Los analistas de SOC los usan cada día; los pentesters los escanean cada día. **MySQL, 3306. PostgreSQL, 5432. Microsoft SQL Server, 1433. MongoDB, 27017. Redis, 6379. Elasticsearch, 9200. Cassandra, 9042.** Ese es el conjunto. Aquí está la regla que va con ellos: si alguna vez ves *cualquiera* de estos expuesto directamente a internet, eso es un **hallazgo** — siempre, sin excepciones, repórtalo. Un puerto de base de datos abierto a `0.0.0.0` es el equivalente en la nube a dejar la puerta de la cámara acorazada abierta a la calle. Grupos de seguridad de red, reglas de cortafuegos, listas de seguridad — cada nube lo llama de forma ligeramente distinta, pero el trabajo es idéntico: cierra el puerto que no necesita estar abierto. Si no aprendes ninguna otra cifra hoy, aprende estos siete.

---

[DIAPOSITIVA 23 — Tus notas ahora son una base de datos]

Breve desvío antes del final de seguridad, porque esto estará en tu radar dentro de un año, te guste o no. **Los archivos Markdown ahora son una base de datos** — no como metáfora, literalmente, de las que lee un LLM. Aquí está el patrón. Coges una carpeta de archivos `.md` — un vault de Obsidian, una exportación de wiki, un montón de notas de reuniones, los documentos de GitHub de tu equipo. Los pasas por un *modelo de embeddings* que convierte el texto en vectores, y guardas esos vectores en una base de datos vectorial. Ahora, cuando alguien le hace una pregunta a tu asistente de IA, el sistema busca semánticamente en tus notas, agarra los fragmentos más relevantes y los mete en el prompt del modelo. Tu humilde carpeta de notas acaba de convertirse en la *fuente de verdad* que una IA le repite a tus usuarios. Siéntate a pensar en lo raro — y lo expuesto — que es eso.

---

[DIAPOSITIVA 24 — Pipeline RAG: ¿dónde está la frontera de confianza?]

Ese patrón tiene nombre: **RAG** — generación aumentada por recuperación. Archivos `.md`, a un modelo de embeddings, a una base de datos vectorial, al prompt del LLM, y sale como respuesta. Así funciona casi todo producto de "chatea con tus documentos". Ahora ponte el sombrero de seguridad y encuentra la **frontera de confianza.** Está justo entre *el proceso que escribe el markdown* y el modelo de embeddings. Porque si cualquiera puede editar esos archivos — y "cualquiera" incluye al becario, al colaborador de código abierto, el ticket de soporte que se registra automáticamente como un `.md`, la pull request de un usuario no confiable — entonces cualquiera puede plantar contenido que la IA citará después *como autoritativo.* El modelo no tiene ni idea de que el documento es hostil; solo recupera el fragmento más relevante y habla. Es el escritor del documento, no quien hace la pregunta, en quien tienes que confiar. Mapea esa frontera; ahí es donde vive el ataque.

---

[DIAPOSITIVA 25 — La conclusión: trata el markdown como una base de datos]

Así que aquí está la conclusión, y es una sola frase: **trata el markdown como una base de datos — porque para el LLM, lo es.** Eso significa que los controles aburridos y probados que ya conoces aplican directamente. Control de acceso sobre la carpeta de documentos: no todo el mundo debería poder escribir en aquello que la IA lee. Revisión de código sobre los cambios en `.md`, igual que revisarías un cambio de configuración, porque una edición de documento es ahora un cambio de comportamiento. Seguimiento de diferencias en la wiki, para poder responder "quién cambió esto y cuándo". La vieja frase de Schneier sobre superponer criptografía, control de acceso y todas las demás tecnologías para *prevenir* ataques — ese arsenal se extiende ahora a tus notas. El becario ya no puede simplemente subir a la carpeta de documentos sin revisión. Bienvenido a 2026, donde tus notas de reuniones son infraestructura de producción.

---

[DIAPOSITIVA 26 — SEGURIDAD: qué está siendo golpeado de verdad en 2026]

Vale. Respira hondo. Esta es la parte por la que vinisteis. El siguiente tramo va de cómo las bases de datos *de verdad* son atacadas en el mundo real ahora mismo — no en teoría, no en un libro de texto de 2009, sino en 2026. Mi objetivo es que salgáis de aquí con suficiente vocabulario para estar en una sala de crisis y no sentiros como el novato. Un encuadre para llevar a través de todo, cortesía de Bruce Schneier: los fundamentos — autenticación, autorización, amenazas, adversarios — apenas cambian de un año a otro. Lo que cambia es el *envoltorio.* El mismo puñado de errores sigue volviendo con ropa nueva. Así que voy a mostraros ambas cosas: el principio duradero de debajo, y la forma nueva y reluciente que viste este año. Vienen doce categorías. Vamos a ello.

---

[DIAPOSITIVA 27 — xkcd #327, Bobby Tables]

Empezamos con el ataque a bases de datos más famoso de todos los tiempos: **la inyección SQL.** Si nunca has visto el xkcd número 327 — "Bobby Tables" — búscalo en cuanto esto termine. Una madre llama a su hijo `Robert'); DROP TABLE Students;--` y la base de datos de estudiantes del colegio se esfuma, porque alguien construyó una consulta pegando cadenas de texto. Esa viñeta es el mecanismo entero en un panel: **concatenación de cadenas en consultas.** Pero aquí está la parte que nadie dice en voz alta — la inyección SQL es una *historia de éxito* de la seguridad. La causa era la concatenación; la solución son las **consultas parametrizadas**, donde los datos nunca pueden confundirse con el código. Los ORM modernos — Django, SQLAlchemy, Hibernate, Entity Framework — parametrizan por defecto. La industria arregló de verdad el bug clásico. ¿Sigue existiendo la inyección SQL en sistemas heredados? Por supuesto. Pero el titular es más grande y más raro que "parchea tus consultas".

---

[DIAPOSITIVA 28 — La superficie de ataque se ha expandido, no encogido]

Aquí está el titular. Arreglamos la inyección SQL, y la superficie de ataque no se hizo más pequeña — se **expandió.** Cerramos una puerta y el edificio creó once nuevas. Eso es lo que hay que interiorizar antes de seguir: la seguridad no es un juego que ganas y te marchas; es una superficie que sigue cambiando de forma a medida que cambia la tecnología de debajo. Cada nueva familia de bases de datos, cada nuevo modelo de despliegue, cada nueva capa de abstracción que añadimos por comodidad vino con su propia forma fresca de fallar. Así que durante el resto de esta sección voy a guiaros por once categorías *actuales* de ataque a bases de datos — las que ponen a la gente en la portada de Krebs este año. Algunas son bugs antiguos con ropa nueva; algunas de verdad no existían hace unos años. Todas están activas ahora mismo.

---

[DIAPOSITIVA 29 — Inyección NoSQL]

Cuando la industria se pasó a NoSQL, muchos desarrolladores pensaron: "no SQL significa no inyección SQL". Error. La inyección solo cambió de idioma. En MongoDB, las consultas *son* JSON — así que si coges JSON de un formulario web y lo metes directamente en una consulta, un atacante puede cambiar una cadena por un **operador de consulta.** El clásico bypass de login: en lugar de una contraseña, envían `{ "$ne": "x" }` — *distinto de x.* La consulta se convierte en "encuentra a alice cuya contraseña no sea x", y como su contraseña no es la letra literal x, coincide. Están dentro. También está `$where`, que históricamente permitía inyectar JavaScript en bruto en el motor de la base de datos. Y el N1QL de Couchbase tiene sabor a SQL, así que los viejos patrones aplican directamente. El principio, sacado directo de OWASP: *cualquier* intérprete puede ser inyectado — no solo SQL. La clase es universal; solo se movió la sintaxis.

---

[DIAPOSITIVA 30 — Bases de datos expuestas y mal configuradas]

Pasa diez minutos en **Shodan** o **Censys** y lo verás: internet está lleno de bases de datos que no deberían estar en internet. MongoDB atado a `0.0.0.0` sin autenticación. Clústeres de Elasticsearch abiertos de par en par. Redis sin contraseña. Postgres con `host all all 0.0.0.0/0 trust` puesto en su configuración. No son hallazgos exóticos y difíciles de conseguir — están *por todas partes.* Y la gente automatiza la recolección: busca los **ataques Meow** de 2020, donde los bots recorrían internet borrando miles de bases de datos abiertas por *diversión* — sin rescate, sin exigencias, solo borrado. Los bugs son viejos; la *exposición* es la parte nueva. Así que aquí está el único punto de acción que te tatuaría: averigua qué tiene tu propia organización atado a interfaces públicas, y confirma que nada de ello es una base de datos. Medio día de trabajo. Genuinamente puede salvarte la carrera.

---

[DIAPOSITIVA 31 — Malas configuraciones en la nube]

En la nube, el bug rara vez es el motor de la base de datos — es la **política a su alrededor.** Los grandes éxitos: **buckets S3 públicos llenos de volcados de bases de datos** — un ingeniero hace un snapshot de producción para pruebas, lo deja en S3, se olvida de cerrar el bucket; Accenture, Verizon y docenas más cayeron exactamente así. **Capital One, 2019** — y escucha, porque el mito es erróneo: *no* fue un bucket público. Un atacante golpeó un cortafuegos de aplicaciones web mal configurado con una falsificación de petición del lado del servidor, lo engañó para que entregara sus propias credenciales de AWS desde el servicio de metadatos de la instancia, y esas credenciales tenían lectura amplia sobre S3. Unos cien millones de registros se largaron. El bug fue la *política IAM.* Luego **roles de Lambda demasiado amplios** — `s3:*` sobre `*` porque funcionó la primera vez — y **grupos de seguridad abiertos a `0.0.0.0/0` en el 5432.** La mayoría de las brechas en la nube son fallos de higiene, no días cero.

---

[DIAPOSITIVA 32 — Escalada de privilegios: BD → SO]

Aquí hay un movimiento que sorprende a los analistas noveles: una cuenta de *base de datos* puede convertirse en acceso de *shell* en el host. Tres clásicos. **El `xp_cmdshell` de Microsoft SQL Server** — un procedimiento almacenado integrado que ejecuta comandos del sistema operativo como el proceso de la base de datos; desactivado por defecto desde 2005, todavía encontrado activado en tiendas heredadas, y un hallazgo crítico al instante cuando lo ves. **El `COPY ... TO PROGRAM` de PostgreSQL** — `COPY` está pensado para carga masiva, pero un superusuario puede canalizar su salida a un comando de shell arbitrario. **Las funciones definidas por el usuario de MySQL** — escribe un archivo de objeto compartido en el directorio correcto, cárgalo como una función SQL, y tienes `sys_exec` en el SO. El patrón bajo los tres: cada función privilegiada de base de datos que toca el sistema operativo existe por una razón legítima de administración *y* es parte de tu superficie de ataque. Las funciones de comodidad son funciones de explotación. Siempre ambas.

---

[DIAPOSITIVA 33 — Brechas de seguridad en lagos de datos]

Los lagos de datos son el objetivo blando de la era moderna. La promesa es "vuelca todo en S3, consúltalo después" — y el resultado es que *todo* acaba en S3, incluidas las cosas que nunca pensaste meter ahí: datos personales de clientes, datos financieros, código fuente con credenciales horneadas dentro, todo apozado en un almacenamiento que originalmente se montó para algún trabajo de analítica de marketing. Tres modos de fallo. **IAM permisivo** — la capa de cómputo del lago necesita lectura amplia, y ese acceso de lectura se escapa a los humanos a través de roles de consola y cadenas de assume-role. **Sin cifrado en reposo obligatorio** sobre las claves del bucket. Y **sin validación del lado de la escritura** — cualquiera con acceso de escritura puede dejar caer un archivo envenenado que la analítica de aguas abajo ingiere encantada. Así que cuando entres en una organización, haz dos preguntas: *¿quién puede escribir en el lago, y quién puede leer de él?* Si la respuesta a cualquiera de las dos es "no estamos seguros", ese es tu primer hallazgo.

---

[DIAPOSITIVA 34 — Al ransomware le encantan las bases de datos]

Las bandas modernas de ransomware se dieron cuenta de que golpear la base de datos supera a golpear los endpoints, porque la base de datos es *lo que el negocio necesita recuperar* — máxima ventaja. ¿Recuerdas WannaCry en 2017? Explotó un fallo conocido de SMB de Windows cuyo parche llevaba publicado *cincuenta y nueve días.* La solución existía desde hacía dos meses y aun así tumbó al mundo. El manual moderno de bases de datos tiene cuatro movimientos: **cifrar la base de datos en vivo.** Luego **cifrar las copias de seguridad** — porque si no lo haces, el cliente simplemente restaura y se ríe de ti. Luego **exfiltrar una copia primero**, para poder extorsionar con divulgación pública aunque *sí* restauren. Y el Ransomware como Servicio pone todo eso al alcance de bandas que no sabrían escribir ni una línea de ello. La defensa es poco glamurosa y efectiva: **copias de seguridad offline e inmutables**, más restauraciones que de verdad has *probado.* Una copia de seguridad sin probar es una esperanza, no un control.

---

[DIAPOSITIVA 35 — Ataques de credenciales]

Dos bugs viejos y duraderos aquí. **Credenciales por defecto.** Redis venía sin contraseña durante años. Elasticsearch no tenía autenticación en su versión gratuita, también durante años. Montones de sistemas todavía vienen con `admin/admin` o una contraseña `sa` en blanco en SQL Server. Y según los informes de brechas, las *credenciales robadas* son el vector de ataque preferido del crimen organizado y motivado financieramente — las credenciales por defecto son solo credenciales robadas con ventaja. **Cadenas de conexión filtradas.** Las cosas que tienen pinta de `postgres://user:password@host:5432/dbname` se suben a Git, se pegan en Slack y se hornean en imágenes Docker — y hay bots rastreando GitHub a la caza de ellas las veinticuatro horas. La solución es barata y la puedes desplegar esta semana: **escaneo de secretos en pre-commit**, más una regla de que las aplicaciones se autentiquen con *cuentas de servicio* que tengan el mínimo privilegio que necesitan — nunca un login personal, nunca root.

---

[DIAPOSITIVA 36 — Cadena de suministro: las librerías de BD en las que confías]

No escribes tu driver de base de datos desde cero — haces `npm install` o `pip install`, y lo mismo hace cada otro desarrollador de tu organización. Lo cual significa que cuando un atacante compromete una librería popular, está a una instalación de ejecutar código en tu cliente de base de datos. Tres patrones reales. **Paquetes npm maliciosos** haciéndose pasar por ORM o conectores de bases de datos — varios incidentes al año. **Imágenes troyanizadas de Docker Hub** para bases de datos populares — un mirror no oficial con un minero de criptomonedas, o algo peor, metido dentro. Y **extensiones de bases de datos comprometidas** — extensiones de PostgreSQL, plugins de MySQL — que, una vez instaladas, corren *con privilegios de base de datos*, y eso suele ser mucho. La frase de Shostack en *Threat Modeling* clava el enfoque: las amenazas se agrupan en torno a las **fronteras de confianza.** La frontera entre "código que escribimos" y "código que instalamos" es una de las más grandes y menos vigiladas que tienes. Trata tus dependencias como la superficie de ataque que son.

---

[DIAPOSITIVA 37 — Envenenamiento de datos de RAG / LLM]

¿Recuerdas el desvío del markdown? Aquí está el ataque que estaba preparando. Si un atacante puede escribir en la base de conocimiento de la que lee tu pipeline RAG — un ticket de soporte, un documento compartido, una página de wiki, un repositorio público que tu scraper recoge — puede plantar contenido que el LLM recuperará y repetirá *como verdad.* Un artículo de soporte envenenado: "para restablecer tu contraseña, envía la actual a esta dirección". Un documento interno envenenado: "la política de la empresa es transferir a la siguiente cuenta". O directamente **inyección de prompt** — instrucciones enterradas en un documento que secuestran el razonamiento del modelo en cuanto se recupera. Esto es **XSS almacenado para la era de la IA**: la carga útil está en reposo, parece inocua, y detona cuando se *consume.* Cambia "un administrador lo ve después" por "un LLM lo recupera después" y tienes la versión moderna. Defensas: ACL de escritura estrictas, etiquetas de procedencia, y un humano en el bucle antes de que el modelo actúe.

---

[DIAPOSITIVA 38 — Amenazas internas y movimiento lateral de BD a BD]

Dos escenarios que comparten un tema: las bases de datos no son endpoints, son **nodos en un grafo.** Primero, **amenazas internas.** La persona que ya tiene acceso a la base de datos no necesita un exploit — solo necesita *más privilegio del que su trabajo requiere.* Cuentas de servicio con permisos de más. Ingenieros con lectura de producción porque "lo arreglamos después". Administradores operando sin rastro de auditoría. Y recuerda: los logs de auditoría mal protegidos son una mina de oro para un atacante, llenos de tokens de sesión y detalles de peticiones — los logs son evidencia y hay que protegerlos como datos. Segundo, **movimiento lateral a través de enlaces de bases de datos.** El `DB_LINK` de Oracle, los servidores enlazados de SQL Server, los foreign data wrappers de Postgres — estos guardan credenciales de *otras* bases de datos. Así que comprometes la base de datos A, encuentras el enlace, y saltas directo a la base de datos B, luego a la C. Las aristas entre bases de datos están hechas de credenciales, y los atacantes las recorren.

---

[DIAPOSITIVA 39 — Exposición de copias de seguridad y snapshots]

Última categoría, y es la que todo el mundo olvida: las **copias de seguridad.** La gente blinda la base de datos de producción — cortafuegos, cifrado, acceso restringido — y luego la respalda en un recurso de red con permisos por defecto, o en un bucket S3 con lectura amplia. Son los mismos datos joya-de-la-corona que producción, protegidos con la mitad del cariño. El patrón: copias de seguridad sin cifrar en un recurso legible por *Usuarios del Dominio.* Snapshots en la nube compartidos entre cuentas "solo para la migración" y nunca dejados de compartir. Copias de seguridad externas entregadas a un proveedor cuya postura de seguridad nadie comprobó nunca. Aplica la misma disciplina que aplicarías a los datos en vivo — identificar, autenticar, autorizar, auditar — a cada copia de seguridad y snapshot. Si acaso, aplícala *con más fuerza*, porque la copia de seguridad es el recurso de *último recurso.* Cuando todo lo demás ha fallado y echas mano de la copia de seguridad, ese es el peor momento posible para descubrir que estaba abierta de par en par.

---

[DIAPOSITIVA 40 — Tu mapa mental]

Recompongamos el mapa. Uno: una base de datos es **almacenamiento organizado más una forma de hacer preguntas** — archivador, Excel, o un clúster de cien millones de filas, la misma idea. Dos: hay **diez familias**, cada una con su propio problema de seguridad estrella — y ya las conoces las diez. Tres: casi todo vive en la **nube**, donde el bug rara vez es el motor y casi siempre es la **configuración** — responsabilidad compartida, tú eres dueño de la política y los datos. Cuatro: **el markdown ahora es una base de datos para los LLM**, y el envenenamiento de RAG es el nuevo XSS almacenado. Cinco: **la inyección SQL se arregló, y la superficie de ataque se expandió** a otras once formas de todos modos. Esa es la charla entera en cinco líneas. Si no recuerdas nada más, recuerda que seguir los datos es el trabajo, y los datos siempre están en una base de datos.

---

[DIAPOSITIVA 41 — Qué hacer la semana que viene]

Cinco cosas concretas que puedes hacer *la semana que viene* — no algún día, la semana que viene. Una: **instala PostgreSQL en local**, crea una tabla, escribe un `SELECT`. Tocar la cosa la desmitifica para siempre; deja de dar miedo en cuanto está corriendo en tu portátil. Dos: haz los **laboratorios de inyección SQL de PortSwigger** — son gratis, y escribirás un exploit funcional al final de una tarde. Tres: **navega por Shodan o Censys** — legalmente, solo sistemas que poseas o estés autorizado a probar — y observa cómo es de verdad "expuesto". Cuatro: **lee un informe de brecha** de principio a fin — Capital One, Equifax o MOVEit; las brechas reales son los mejores libros de texto que existen. Cinco: **averigua qué bases de datos corre tu propia organización.** La mayoría de los analistas de SOC no saben responderlo. Pasa una tarde haciendo la lista real, y al instante eres más útil que la mitad del equipo.

---

[DIAPOSITIVA 42 — Recursos que vale la pena guardar]

Cinco marcadores para llevarte. **PortSwigger Web Security Academy** — portswigger.net/web-security — la mejor rampa de entrada gratuita a la seguridad de aplicaciones web que existe, y donde te curtirás con inyección real. **SQLBolt** — sqlbolt.com — aprende SQL de forma interactiva, en tu navegador, divirtiéndote, sin instalar nada. **Use The Index, Luke** — use-the-index-luke.com — cuando estés listo para la magia profunda de cómo funcionan de verdad los índices y el rendimiento de consultas. **DB-Engines Ranking** — db-engines.com — la tabla de popularidad en marcha de básicamente toda base de datos que existe, genial para ver qué vale la pena aprender. Y el **OWASP Top 10** — owasp.org/Top10 — la lista canónica de vulnerabilidades web, incluidas las clases de inyección y mala configuración que tocamos hoy. Guarda estos cinco y tienes meses de aprendizaje autodirigido en cola, gratis.

---

[DIAPOSITIVA 43 — Las bases de datos son donde está el dinero. Literalmente.]

Os dejo con esto. Hay una vieja frase atribuida al atracador de bancos Willie Sutton. Cuando le preguntaron por qué robaba bancos, supuestamente dijo: *porque ahí es donde está el dinero.* En 2026, el dinero está en las **bases de datos.** Registros de clientes, registros financieros, registros de salud, propiedad intelectual, pesos de modelos, embeddings vectoriales, código fuente, secretos — todo ello vive en alguna base de datos, en algún sitio. Los atacantes ya lo saben; por eso cada historia de brecha termina donde termina. Lo único que ha cambiado en la última hora es que *ahora tú también lo sabes* — y, más importante, tienes el mapa para encontrarlo, nombrarlo y razonar sobre cómo falla. No necesitas una carrera de informática para ser peligroso aquí. Necesitabas el mapa. Lo tienes. Ahora sabes dónde mirar.

---

[DIAPOSITIVA 44 — Referencias: libros citados]

Ya casi estamos — los recibos. Todo lo que os he contado hoy está construido sobre los hombros de gente que lo escribió como Dios manda, y esta diapositiva lista los libros en los que me apoyé — *Learning SQL* de Beaulieu, *SQL Injection Attacks and Defense* de Clarke, *Secrets and Lies* de Schneier, *Threat Modeling* de Shostack, el *Web Application Hacker's Handbook*, *Cybersecurity Attack and Defense Strategies*, *Alice and Bob Learn Application Security* de Tanya Janca, y el OWASP Top 10 — la edición actual de 2025 — entre otros. No tenéis que leerlos todos — pero si alguna categoría de hoy os encendió, hay un libro entero en esta diapositiva esperando para llevaros más hondo. Hacedle una foto antes de que desaparezca. Estos son los hombros sobre los que se sostiene toda la charla — y con ellos ahí en la pantalla, abramos el turno de preguntas.

---

[DIAPOSITIVA 45 — Preguntas: dispara]

Y eso es la charla — gracias por quedaros conmigo los cuarenta y cinco minutos enteros. Esta última diapositiva es donde lo abrimos, así que este es vuestro momento: lanzadme vuestras preguntas, vuestras batallitas, eso de vuestro propio entorno que os ha estado rondando todo el rato que yo hablaba. Ninguna pregunta es demasiado básica aquí — recordad que toda la premisa de esta charla es que nadie nace sabiendo esto, y los que hacen las preguntas "obvias" suelen ser los que hablan en silencio por media sala. Que no os quedéis todos mirando. Si nos quedamos sin tiempo o tu pregunta necesita una pizarra, agárrame después o escríbeme — estoy en github.com/CryptoJones, o CryptoJones@infosec.exchange. Mientras se levantan las primeras manos: ¿qué fue lo que más os sorprendió? Para mucha gente es que las notas en markdown son ahora una base de datos viva. Así que — disparad. Y cuando terminemos aquí: id a averiguar qué bases de datos corre *vuestra* organización. En serio. Id.

---

*Aproximadamente 45 minutos de guion a lo largo de 45 diapositivas, cerrando con preguntas abiertas. Una charla independiente de CryptoJones (Aaron K. Clark).*
