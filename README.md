# real_estate_avito
## Описание : 
Проектик для использования и тестирования технологий биг ~~и не очень~~ даты

* ETL - dagster  
  * Повольно универсальная и "питонячая" DAG платформа
  * Позволяет дешево строить довольно гибкие дата пайплайны
* BD - duckdb
    * Колоночная бдшка с классной итеграцией по форматам и технологиям
    * Нативная поддержка 
        * .csv
        * .parquet
        * других бд (sqlite,postgres)
* DM  - Poetry 
    * Удобный и гибкий медеджер зависимостей
* Docker - docker epta
    * Инструмент виртуализации окружения
    * Гарантируем воспроизведения среды разработки на любой консервной банке
* Selenium
    * Эмуляция браузера для сбора открытых данных


## Состав
### **/data**
Cодержит собранные данные по категориям недвижки  
1) Застройщки
1) Вторичка
1) Агенства

#### Параметры
```
0	datetime - время сбора (datetime)
1	publish_delta - дельта публикации от времени сбора (текст)
2	id - id объявления
3	url - url объявления
4	text - тект превью объявления
5	price - цена
6	JK - наличие ЖК (в основном у застройщиков)
7	metro_dist - расстояние до метро
8	metro - название метро
9	metro_branch - цвет ветки метро
10	street - название улицы
11	is_new - является ли новостройкой ( прокси от JK)
12	n_rooms - кол-во комнат
13	m2 - метраж квартиры
14	floor - этаж квартиры
15	max_floor - этажность дома
16	rubm2 - цена квадратного метра 
```

### **/notebooks**
Примеры использования данных и технодемки итоговых скриптов  
1) selenium_test - использование headless seleniuma для не агрессивного парсинга
1) examples - примеры получения данных
### **/repositories**
Файлы и функции нашего DAG пайплайнера\шедулера
## Запуск добора данных
### Параметризация:
+ либо .env файлик в корне проекта
+ либо переменные окружения с соответствующими именами из compsoe.yml
### Запуск
``` shell 
docker compose up -d
```
Запуск процессов в графическом интерфейсе на локал хосте и указанном порте