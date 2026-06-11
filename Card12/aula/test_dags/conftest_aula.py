import pytest
from airflow.models import DagBag

# fixture para carregar os DAGs do Airflow, com escopo de sessão para evitar recarregamento 
# desnecessário durante os testes
@pytest.fixture(scope="session") 
def dagbag():
    return DagBag()