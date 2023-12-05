class DatabaseManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def append_to_file(self, content):
        try:
            with open(self.file_path, 'a') as file:
                file.write(content + '\n')
        except Exception as e:
            print(f'Error appending to {self.file_path}: {str(e)}')

