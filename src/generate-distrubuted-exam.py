import random

questions = {
    1: [
        "Zookeeper",
        "Основные принципы и парадигмы распределённых систем",
        "Преимущества децентрализованных систем",
        "Роль облачных систем в распределённых системах",
        "Примеры распределённых систем и их применение",
        "Основная архитектура Hadoop-кластера",
        "Отличия централизованной архитектуры от децентрализованной",
        "Виды кластеров (HA, Beowulf, Облачные)",
        "Проблемы масштабируемости централизованных систем",
        "CAP теорема и её применение в распределённых системах",
        "Основные характеристики HDFS",
        "Типы кластеров и их особенности",
        "Технологии потоковой обработки данных",
        "Пример использования Apache Kafka в распределённых системах",
        "CEPH (Common Extensible Parallel Hierarchical storage)",
    ],
    2: [
        "Основные источники данных для Big Data",
        "Свойства больших данных: Объем и Скорость",
        "Свойства больших данных: Разнообразие и Достоверность",
        "Методы анализа данных для больших данных (классические)",
        "Методы анализа данных для больших данных (новые)",
        "Отличия традиционной аналитики от аналитики больших данных",
        "Отличия SQL vs NoSQL СУБД",
        "NoSQL СУБД: документно-ориентированные, колоночные хранилища",
        "NoSQL СУБД: графовые хранилища и ключ-значение",
        "Масштабирование реляционной СУБД",
        "CAP теорема",
        "Традиционный подход организации хранилищ",
        "Advanced Architecture",
        "Lambda Architecture",
        "Lakehouse",
    ],
    3: [
        "ClickHouse: что это и где применяется?",
        "ClickHouse: основные отличия от классических СУБД",
        "Движки ClickHouse: назначение и примеры",
        "MergeTree: ключевые возможности и варианты",
        "Слияния (merges) в ClickHouse: зачем нужны и как работают",
        "Партиционирование в ClickHouse: зачем нужно и как выбирать ключ",
        "ORDER BY в ClickHouse: как влияет на хранение и скорость запросов",
        "Primary Key в ClickHouse: отличие от ORDER BY",
        "TTL в ClickHouse: сценарии и настройка",
        "Обновления данных: ALTER UPDATE/DELETE и как устроены мутации",
        "UPSERT в ClickHouse: практические подходы и ограничения",
        "Распределенные таблицы и шардирование в ClickHouse",
        "Репликация в ClickHouse: ReplicatedMergeTree и роль ZooKeeper/ClickHouse Keeper",
    ],
    4: [
        "Вычисления в памяти",
        "Распределенные вычисления",
        "База данных в памяти",
        "Кэширование памяти",
        "Пограничные вычисления",
        "Apache Spark: Определение & история",
        "Цели Apache Spark",
        "Apache Spark vs Hadoop MapReduce",
        "Apache Spark: Применение (Машинное обучение & Анализ больших данных)",
        "Apache Spark: Применение (Стриминг данных & Графовые вычисления)",
        "Apache Spark: Архитектура",
        "Apache Spark: Cluster Manager",
        "Apache Spark: RDD",
        "Apache Spark: Роль Driver’а",
        "Apache Spark: Роль Executor’ов",
    ],
    5: [
        "Apache Spark: Core",
        "Apache Spark: DataFrame",
        "Apache Spark: Dataset",
        "Apache Spark: Преимущества Dataset API",
        "Apache Spark: Основные отличия между RDD, DataFrame и Dataset",
        "Apache Spark: Когда использовать RDD?",
        "Apache Spark: Преимущества Dataset API",
        "Apache Spark: DataFrame vs Dataset API",
        "Apache Spark: Transformations & Actions",
        "Apache Spark: Task Scheduler & DAG",
        "Apache Spark: Логическое планирование",
        "Apache Spark: Физическое планирование",
        "Apache Spark: Spark SQL",
        "Apache Spark: Архитектура Spark SQL",
        "Apache Spark: Catalyst Optimizer",
    ],
    6: [
        "Apache Spark: Dataframe API",
        "Apache Spark Dataframe API: Агрегации",
        "Apache Spark Dataframe API: Группировки",
        "Apache Spark Dataframe API: Join",
        "Apache Spark Dataframe API: Кэширование данных",
        "Apache Spark: Broadcast",
        "Apache Spark: Партиционирование данных",
        "Apache Spark: Отличия repartition и coalesce",
        # дубли до 13 (17 по куберу)
        "Apache Spark: Основные отличия между RDD, DataFrame и Dataset",
        "Apache Spark: Когда использовать RDD?",
        "Apache Spark: Transformations & Actions",
        "Apache Spark: Task Scheduler & DAG",
        "Apache Spark: Логическое & Физическое планирование",
    ],
    7: [
        "Apache Kafka: Описание & История",
        "Apache Kafka: Популярные сценарии использования",
        "Apache Kafka: Архитектура",
        "Apache Kafka: Topics & Partitions",
        "Apache Kafka: Репликация",
        "Apache Kafka: Режимы репликации",
        "Apache Kafka: Producers & Consumers",
        "Apache Kafka: Consumer Groups",
        "Apache Kafka: Принципы доставки данных",
        "Apache Kafka: Брокеры Kafka",
        "Apache Kafka: Кластеризация",
        "Apache Kafka: Роль Zookeeper",
        "Apache Kafka: Восстановление данных при сбоях",
        "Apache Kafka: Schema Registry",  # было на практике!
        "Использование Kafka для интеграции микросервисов",  # его нет в лекциях, но я хз какой тут можно
    ],
    8: [  # 14 , есть 16 в след
        "Apache Kafka: Connect API",
        "Apache Kafka Connect API: Change Data Capture & Импорт и экспорт данных",
        "Apache Kafka Connect API: Аналитика в реальном времени & Сбор метрик",
        "Apache Kafka Connect API: Передача данных в хранилища & Поддержка различных форматов",
        "Apache Kafka Connect API: Обработка событий",
        "Apache Kafka: Потоковая vs пакетная обработка данных",
        "Apache Kafka: Streams API",
        "Apache Kafka: Основные параметры производительности Kafka",
        "Apache Kafka: Техники для повышения производительности Kafka",
        "Apache Kafka: Параметры потребителей",
        "Apache Kafka: Интеграция с Apache Spark и Apache Flink",
        "Apache Flink",
        "Apache Kafka: Параметры потребителей",
        "Apache Kafka: Интеграция с платформами данных",
    ],
    9: [  # 16
        "Kubernetes: Оркестровка контейнеров",
        "Kubernetes: Описание инструмента & Сертифицированные дистрибутивы",
        "Kubernetes vs Docker Swarm",
        "Kubernetes: Мастер Kubernetes",
        "Kubernetes: ETCD & Планировщик",
        "Kubernetes: Менеджер сервера API & Менеджер по работе с контроллерами",
        "Kubernetes: Kubectl",
        "Kubernetes: Kubernetes Worker",
        "Kubernetes: Kubelet & Kube proxy",
        "Kubernetes: K3s",
        "Kubernetes: Pods",
        "Kubernetes: Масштабирование капсул",
        "Kubernetes: Императивные и декларативные команды",
        "Kubernetes: Файл Manifest/Spec",
        "Kubernetes: Создание капсул (Декларативный способ)",
        "Kubernetes: Создание капсул (Императивный способ)",
    ],
    10: [  # 17
        "Kubernetes: Deployment",
        "Kubernetes: Стратегия скользящего обновления",
        "Kubernetes: Пространства имен",
        "Kubernetes: Службы",
        "Kubernetes: ClusterIP",
        "Kubernetes: NodePort",
        "Kubernetes: Ограничения NodePort",
        "Kubernetes: LoadBalancer",
        "Kubernetes: GCP LoadBalancer",
        "Kubernetes: LoadBalancer vs Ingress",
        "Kubernetes: MetalLB",
        "Kubernetes: Volumes",
        "Kubernetes: emptyDir",
        "Kubernetes: Постоянный том и утверждение постоянного тома",
        "Kubernetes: Планирование (nodeSelector)",
        "Kubernetes: Планирование (nodeAffinity)",
        "Kubernetes: Taints and Tolerations",
    ],
}

# Преобразуем данные для генерации
chapter_questions = [
    (chapter, question)
    for chapter, questions_list in questions.items()
    for question in questions_list
]

# Проверка на четность количества вопросов
if len(chapter_questions) % 2 != 0:
    raise ValueError(
        f"Общее количество вопросов должно быть четным для формирования пар. {len(chapter_questions)}"
    )

# Перемешиваем вопросы
random.shuffle(chapter_questions)

# Разделяем на билеты
tickets = []
while chapter_questions:
    question1 = chapter_questions.pop()
    question2 = chapter_questions.pop()

    # Проверяем, чтобы вопросы были из разных глав
    if question1[0] != question2[0]:
        tickets.append((question1[1], question2[1]))
    else:
        # Если главы совпадают, добавляем вопросы обратно и перемешиваем
        chapter_questions.extend([question1, question2])
        random.shuffle(chapter_questions)

# Вывод билетов
for i, ticket in enumerate(tickets, 1):
    print(f"Билет {i}: {ticket[0]}, {ticket[1]}")
