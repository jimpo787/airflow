from airflow.exceptions import AirflowException
import pendulum
# Airflow 3.0 부터 아래 경로로 import 합니다.
from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator

# Airflow 2.10.5 이하 버전에서 실습시 아래 경로에서 import 하세요.
#from airflow import DAG
#from airflow.decorators import task
#from airflow.operators.bash import BashOperator

with DAG(
    dag_id='dags_python_with_trigger_rule_eg1',
    start_date=pendulum.datetime(2026,4,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    bash_upstream_1 = BashOperator(
        task_id='bash_upstream_1',
        bash_command='echo upstream1'
    )

    @task(task_id='python_upstream_1')
    def python_upstream_1():
        raise AirflowException('downstream_1 Exception!')


    @task(task_id='python_upstream_2')
    def python_upstream_2():
        print('정상 처리')

    @task(task_id='python_downstream_1', trigger_rule='all_done')
    def python_downstream_1():
        # trigger_rule 'all_done' 모든 Task가 성공적 수행시 나음 테스크로 넘어갈 수 있음, 다른 Trigger Rule은 Airflow 공식 문서를 확인하자
        # 당현히 예제 upstream의 경우 exception을 강제로 발생햇음으로 안넘어 갈 것임
        print('정상 처리')

    [bash_upstream_1, python_upstream_1(), python_upstream_2()] >> python_downstream_1()