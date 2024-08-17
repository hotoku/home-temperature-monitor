from datetime import datetime

from pydantic import BaseModel


class SwitchBotCredential(BaseModel):
    token: str
    secret: str
    device_id: str


class Observation(BaseModel):
    battery: int
    deviceId: str
    deviceType: str
    humidity: float
    temperature: float
    version: str


class SwitchBotResponse(BaseModel):
    body: Observation
    message: str
    statusCode: int


class SensorInfo(BaseModel):
    battery: int
    temperature: float
    humidity: float
    created_at: datetime
