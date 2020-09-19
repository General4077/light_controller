from .pi_controller import RunLights

with RunLights() as control:
    control.refresh(10)