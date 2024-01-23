from fastapi import HTTPException
from configs.logger import logger

class ManageBody:
    def clean_str(self, value:str, key, keys_str_split) -> str:
        if type(value) == str:
            if key in keys_str_split:
                self.__dict__[key] = ' '.join(value.split())
            else:
                self.__dict__[key] = value.strip()
    
    def clean_int(self, value:str, key, keys) -> str:
        try: 
            if key in keys:
                int(value)
        except:
            logger.error(f"{key} must be number.")
            raise HTTPException(status_code=400, detail=f"{key} must be number.")
    
    def check_is_empty(self, value:str, key, keys) -> str:
        if type(value) == str and not value and key in keys:
            logger.error(f"{key} not provided.")
            raise HTTPException(status_code=400, detail=f"{key} not provided.")
    
    # check key empty and delete spaces
    def clean_model(self, keys_require:list = [], keys_int:list = [], keys_str_split:list = []):
        for key, value in self.__dict__.items():
            self.clean_str(value, key, keys_str_split)
            self.check_is_empty(value, key, keys_require)
            self.clean_int(value, key, keys_int)