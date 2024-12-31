from setuptools import setup, find_packages

setup(
    name="jobfinder",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "crewai",
        "pytest",
    ],
    python_requires=">=3.10,<3.13",
)
