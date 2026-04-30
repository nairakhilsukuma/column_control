import os
import yaml
from src.dsc_winequality.logging import logger
import json
import joblib #can be .pkl (its a serialization format for models)
from ensure import ensure_annotations # ensures typehinter is ensured **** IMPORTANT
from box import ConfigBox #Helps to directly access dictionary values using "a.key" , the dot
from pathlib import Path
from typing import Dict , Any
from box.exceptions import BoxValueError


@ensure_annotations
def read_yaml(yaml_path: Path) -> ConfigBox:
    """ read yaml paths
    Args:
        yaml_path : path of the yaml file to read as a Path() str.

    Outputs:
        ConfigBox(Dict): Parsed yaml file as a dictionary

    """
    try:
        with open(yaml_path) as file:
            content = yaml.safe_load(file)
            logger.info(f"yaml file: {yaml_path} laoded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml loader failed")
    except Exception as e:
        raise e
        

@ensure_annotations
def read_yaml(yaml_path: Path) -> ConfigBox:
    """ read yaml paths
    Args:
        yaml_path : path of the yaml file to read as a Path() str.

    Outputs:
        ConfigBox(Dict): Parsed yaml file as a dictionary

    """
    try:
        with open(yaml_path) as file:
            content = yaml.safe_load(file)
            logger.info(f"yaml file: {yaml_path} laoded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml loader failed")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_of_directories: list[Path], verbose = True):
    """ create a list of dictionaries

    Args:
        path_of_directories: list of paths of directories to be made as Path()

    Outputs:
        None
    
    """
    for dir_path in path_of_directories:
        try:
            os.makedirs(dir_path, exist_ok = True)
            if verbose:
                logger.info(f"created directory at: {dir_path}")
        except:
            logger.warning(f"creating directory at:{dir_path} failed")


@ensure_annotations
def save_json(json_data:Dict, json_path:Path):
    """ save json data

    Args:
        json_data (dict): data to be saved in json file
        json_path (Path): path to json file

    Outputs:
        None
    """
    try:
        with open(json_path, "w") as f:
            json.dump(json_data, f, indent = 2)
        logger.info(f"json file saved at {json_path}")
    except:
        logger.warning(f"json saving to:{json_path} failed")



@ensure_annotations
def load_json(json_path: Path) -> Dict:
    """ load json files to a dictionary format
    
    Args:
        json_path: path to load the json from
    Output:
        content: loaded json in dictionary format 
    """
    try:
        with open(json_path) as f:
            content = json.load(json_path)
        return ConfigBox(content)
    except:
        logger.warning(f"loading json from {json_path} failed")

    

@ensure_annotations
def save_model(model:Any, model_save_path: Path, model_save_type:str = "joblib"):
    """save the model binary file

    Args:
        model: model type (.joblib, .pkl, .onnx)
        model_save_path: save folder path as Path()
        model_save_type: (.joblib, .pkl, .onnx) defaults to .joblib

    Outputs:
        saves model as specified at model_save_path
    
    """
    #TODO : Allow saving as .pkl and .onnx (universal helper)
    try:
        if model_save_type == "joblib":
            joblib.dump(value = model, filename = model_save_path)

        logger.info(f"model file saved at {model_save_path} as {model_save_type}")
    except:
        logger.error(f"model file saving at {model_save_path} as {model_save_type} failed")




@ensure_annotations
def load_model(model_load_path: Path, model_load_type:str = "joblib"):
    """loads saved model
    
    Args:
        model_load_path: 
        model_load_type: ,defaults to joblib
    Outputs:
        model of the model_type specified, defaults to joblib
    """
    try:
        #TODO: Allow loading as other possbilities
        if model_load_type == "joblib":
            model = joblib.load(model_load_path)
            logger.info(f"model at {model_load_path} loaded successfully")
            return model
    except:
        logger.error(f"model loading failed from {model_load_path}")
    