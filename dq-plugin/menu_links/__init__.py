from flask_admin.base import MenuLink

test_link = \
    MenuLink(
        category='Plugins',
        name='Test Menu Link',
    	url='https://airflow.apache.org/'
    )


MENU_LINKS = [
    test_link,
]
