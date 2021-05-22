from setuptools import find_packages, setup

setup(
    name="parky-server",
    version="0.0.1",
    description="backend server for parky",
    install_requires=["fastapi[all]", "sqlalchemy", "requests", "uvicorn", "mysql-client", "mysql-connector-python"],
    url="https://github.com/not-decided-yet/parky-server",
    author="Not Decided Yet (NDY)",
    author_email="harrydrippin@gmail.com",
    packages=find_packages(exclude=["tests"]),
)
