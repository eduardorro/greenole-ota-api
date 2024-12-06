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
        result = {'payload': payload, 'info': []}

        for v in self.update.versions:
            result['info'].append({
                'out_topic': v.device.get_out_topic(),
                'ack_topic':v.device.get_ack_topic(),
                "update_id": v.id
            })

        app.send_task(
            "send_update",
            kwargs=result
        )
