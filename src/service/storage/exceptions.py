class StorageNotFound(FileNotFoundError):
    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.filepath = filepath
