import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="itay-bardugo-cron-migration", # Replace with your own username
    version="1.0.1",
    author="Itay Bardugo",
    author_email="itaybardugo91@gmail.com",
    description="manage your cron jobs with python and a revision system(CLI)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itay-bardugo/python-cron-migration",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": [
            'cronmig=cron_migration.cli.commands:cronmig',
            'cronmig-revision=cron_migration.cli.commands:revision',
        ]
    },
    python_requires='>=3.8.3',
)
