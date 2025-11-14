"""Plugin directory for organisation-specific cleaning logic.

Custom modules should expose a META dict and a process(df, **kwargs) callable.
The PipelineManager dynamically imports every .py file inside this folder.
"""
