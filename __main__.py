from .pi_controller import RunLights

REST_MINUTES = 10

with RunLights() as control:
    while True:
        control.refresh(REST_MINUTES)