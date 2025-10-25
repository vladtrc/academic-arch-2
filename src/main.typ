#set page(margin: 1.5cm)
#set heading(numbering: "1.")
#set par(justify: true)

// ============ СЧЁТЧИКИ ============
#let lecture-counter-1 = counter("lecture-1")
#let module-counter-1 = counter("module-1")
#let lecture-counter-2 = counter("lecture-2")
#let module-counter-2 = counter("module-2")

#let make-new-lecture(counter) = (name) => context {
  counter.step()
  let num = counter.get().at(0)
  [Лекция #num: #name]
}

#let make-new-module(counter) = (name) => context {
  counter.step()
  let num = counter.get().at(0)
  [Модуль #num: #name]
}


#lecture-counter-1.update(1)
#module-counter-1.update(1)
#lecture-counter-2.update(1)
#module-counter-2.update(1)

#outline(
  title: [Содержание],
  indent: auto,
  depth: 4
)

#lecture-counter-1.update(1)
#module-counter-1.update(1)
#lecture-counter-2.update(1)
#module-counter-2.update(1)

= Архитектура информационных систем

#let new-lecture = make-new-lecture(lecture-counter-1)
#let new-module = make-new-module(module-counter-1)

== #new-module("Архитектурные основы")

=== #new-lecture("Введение. Принципы построения приложения")
==== Оптимизация системы требует выбора критерия оптимизации
==== Принципы SOLID
==== Dependency Injection
==== Clean Architecture

=== #new-lecture("Альтернативные архитектурные паттерны")
==== Архитектура на основе фреймворка (Rails, Django)
==== Модель акторов (Erlang/Elixir/Akka)
==== Проектирование, ориентированное на данные (Data-oriented design)

=== #new-lecture("Протоколы взаимодействия")
==== REST: стандартный веб-протокол
==== GraphQL: клиент запрашивает только нужные данные
==== gRPC: бинарный протокол, высокая производительность
==== WebSocket: двусторонний канал

== #new-module("Фундаментальные структуры хранилищ данных")

=== #new-lecture("Базовые механизмы хранения данных")
==== CSV-файлы как минимальная форма персистентности
==== CSV с добавлением записей и журналированием изменений
==== Хеш-индексы как первый уровень ускорения выборки

=== #new-lecture("Структурированные индексы")
==== Отсортированная таблица строк (Sorted String Table, SSTable)
==== Дерево слияния структурированного журнала (Log-Structured Merge-Tree, LSM-Tree)
==== Когда использовать LSM-деревья и B-деревья (LSM хороша для записи, B-Tree для чтения)

=== #new-lecture("ACID, уровни изоляции, аналитические и транзакционные хранилища")
==== ACID (Atomicity, Consistency, Isolation, Durability)
==== Уровни изоляции
- Read Uncommitted
- Read Committed
- Repeatable Read
- Serializable
==== Аналитические базы данных (OLAP) и колоночные хранилища
==== Сжатие колонок
==== Сравнение подходов

== #new-module("Другие хранилища данных")

=== #new-lecture("Аналитика в оперативной памяти")
==== Vectorized execution (блочная обработка)
==== DuckDB
- Чтение из различных источников
- Трансформация данных
- Запись

=== #new-lecture("Кэш в оперативной памяти")
==== Skip List
==== Incremental Rehashing
==== HyperLogLog
==== Redis
- Архитектура (однопоточность, event-driven)

== #new-module("Методы поиска похожих/близких элементов")

=== #new-lecture("Специализированные индексы для поиска")
==== Inverted Index (перевёрнутые индексы)
- Постинг-листы (posting lists)
- Применение: Elasticsearch, Lucene
==== Trie (префиксные деревья)
- Автодополнение, префиксный поиск
==== Bitmap indexes
- Для категориальных данных

=== #new-lecture("Векторные индексы для поиска подобия")
==== Основы векторных представлений
==== HNSW (Hierarchical Navigable Small World)
- Граф как индекс
- Поиск соседей
==== LSH (Locality-Sensitive Hashing)
- Вероятностный поиск
==== Примеры: Weaviate, Pinecone, Qdrant

=== #new-lecture("Геопространственные структуры")
==== R-Tree
- Bounding boxes, MBR
- Применение: PostGIS
==== QuadTree и KD-Tree
- Разбиение пространства
- Когда какое дерево эффективнее


