from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["discord", 
                "pillow", 
                "git@github.com:Pablo-Valverde/pydiscord.git"
               ]

setup(
    name="felaciano",
    version="1.0.0",
    author="Pablo Valverde",
    author_email="pabludo8cho@gmail.com",
    description="Felaciano el makina",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Pablo-Valverde/bot_discord",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9.5",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
