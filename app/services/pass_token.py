import hashlib
import hmac
import io
import time
import uuid

import segno


def create_dynamic_pass(secret: str, profile_id: int, trip_id: int) -> tuple[str, str]:
    nonce = uuid.uuid4().hex
    raw = f"{profile_id}:{trip_id}:{int(time.time())}:{nonce}"
    digest = hmac.new(secret.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()
    token = f"ELDER-{digest[:28]}"

    qr = segno.make(token)
    output = io.BytesIO()
    qr.save(output, kind="svg", scale=5, border=2)
    return token, output.getvalue().decode("utf-8")
