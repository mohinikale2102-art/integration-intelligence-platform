import json
from app import repository as repo
from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.services.simulator import timestamp

def investigate(event):
    response = json.loads(event["response_payload"] or "{}")
    code = event["http_status"]
    evidence = [
        f"The receiving application returned HTTP {code}.",
        f"Event type: {event['event_type']}.",
        f"Source: {event['source']}; destination: {event['destination']}."
    ]
    if code == 400:
        missing = response.get("missing_fields", [])
        cause = "The receiver rejected the payload because required fields are missing."
        if missing:
            evidence.append("Missing fields reported by the receiver: " + ", ".join(missing) + ".")
        steps = ["Compare the outgoing payload with the receiver's required schema.",
                 "Check the source-to-destination field mapping.",
                 "Correct the payload and retry after reviewing the change."]
    elif code in (401, 403):
        cause = "The receiving application rejected the request because authentication or authorization was not accepted."
        steps = ["Verify the configured credential and authentication method.",
                 "Check whether the credential is active and has the required permissions.",
                 "Retry only after correcting the authentication issue."]
    elif code == 504:
        cause = "The receiving application did not respond within the allowed time."
        evidence.append("The receiver returned a gateway timeout.")
        steps = ["Check receiver availability and processing time.",
                 "Review network and timeout settings.",
                 "Retry after confirming the receiver is healthy."]
    else:
        cause = "The receiving application did not accept the event."
        steps = ["Inspect the request and response payloads.", "Review receiver-side application logs."]
    summary = f"The integration event failed with HTTP {code}. {cause}"
    provider = "rules"
    if GEMINI_API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = (
                "Explain this integration failure using only supplied evidence. Separate facts from likely causes. "
                "Do not claim that a fix was applied. Give concise investigation guidance.\n\n"
                + json.dumps({"event": event, "evidence": evidence, "cause": cause, "steps": steps}, indent=2)
            )
            result = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            if result.text:
                summary = result.text.strip()
                provider = "gemini"
        except Exception:
            provider = "rules_fallback"
    repo.save_investigation(event["id"], summary, evidence, cause, steps, provider, timestamp())
    return repo.investigation(event["id"])
