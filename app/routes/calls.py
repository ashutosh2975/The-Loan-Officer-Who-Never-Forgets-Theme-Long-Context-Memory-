from fastapi import APIRouter, Request
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Store calls in memory (just for this session)
calls_log = {}

@router.post("/vapi/webhook")
async def vapi_webhook(request: Request):
    try:
        body = await request.json()
    except Exception:
        return {"status": "invalid json"}

    event_type = body.get("message", {}).get("type", "")

    if event_type == "call-start":
        return await handle_call_start(body)

    elif event_type == "transcript":
        return await handle_transcript(body)

    elif event_type == "end-of-call-report":
        return await handle_call_end(body)

    return {"status": "ignored"}


async def handle_call_start(body: dict):
    msg   = body.get("message", {})
    call  = msg.get("call", {})
    call_id = call.get("id", "unknown")

    calls_log[call_id] = []

    print("\n")
    print("=" * 60)
    print(f"📞  CALL STARTED")
    print(f"    Call ID : {call_id}")
    print(f"    Phone   : {call.get('customer', {}).get('number', 'web call')}")
    print("=" * 60)

    return {"status": "ok"}


async def handle_transcript(body: dict):
    msg     = body.get("message", {})
    call    = msg.get("call", {})
    call_id = call.get("id", "unknown")
    role    = msg.get("role", "unknown")
    text    = msg.get("transcript", "").strip()

    if not text:
        return {"status": "empty"}

    # Save to memory
    if call_id not in calls_log:
        calls_log[call_id] = []
    calls_log[call_id].append({"role": role, "text": text})

    # Print to terminal nicely
    if role == "user":
        print(f"\n  🧑 USER      : {text}")
    else:
        print(f"  🤖 ASSISTANT : {text}")

    return {"status": "ok"}


async def handle_call_end(body: dict):
    msg      = body.get("message", {})
    call     = msg.get("call", {})
    call_id  = call.get("id", "unknown")
    duration = int(msg.get("durationSeconds", 0))
    full     = msg.get("transcript", "")

    print("\n")
    print("=" * 60)
    print(f"📵  CALL ENDED")
    print(f"    Call ID  : {call_id}")
    print(f"    Duration : {duration} seconds")
    print("=" * 60)
    print("\n📄  FULL TRANSCRIPT:")
    print("-" * 60)
    print(full if full else "No transcript available")
    print("-" * 60)
    print("\n")

    return {"status": "ok"}