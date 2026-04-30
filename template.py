import os 
from pathlib import Path
import logging

logging.basicConfig(level = logging.INFO, format = '[%(asctime)s]: %(message)s:')

project_name = "dsc_winequality"

list_of_files = [
    ".gthub/workflows/.gitkeep",  #responsible in doing deployments (github)
    f"src/{project_name}/__init__.py", #constructor to convert this to a package and import easily (must be done inside every fresh folder)
    f"src/{project_name}/components/__init__.py", # all the pipelines stay inside this, will be having classes, will be a package and will get installed inside lcoal
    f"src/{project_name}/utils/__init__.py", # generic functionalities, can be used evrywhere in the project
    f"src/{project_name}/utils/common.py", # functionalities which will be used across classes in components
    f"src/{project_name}/config/__init__.py", 
    f"src/{project_name}/config/configuration.py", #what all different pipelines, training pipeline, prediction pipeline
    f"src/{project_name}/pipeline/__init__.py", 
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",  
    f"src/{project_name}/constants/__init__.py", 
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "Dockerfile",
    "pyproject.toml",
    "setup.py",
    "dev/simulate.ipynb", # play around for work
    "frontend/application.py", #frontend sml
    "frontend/pages/01_landing.py",
]



for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = filepath.parent, filepath.name
    if filedir != Path("."):
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file at {filepath}")
    else:
        logging.info(f"{filepath} already exists")