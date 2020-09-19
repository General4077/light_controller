from .pi_controller import RunLights

with RunLights() as control:
    for _ in range(2):
        control.refresh(10)