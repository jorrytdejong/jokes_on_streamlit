from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


@dataclass(frozen=True)
class HumorTemplate:
    key: str
    name: str
    description: str
    prompt_focus: str
    examples: tuple[tuple[str, str], ...]


def _secret_or_env(name: str) -> str | None:
    try:
        if name in st.secrets:
            value = st.secrets[name]
            if value is not None and str(value).strip():
                return str(value).strip()
    except Exception:
        pass

    value = os.getenv(name)
    if value is not None and value.strip():
        return value.strip()
    return None


def _default_model() -> str:
    return _secret_or_env("OPENAI_MODEL") or "gpt-4o-mini"


def _build_user_prompt(template: HumorTemplate, seed: str) -> str:
    examples_text = "\n".join(
        [f'Input: "{example_input}"\nJoke: "{example_joke}"' for example_input, example_joke in template.examples]
    )
    return (
        f"Humor type: {template.name}\n"
        f"Style brief: {template.prompt_focus}\n\n"
        f"{examples_text}\n\n"
        f'Now write one new joke for this input: "{seed}"\n'
        "Rules:\n"
        "- Return only the joke text.\n"
        "- Keep it to 1-3 sentences.\n"
        "- Keep the style faithful to the humor type.\n"
        "- No explanations, no labels.\n"
    )


def _extract_output_text(response: object) -> str:
    direct = getattr(response, "output_text", "")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()

    output = getattr(response, "output", None)
    if not output:
        return ""

    chunks: list[str] = []
    for item in output:
        content_items = getattr(item, "content", []) or []
        for content in content_items:
            text = getattr(content, "text", "")
            if isinstance(text, str) and text.strip():
                chunks.append(text)

    return "\n".join(chunks).strip()


def _call_openai(template: HumorTemplate, seed: str) -> str:
    if OpenAI is None:
        raise RuntimeError(
            "The 'openai' package is not installed. Run: pip install -r requirements.txt"
        )

    api_key = _secret_or_env("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Add it to .streamlit/secrets.toml or environment variables."
        )

    client = OpenAI(api_key=api_key)
    try:
        response = client.responses.create(
            model=_default_model(),
            max_output_tokens=180,
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "You are a joke writer. Produce one concise joke that matches "
                                "the requested humor style."
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": _build_user_prompt(template, seed),
                        }
                    ],
                },
            ],
        )
    except Exception as error:  # pragma: no cover
        raise RuntimeError(f"OpenAI request failed: {error}") from error

    output = _extract_output_text(response)
    if not output:
        raise RuntimeError("OpenAI returned an empty response.")
    return output


def echo_input(text: str) -> str:
    return text.strip()


def extend_input(text: str, add_on: str) -> str:
    base = echo_input(text)
    extra = echo_input(add_on)

    if base and extra:
        return f"{base} {extra}"
    if base:
        return base
    if extra:
        return extra
    return "absolutely nothing"


