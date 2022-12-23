from dataclasses import dataclass, asdict

import requests

@dataclass()
class RingLightStatus:
    on: int
    brightness: int
    temperature: int

    def __repr__(self):
        return (
            f"power: {self.on} | "
            f"brightness: {self.brightness} | "
            f"temperature: {self.temperature} "
        )

class RingLight:

    RING_LIGHT_HOST = "http://robringlight.home:9123"
    API = f"{RING_LIGHT_HOST}/elgato/lights"

    def current_settings(self) -> RingLightStatus:
        data = requests.get(RingLight.API).json()
        return RingLightStatus(**data['lights'][0])

    def send_settings(self, settings: RingLightStatus) -> RingLightStatus:
        data = {
                "numberOfLights": 1,
                "lights": [asdict(settings)]
            }
        
        resp = requests.put(
            RingLight.API,
            json=data,
        )
        resp.raise_for_status()

        return RingLightStatus(**resp.json()['lights'][0])
