#import "_common.typ": *

#set page(margin: 1.5cm)
#set heading(numbering: "1.")
#set par(justify: true)

#let new-lecture = make-lecture-fn("rsod")
#let new-module = make-module-fn("rsod")

// Титульная страница
#page(numbering: none)[
  #set align(center)
  #v(1fr)

  #text(size: 14pt, weight: "bold")[
    Санкт-Петербургский государственный электротехнический \
    университет «ЛЭТИ» им. В.И. Ульянова (Ленина)
  ]

  #v(1fr)

  #text(size: 28pt, weight: "bold")[
    Распределённые системы \
    обработки данных
  ]

  #v(0.5fr)


  #v(2fr)

  #text(size: 12pt)[
    Санкт-Петербург \
    2026
  ]

  #v(0.5fr)
]

#outline(title: [Содержание], indent: auto, depth: 4)
#lecture-state.update(0)
#pagebreak()

#print-glossary()



#pagebreak()

= #new-module("Компоненты распределённых систем")

== #new-lecture("Основы распределённых систем")
=== CAP-теорема
- Следствия компромиссов между согласованностью, доступностью и устойчивостью к разделению сети
- Примеры CA, AP, CP систем
=== Механизмы репликации данных
- Архитектура "ведущий-подчинённый" (Leader-Follower)
- Репликация с использованием кворумов (quorum-based replication)
=== ZooKeeper: распределённое решение проблем согласованности и отказоустойчивости
- Механизмы решения классических проблем распределённых систем
- Применение в системах Kafka и ClickHouse

== #new-lecture("Гарантии консистентности и координация распределённых транзакций")
=== Алгоритмы достижения консенсуса
- Raft
- Paxos
=== Модель конечной консистентности (Eventual consistency) и требование идемпотентности операций
=== Протокол двухфазного коммита (Two-Phase Commit, 2PC)
- Этапы выполнения
- Гарантии надёжности
= #new-module("Распределенные сервисы")

== #new-lecture("Асинхронное взаимодействие сервисов")
=== Event Bus и Event-Driven Architecture
=== Publish-Subscribe vs Message Queue
=== Saga Pattern

== #new-lecture("Kafka")
=== Внутреннее устройство

== #new-lecture("Kubernetes")
=== Роль и место в современных архитектурах
=== Области использования
=== Внутреннее устройство

== #new-lecture("ClickHouse")
=== Архитектура системы хранения и обработки данных
- Принципы организации хранения
- Методы компрессии данных
=== Партиционирование
- Выбор ключа
- Управление партициями (добавление, удаление)
=== Таблицы серии MergeTree как основной механизм персистентности
- Базовая таблица MergeTree и её специализированные варианты
- ReplacingMergeTree для управления версионированием
- ReplicatedMergeTree для обеспечения отказоустойчивости

== #new-lecture("Apache Spark")
=== Роль и место в современных архитектурах
=== Области использования
=== Внутреннее устройство
=== API
- Dataframe
- SparkSQL

== #new-lecture("Erlang")
=== Роль и место в современных архитектурах
=== Erlang VM (BEAM) и процессы
=== Модель акторов
=== Fault tolerance и "Let it crash" философия
=== OTP фреймворк (Supervisor, GenServer)
=== Синхронизация и распределённые вычисления
=== Elixir

= #new-module("Распределенные БД")

== #new-lecture("Большие данные")
=== Свойства
- Объем
- Скорость
- Разнообразие
- Достоверность
=== Архитектуры
- Modern Data Architecture
- Lambda
- Lakehouse

== #new-lecture("Full Text Search в распределённых системах")
=== Elasticsearch и Solr
- Sharding: hash-based, range-based
- Replication и replica factor
- Eventual consistency при индексировании
=== Распределённый поиск
- Broadcast query, merge результатов
- Search After вместо offset/limit
=== Масштабирование
- Hot shards проблема
- Index rollover, segment merging

== #new-lecture("Документные хранилища")
=== MongoDB: sharding strategies, write concerns
=== Object storage: MinIO

== #new-lecture("Распределенные пространственные и графовые БД")
=== Графовые БД
=== Пространственные БД
=== Шардирование графов и пространственных данных
