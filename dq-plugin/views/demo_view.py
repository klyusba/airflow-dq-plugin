from flask_admin import BaseView, expose
from flask import redirect, request
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms import DateTimeField

from demo_plugin.hooks import PostgresHook
from airflow.hooks.base_hook import BaseHook
from airflow.configuration import conf
from airflow.api.common.experimental.trigger_dag import trigger_dag


DAGS_FOLDER = conf.get('core', 'dags_folder')
CONN_ID = 'dq'
SOURCE_CONN_ID = 'db_ng_ach_gov_ru'  # TODO move to checks table


class CreateCheckForm(Form):
    name = StringField("Название сверки: ", render_kw={'style': 'width: 50vw'})
    script = TextAreaField("Скрипт:", render_kw={'style': 'width: 50vw; height: 50vh'})
    schedule = StringField("Регламент запуска: ", render_kw={'style': 'width: 50vw'})
    submit = SubmitField("Создать")


class DemoView(BaseView):
    @expose('/')
    def index(self):
        pg_hook = PostgresHook(postgres_conn_id=CONN_ID)
        checks = pg_hook.get_records("SELECT id, name FROM checks ORDER BY name")
        return self.render("index.html", checks=checks)

    @expose('/check/<int:id>')
    def get_check(self, id):
        pg_hook = PostgresHook(postgres_conn_id=CONN_ID)
        name, author, schedule, query = pg_hook.get_first(
            "SELECT name, author, schedule, query FROM checks WHERE id = %(id)s", 
            parameters={'id': id}
        )
        return self.render("properties.html", id=id, name=name, author=author, script=query, schedule=schedule)

    @expose('/check', methods=('POST',))
    def create(self):
        pg_hook = PostgresHook(postgres_conn_id=CONN_ID)
        check_id = pg_hook.run_returning("""
            INSERT INTO checks (name, author, schedule, query) 
            VALUES (%(name)s, 'admin', %(schedule)s, %(script)s)
            RETURNING id 
            """, 
            parameters=request.form
        )[0]

        name = request.form['name']
        schedule = request.form['schedule']
        script = request.form['script']
        dag = self.render('dag.tmpl', id=check_id, name=name, schedule=schedule, script=script, dq_conn_id=CONN_ID, conn_id=SOURCE_CONN_ID)
        with open(DAGS_FOLDER + f'/dq/dq_{check_id}.py', 'w', encoding='utf-8') as f:
            f.write(dag)

        return redirect('.')

    @expose('/run/<int:id>')
    def run(self, id):
        pg_hook = PostgresHook(postgres_conn_id=CONN_ID)
        try:
            run_id, status, run_dttm = pg_hook.get_first(
                """SELECT id, status, start_dttm FROM runs WHERE check_id = %(id)s ORDER BY id DESC LIMIT 1""", 
                parameters={'id': id}
            )
            results = pg_hook.get_records(
                "SELECT msg FROM results WHERE run_id = %(id)s", 
                parameters={'id': run_id}
            )
            return self.render("run.html", results=results, run_dttm=run_dttm, status=status)
        except:
            return ""

    @expose('/new')
    def form_new(self):
        form = CreateCheckForm(data={'schedule': '@daily'})
        return self.render("new.html", form=form)
