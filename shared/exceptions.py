from fastapi import FastAPI
class NotFoundExecption(Exception):
    def __init__(self, name: str):
        self.name = name
