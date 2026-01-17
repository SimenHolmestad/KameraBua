from .base_run_config import BaseRunConfig


class Build(BaseRunConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.build_frontend()
