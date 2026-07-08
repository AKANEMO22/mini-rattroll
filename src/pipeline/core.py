from typing import List
from src.interfaces.base import PipelineStep
from src.core.contexts import PipelineContext

class Pipeline:
    """Core Pipeline Engine to execute sequential steps."""
    def __init__(self):
        self._steps: List[PipelineStep] = []

    def add_step(self, step: PipelineStep):
        self._steps.append(step)

    def run(self, context: PipelineContext) -> PipelineContext:
        for step in self._steps:
            step.execute(context)
        return context
