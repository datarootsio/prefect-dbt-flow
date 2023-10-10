from distutils.core import setup

setup(
    name="prefect_dbt_flow",
    packages=["prefect_dbt_flow"],
    version="0.0.1",
    license="MIT",
    description="Prefect - dbt integration",
    author="Nico Gelders",
    author_email="nico@dataroots.io",
    url="https://datarootsio.github.io/prefect-dbt-flow",
    download_url="https://github.com/datarootsio/prefect-dbt-flow/archive/refs/tags/v0.0.1-alpha.tar.gz",
    keywords=["dbt", "prefect"],
    install_requires=[
        "prefect",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)
