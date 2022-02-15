import hashlib
import hmac
from typing import Dict


def _generate_signature(self, data: Dict) -> str:
    ordered_data = self._order_params(data)
    query_string = '&'.join([f"{d[0]}={d[1]}" for d in ordered_data])
    m = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
    return m.hexdigest()