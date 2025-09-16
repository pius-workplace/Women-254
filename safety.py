from typing import Dict, Tuple, Optional

EMERGENCY_KEYWORDS = {
    "english": ["help", "unsafe", "in danger", "stalking", "stalker", "rape", "assault", "violence",
                "domestic", "abuse", "harassment", "sos", "panic", "kidnap", "threat", "blackmail",
                "emergency", "attacked", "hurt"],
    "swahili": ["msaada", "hatari", "niko hatarini", "ninahitaji msaada", "ubakaji", "unanyanyaswa",
                "kudhulumiwa", "kupigwa", "unyanyasaji", "tishio", "hatari ya maisha", "misheni"],
    "sheng": ["niko kwa shida", "nisaidie", "danger", "mbaya", "amekam", "ananishow", "ananiforce",
              "niko tight", "wamenishika", "shida kubwa"]
}

def detect_emergency(text: str) -> bool:
    if not text or not isinstance(text, str):
        return False
    t = text.lower().strip()
    for lang_keywords in EMERGENCY_KEYWORDS.values():
        for kw in lang_keywords:
            if kw in t:
                return True
    return False

def emergency_response() -> Dict[str, str]:
    return {
        "en": ("If you are in immediate danger, call **999** (Kenya Police) now. "
               "You can also reach the **GBV Toll‑Free Helpline 1195**. "
               "If safe, share your location with a trusted person. "
               "This chat is anonymous; no data is stored."),
        "sw": ("Ukiwa kwenye hatari sasa, pigia **999** (Polisi wa Kenya) mara moja. "
               "Pia unaweza kupiga **1195** – Huduma ya GBV bila malipo. "
               "Ikiwa ni salama, shiriki eneo lako na mtu unayemuamini. "
               "Mazungumzo haya ni ya siri; hakuna taarifa inayohifadhiwa."),
        "sheng": ("Kama ni urgent, pigia **999** saa hii. Pia kuna **1195** ya GBV – free. "
                  "Kama ni poa, tuma location kwa mtu wako wa kuamini. "
                  "Hii chat ni anonymous; hatu-hifadhi details zako.")
    }

SAFETY_BY_DESIGN = """
- No storage of personal identifiers by default.
- Anonymous mode; logs redact names, phones, GPS.
- Escalation: emergency keyword detection → show hotlines first before any other reply.
- Dignity & privacy: trauma‑informed language, non‑judgmental tone.
- Inclusivity: support English, Swahili, and Sheng.
- Content moderation: Block harmful or explicit responses.
- Rate limiting: Prevent abuse by limiting requests per user.
- Audit trail: Log interactions (anonymized) for safety review.
"""

def validate_safety_response(response: str) -> Tuple[bool, Optional[str]]:
    unsafe_keywords = ["kill", "hurt", "violence", "explicit", "illegal"]
    if any(kw in response.lower() for kw in unsafe_keywords):
        return False, "Response contains potentially harmful content."
    if "personal data" in response.lower() or "location" in response.lower():
        return False, "Response inadvertently shares personal data."
    return True, None