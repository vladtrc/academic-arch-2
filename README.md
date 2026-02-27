# academic-arch-2

Учебные материалы в формате Typst. Репозиторий собирает PDF-лекции по трём курсам:
- `ais` — «Архитектура информационных систем»: слои, DI, порты/адаптеры, примеры персистентности в CSV;
- `rsod` — «Распределённые системы обработки данных»: консенсус, репликация, event-driven, Kafka/Spark;
- `olap-ib` — «Аналитическая обработка данных в задачах ИБ»: ClickHouse, MergeTree, партиционирование, TTL.

## Требования

- `docker` — сборка PDF через контейнер Typst;
- `uv` — запуск Python-скриптов проекта (генерация архитектурных схем из YAML, утилиты для примеров с CSV).

## Основные команды

```bash
make           # сборка всех PDF
make -B build  # принудительная пересборка
make watch     # пересборка при изменениях
make clean     # удалить PDF-артефакты
make list ais  # структура документа по заголовкам
```

## Генерация Figure 5 из YAML

Конфиг схемы: `scripts/clean-architecture.yaml`.

Сборка SVG вручную:

```bash
uv run --project scripts scripts/gen_arch_svg.py \
  --input scripts/clean-architecture.yaml \
  --output src/assets/clean-architecture.svg
```

Скрипт поддерживает произвольную layered architecture:
- набор слоёв (`layers`);
- компоненты внутри каждого слоя (`components`);
- связи между компонентами (`connections`).
