import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="1", # Replace with your own username
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "cronp": [
            'db=cron_migration.app:cli'
        ],
        "console_scripts": [
            'cronp-db=cron_migration.app:cli'
        ]
    },
    python_requires='>=3.6',
)

import pkg_resources

named_objects = {}
for ep in pkg_resources.iter_entry_points(group='my_ep_group_id'):
   named_objects.update({ep.name: ep.load()})