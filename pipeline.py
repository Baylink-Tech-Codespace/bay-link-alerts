from typing import Dict, Any, Callable
from notification import send_alert
from database.models.BaylinkAlertLogs import BaylinkAlertLogs
from database.db import db
import config

class AlertSystem:
    def __init__(self):
        pass

    def send_log_to_db(self, message: str, data: Dict[str, Any]):
        session = db.get_session()
        retailer_id = data['retailer_id']
    
        try:
            log_entry = BaylinkAlertLogs(
                retailer_id=retailer_id,
                message=message,
                data=data, 
            )
            session.add(log_entry)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Failed to log alert to DB: {e}")
        finally:
            session.close()

    def alert_pipeline(self, event_name: str, event_data: Dict[str, Any]): 
        if event_name in config.ALERT_RULES: 
            condition: Callable[[Dict[str, Any]], bool] = config.ALERT_RULES[event_name]
        
            if condition(event_data):
                message = event_data['message']
                recipient = event_data['recepient'] 
                send_alert(message, recipient)
                self.send_log_to_db(message, event_data)

alert_system = AlertSystem()