import logging
from datetime import datetime

import aiocomfoconnect.sensors
from aiocomfoconnect import ComfoConnect 

from aiocomfoconnect.exceptions import (
    AioComfoConnectNotConnected,
    AioComfoConnectTimeout,
    ComfoConnectError,
    ComfoConnectNotAllowed,
)

from comfobridge.measurement import Measurement
from comfobridge.reporting import Reporting

logger = logging.getLogger(__name__)

class Ventilation:
    def __init__(self, comfoconnect_host, uuid, local_uuid, sensor_callback, reporting: Reporting):
        self.comfoconnect = ComfoConnect(comfoconnect_host, uuid, sensor_callback=self.filter)
        self.local_uuid = local_uuid
        self.sensor_callback_fn = sensor_callback
        self.reporting = reporting

    async def connect(self):
        logger.info("Connecting to ComfoConnect...")
        await self.comfoconnect.connect(self.local_uuid)


class Ventilation:
    def __init__(self, bridge_host, bridge_pin, bridge_uid, app_uuid ,app_id , sensor_callback, reporting: Reporting):
        self.bridge_uid = bridge_uid
        self.bridge_host = bridge_host
        self.bridge_pin = bridge_pin
        self.app_uuid = app_uuid
        self.app_id = app_id
        self.comfoconnect = ComfoConnect(self.bridge_host, self.bridge_uid , sensor_callback=self.filter)
        self.sensor_callback_fn = sensor_callback
        self.reporting = reporting
     #   self.last_measurement = {}

    async def connect(self):
        try:
            logger.info("Connecting to ComfoConnect...")
            await self.comfoconnect.connect(self.app_uuid)
        except ComfoConnectNotAllowed:
            logger.info("....Access denied")
            logger.info("Try to register...")
            #await self.register_to_bridge(self)
            #logger.info("Connecting to ComfoConnect again ...")
            #await self.comfoconnect.connect(self.local_uuid)

    async def register_all_sensors(self):
        for key in aiocomfoconnect.sensors.SENSORS:
            logger.info("Registering sensor %s", key)
            await self.comfoconnect.register_sensor(aiocomfoconnect.sensors.SENSORS[key])

    async def register_sensors(self, sensors):
        for sensor in sensors:
            logger.info("Registering sensor %s", sensor)
            await self.comfoconnect.register_sensor(aiocomfoconnect.sensors.SENSORS[sensor])

    async def keepalive(self):
        logger.debug("Keeping alive...")
        await self.comfoconnect.cmd_keepalive()

    async def disconnect(self):
        logger.debug("Disconnecting from ComfoConnect...")
        await self.comfoconnect.disconnect()

    def filter(self, sensor, value):
        #if self.reporting.should_report(Measurement(timestamp=datetime.now(), sensor=sensor, value=value)):
        #    self.sensor_callback_fn(sensor, value)
        # if (value != 0) or (self.last_measurement[measurement.sensor.id] == 0): # filtre les 0 unitaires accidentel ne marche pas avec bypass par exemple.
        #    self.last_measurement[measurement.sensor.id] = measurement
        if self.reporting.should_report(Measurement(timestamp=datetime.now(), sensor=sensor, value=value)):
            self.sensor_callback_fn(sensor, value)
