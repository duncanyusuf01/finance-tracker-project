from setuptools import setup, find_packages

setup(
    name='finance_tracker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'alembic',
        'click'
    ],
    entry_points='''
        [console_scripts]
        finance=finance_tracker.cli:cli
    ''',
)