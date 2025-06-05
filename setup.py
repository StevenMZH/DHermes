from setuptools import setup, find_packages

# Cargar dependencias desde requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

# Cargar README para la descripción larga
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hermes-deployer",
    version="0.1.0",
    author="Steven Mendoza",
    # author_email="tu.email@ejemplo.com",
    description="Sistema de despliegue automatizado con YAML para servidores y aplicaciones.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/hermes-deployer",  # Cambia esto
    packages=find_packages(exclude=["tests*", "docs*"]),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hermes=hermes.cli:main",  # Asegúrate de tener este archivo y función
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    license="MIT",
    project_urls={
        "Documentation": "https://github.com/tu_usuario/hermes-deployer",
        "Source": "https://github.com/tu_usuario/hermes-deployer",
        "Issues": "https://github.com/tu_usuario/hermes-deployer/issues",
    },
)
