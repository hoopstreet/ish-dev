import os

class FileInjector:
    @staticmethod
    def inject(project_path, filename, content):
        full_path = os.path.join(project_path, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return f"Successfully injected {filename} into {project_path}"
