import pendulum
# Airflow 3.0 부터 아래 경로로 import 합니다.
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, Variable

# Airflow 2.10.5 이하 버전에서 실습시 아래 경로에서 import 하세요.
#from airflow import DAG
#from airflow.models import Variable
#from airflow.operators.bash import BashOperator

# 일반적으로 전역변수는 바뀌지 않는 상수, 절대 변수 사용. 전역변수 등록은 airflow web에서 등록한다.

with DAG(
    dag_id="dags_bash_with_variable",
    schedule="10 9 * * *",
    start_date=pendulum.datetime(2026, 4, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    var_value = Variable.get("sample_key")

    bash_var_1 = BashOperator(
    task_id="bash_var_1",
    bash_command=f"echo variable:{var_value}"
    )

    # 하기 Task를 권장 (스케줄의 부하가 적기 떄문)
    bash_var_2 = BashOperator(
    task_id="bash_var_2",
    bash_command="echo variable:{{var.value.sample_key}}"
    )