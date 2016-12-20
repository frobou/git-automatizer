from setuptools import setup

setup(
    name="git_automatizer",
    version="0.0.1",
    author="Blobs Frobou",
    license="MIT License",
    author_email="blobs@frobou.com.br",
    url="https://frobou.github.io/git-automatizer/",
    description="Git auto synchronizer",
    packages=["git_automatizer"],
    install_requires=['gitpython']
)