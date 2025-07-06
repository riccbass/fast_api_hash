### inicia o alembic

alembic init alembic

<sub>depois de inicaializado, começa a migrar</sub>

### cria migração

alembic revision --autogenerate -m "Initial Migration"

### executa migração

alembic upgrade head

### cria migração

alembic revision --autogenerate -m "rmover admin"

### executa migração

alembic upgrade head
