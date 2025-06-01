from setuptools import setup, find_packages

setup(
    name='finance_tracker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy>=2.0.0',
        'alembic>=1.14.0', 
        'click>=8.1.0'
    ],
    entry_points='''
        [console_scripts]
        finance=finance_tracker.cli:cli
    ''',
)