== #new-module("Операционные компоненты")

=== #new-lecture("Прокси и Rate Limiting")
==== Forward Proxy / Reverse Proxy
==== Распределение нагрузки
- Round Robin
- Least Connections
- Weighted Least Connections
- IP Hash
- Consistent Hashing
==== Ограничение частоты запросов
- Token Bucket
- Sliding Window

=== #new-lecture("Безопасность и управление доступом")
==== Аутентификация и авторизация
==== RBAC и ABAC
==== Single Sign-On

=== #new-lecture("Логирование, мониторинг и планирование задач")
==== Сбор логов
==== Сбор метрик (Prometheus)
==== Мониторинг и диагностика (Grafana)
==== Планировщики (Celery, Airflow, Dagster)

== #new-module("System Design")

=== #new-lecture("Разбор дизайна конкретной системы")
==== Применение всех концепций на практике

// ============ КУРС 2: Распределённые системы обработки данных ============
#let new-lecture = make-new-lecture(lecture-counter-2)
#let new-module = make-new-module(module-counter-2)
#pagebreak()
= Распределённые системы обработки данных


== #new-module("Компоненты распределённых систем")

=== #new-lecture("Основы распределённых систем")
==== CAP-теорема
- Следствия компромиссов между согласованностью, доступностью и устойчивостью к разделению сети
- Примеры CA, AP, CP систем
==== Механизмы репликации данных
- Архитектура "ведущий-подчинённый" (Leader-Follower)
- Репликация с использованием кворумов (quorum-based replication)
==== ZooKeeper: распределённое решение проблем согласованности и отказоустойчивости
- Механизмы решения классических проблем распределённых систем
- Применение в системах Kafka и ClickHouse

=== #new-lecture("Гарантии консистентности и координация распределённых транзакций")
==== Алгоритмы достижения консенсуса
- Raft
- Paxos
==== Модель конечной консистентности (Eventual consistency) и требование идемпотентности операций
==== Протокол двухфазного коммита (Two-Phase Commit, 2PC)
- Этапы выполнения
- Гарантии надёжности
== #new-module("Распределенные сервисы")

=== #new-lecture("Асинхронное взаимодействие сервисов")
==== Event Bus и Event-Driven Architecture
==== Publish-Subscribe vs Message Queue
==== Saga Pattern

=== #new-lecture("Kafka")
==== Внутреннее устройство

=== #new-lecture("Kubernetes")
==== Роль и место в современных архитектурах
==== Области использования
==== Внутреннее устройство

=== #new-lecture("ClickHouse")
==== Архитектура системы хранения и обработки данных
- Принципы организации хранения
- Методы компрессии данных
==== Партиционирование
- Выбор ключа
- Управление партициями (добавление, удаление)
==== Таблицы серии MergeTree как основной механизм персистентности
- Базовая таблица MergeTree и её специализированные варианты
- ReplacingMergeTree для управления версионированием
- ReplicatedMergeTree для обеспечения отказоустойчивости

=== #new-lecture("Apache Spark")
==== Роль и место в современных архитектурах
==== Области использования
==== Внутреннее устройство
==== API
- Dataframe
- SparkSQL

=== #new-lecture("Erlang")
==== Роль и место в современных архитектурах
==== Erlang VM (BEAM) и процессы
==== Модель акторов
==== Fault tolerance и "Let it crash" философия
==== OTP фреймворк (Supervisor, GenServer)
==== Синхронизация и распределённые вычисления
==== Elixir


== #new-module("Распределенные БД")


=== #new-lecture("Большие данные")
==== Свойства
- Объем
- Скорость
- Разнообразие
- Достоверность
==== Архитектуры
- Modern Data Architecture
- Lambda
- Lakehouse

=== #new-lecture("Full Text Search в распределённых системах")
==== Elasticsearch и Solr
- Sharding: hash-based, range-based
- Replication и replica factor
- Eventual consistency при индексировании
==== Распределённый поиск
- Broadcast query, merge результатов
- Search After вместо offset/limit
==== Масштабирование
- Hot shards проблема
- Index rollover, segment merging

=== #new-lecture("Документные хранилища")
==== MongoDB: sharding strategies, write concerns
==== Object storage: MinIO

=== #new-lecture("Распределенные пространственные и графовые БД")
==== Графовые БД
==== Пространственные БД
==== Шардирование графов и пространственных данных