_TEMPLATES = [
    HumorTemplate(
        key="domheid",
        name="Domheid (Stupidity)",
        description="Laughing at foolish behavior or pretending to be foolish.",
        prompt_focus="Mock naive logic and obvious bad decisions in a playful way.",
        examples=(
            (
                "I tried to fix the printer by whispering positive affirmations.",
                "I told the printer it was doing amazing and it rewarded me by printing in invisible ink.",
            ),
            (
                "We forgot the password and guessed 'password'.",
                "The system locked us out for security, which was fair because our strategy was a crime scene.",
            ),
        ),
    ),
    HumorTemplate(
        key="zelfspot",
        name="Zelfspot (Self-mockery)",
        description="Making fun of yourself with insight and confidence.",
        prompt_focus="Make the speaker the target of the joke, with honest self-mockery.",
        examples=(
            (
                "I made a five-step plan to wake up earlier.",
                "I built a perfect morning routine and then slept through the alarm with professional commitment.",
            ),
            (
                "I said I would keep the project simple.",
                "My idea of simple now has color coding, versioning, and an emergency spreadsheet.",
            ),
        ),
    ),
    HumorTemplate(
        key="primitieve_humor",
        name="Primitieve humor (Primitive humor)",
        description="Basic, physical, or taboo humor that breaks etiquette.",
        prompt_focus="Use physical clumsiness and lowbrow silliness without explicit vulgar content.",
        examples=(
            (
                "I entered the room with confidence.",
                "I slipped on nothing, waved like it was choreography, and called it a soft landing.",
            ),
            (
                "I tried to act classy at dinner.",
                "One sneeze later I looked like modern art and everyone pretended not to see it.",
            ),
        ),
    ),
    HumorTemplate(
        key="zwarte_humor",
        name="Zwarte humor (Black humor)",
        description="Joking about heavy themes to cope with tension.",
        prompt_focus="Use dark but non-hateful humor about stress, doom, and survival.",
        examples=(
            (
                "My calendar is full this week.",
                "My free time now exists only as a memorial service between two meetings.",
            ),
            (
                "I checked my deadline.",
                "The deadline looked back at me like we were both aware only one of us would survive.",
            ),
        ),
    ),
    HumorTemplate(
        key="ironie",
        name="Ironie (Irony)",
        description="Saying the opposite of what is meant in a playful way.",
        prompt_focus="Praise a bad outcome as if it were excellent.",
        examples=(
            (
                "I deployed on Friday evening.",
                "Brilliant timing. Nothing says relaxation like emergency bug triage at midnight.",
            ),
            (
                "I skipped testing to save time.",
                "Fantastic efficiency. I only spent the rest of the night testing in production.",
            ),
        ),
    ),
    HumorTemplate(
        key="leedvermaak",
        name="Leedvermaak (Schadenfreude)",
        description="Enjoying another person's harmless mishap.",
        prompt_focus="Find comic relief in someone else's minor, harmless failure.",
        examples=(
            (
                "My colleague presented with total confidence.",
                "When slide two opened upside down, I felt bad for three seconds and then took notes for my own mistakes.",
            ),
            (
                "Someone bragged they never typo.",
                "They wrote 'pubic release' in the company chat, and suddenly humility became a team value.",
            ),
        ),
    ),
    HumorTemplate(
        key="taalhumor",
        name="Taalhumor (Language humor)",
        description="Wordplay, ambiguity, and jokes around phrasing.",
        prompt_focus="Use puns, double meaning, or playful phrasing.",
        examples=(
            (
                "They said to break a leg before my talk.",
                "I delivered safely, but my confidence still needed a cast.",
            ),
            (
                "I asked for constructive feedback.",
                "They were so constructive they rebuilt my entire personality.",
            ),
        ),
    ),
    HumorTemplate(
        key="overdrijving",
        name="Overdrijving (Exaggeration)",
        description="Stretching reality to absurd scale for effect.",
        prompt_focus="Amplify details to ridiculous proportions.",
        examples=(
            (
                "I sent one reminder email.",
                "Within minutes, three departments, two satellites, and my grandmother were aware of the update.",
            ),
            (
                "I had a small delay.",
                "By the time I finished, archaeologists classified the task as a lost civilization.",
            ),
        ),
    ),
    HumorTemplate(
        key="understatement",
        name="Understatement",
        description="Deliberately downplaying a big event.",
        prompt_focus="Describe chaos as if it were mildly inconvenient.",
        examples=(
            (
                "The server crashed during launch.",
                "We had a tiny hiccup if your definition of tiny includes public panic and six phone calls from management.",
            ),
            (
                "Our demo failed live.",
                "It was a slightly imperfect moment, followed by a brief silence measured in geological time.",
            ),
        ),
    ),
    HumorTemplate(
        key="slimme_observatie",
        name="De slimme observatie (Clever observation)",
        description="Pointing out odd things in normal daily behavior.",
        prompt_focus="Highlight an everyday social absurdity in 'have you noticed' style.",
        examples=(
            (
                "Team meetings start at 9:00.",
                "Why is every 9:00 meeting actually a 9:07 meeting with seven people saying, 'Can you hear me?'",
            ),
            (
                "People say they are quick on email.",
                "Have you noticed 'quick reply' usually means after you've sent the third polite follow-up?",
            ),
        ),
    ),
    HumorTemplate(
        key="plotselinge_ommezwaai",
        name="De plotselinge ommezwaai (Sudden twist)",
        description="Setting expectation, then sharply breaking it.",
        prompt_focus="Build a pattern then break it with a surprising final turn.",
        examples=(
            (
                "I had a perfect plan for my day.",
                "I prioritized, scheduled, optimized, and then spent two hours choosing a font.",
            ),
            (
                "I prepared three backup options.",
                "Plan A failed, Plan B failed, and Plan C taught me how to make tea under pressure.",
            ),
        ),
    ),
    HumorTemplate(
        key="verkeerde_opmerking",
        name="De verkeerde opmerking (Inappropriate remark)",
        description="Breaking social etiquette with blunt or shocking comments.",
        prompt_focus="Use blunt honesty that breaks politeness, without hateful or abusive language.",
        examples=(
            (
                "They asked for honest feedback on a confusing presentation.",
                "I said, 'Great mystery novel, but when does the data arrive?' and the room discovered silence.",
            ),
            (
                "Someone said this could have been an email.",
                "I replied, 'It still can,' and suddenly I was not invited to the follow-up.",
            ),
        ),
    ),
    HumorTemplate(
        key="cirkelhumor",
        name="Cirkelhumor (Circular humor)",
        description="Paradoxes, loops, and self-referential joke logic.",
        prompt_focus="Use circular logic or a self-referential paradox.",
        examples=(
            (
                "I stopped overthinking by analyzing less.",
                "I made a detailed plan for not making detailed plans, and it worked until I reviewed it twice.",
            ),
            (
                "I wrote a note to be more spontaneous.",
                "Now every spontaneous moment is scheduled between two reminders to relax naturally.",
            ),
        ),
    ),
    HumorTemplate(
        key="antihumor",
        name="Antihumor",
        description="Intentionally flat jokes or no punchline at all.",
        prompt_focus="Deliver a plain, intentionally unexciting anti-joke.",
        examples=(
            (
                "Why did I open the document?",
                "To read it. Then I closed it.",
            ),
            (
                "I expected a big plot twist today.",
                "Nothing happened. Lunch was acceptable.",
            ),
        ),
    ),
]

TEMPLATES_BY_KEY = {template.key: template for template in _TEMPLATES}


def template_list() -> list[HumorTemplate]:
    return _TEMPLATES


def template_keys() -> list[str]:
    return [template.key for template in _TEMPLATES]


def get_template(template_key: str) -> HumorTemplate:
    if template_key not in TEMPLATES_BY_KEY:
        raise KeyError(f"Unknown template key: {template_key}")
    return TEMPLATES_BY_KEY[template_key]


def generate_joke(template_key: str, user_input: str, add_on: str) -> str:
    template = get_template(template_key)
    seed = extend_input(user_input, add_on)
    return _call_openai(template, seed)
