# Вариант 13. GPS-события транспорта (Apache Cassandra)

## Запуск

1. Запустить Cassandra в Docker: `docker run --name cassandra-node -p 9042:9042 -d cassandra:latest`
2. Создать схему через `cqlsh` из файла `scripts/init_db.cql`
3. Установить зависимости: `pip install -r requirements.txt`
4. Сгенерировать данные: `python data/generate_data.py`
5. Запустить тесты: `python -m unittest discover -s tests`
