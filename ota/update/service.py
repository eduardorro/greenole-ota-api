from version.service import VersionService
from utils.celery import app
from device.models import Device

class UpdateService:
    def __init__(self, update) -> None:
        self.update = update
    
    def save(self):
        self.update.save()
        
        if self.update.all_devices:
            self.update.devices.set(Device.objects.all(), through_defaults={'status': 4})

    def run(self):
        vs = VersionService(self.update.version)
        payload = vs.get_version_payload()
        result = {'payload': payload, 'update_id': self.update.id, 'info': []}

        for d in self.update.devices.all():
            result['info'].append({
                'out_topic': d.get_out_topic(),
                'ack_topic':d.get_ack_topic(),
                "device_id": d.id
            })

        app.send_task(
            "send_update",
            kwargs=result
        )
