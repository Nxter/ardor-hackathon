from setuptools import setup

setup(
    name="sigbro-access-control",
    version="0.1.0",
    description="Sigbro access conrtol checker",
    url="",
    author="scor2k",
    author_email="scor2k@gmail.com",
    license="MIT",
    packages=["sigbro_ac"],
    entry_points={"console_scripts": ["sigbro-ac=sigbro_ac.cli:cli"]},
    zip_safe=False,
)
