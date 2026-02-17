from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class HumorTemplate:
    key: str
    name: str
    description: str
    generator: Callable[[str], str]


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


def _domheid(seed: str) -> str:
    endings = [
        "They nodded and asked if that was the advanced strategy.",
        "Someone wrote it down as a best practice.",
        "The loudest person in the room called it genius.",
    ]
    return f'I said my plan was "{seed}". {random.choice(endings)}'


def _zelfspot(seed: str) -> str:
    endings = [
        "I am not saying I overcomplicate things, but I need a flowchart to make tea.",
        "My confidence level is high, my execution level is still buffering.",
        "I bring chaos to projects and snacks to meetings, so it balances out.",
    ]
    return f'For "{seed}", I trusted myself. {random.choice(endings)}'


def _primitieve_humor(seed: str) -> str:
    endings = [
        "Then I tripped over nothing and blamed gravity for poor teamwork.",
        "A dramatic sound effect happened in my head and that counted as progress.",
        "At some point I made a face that should come with a warning label.",
    ]
    return f'"{seed}" sounded classy. {random.choice(endings)}'


def _zwarte_humor(seed: str) -> str:
    endings = [
        "My schedule held a memorial for free time.",
        "The deadline and I now have a very complicated relationship.",
        "My to-do list now has a chapter called survival mode.",
    ]
    return f'I approached "{seed}" with optimism. {random.choice(endings)}'


def _ironie(seed: str) -> str:
    endings = [
        "Absolutely perfect, if your goal is mild disaster.",
        "Everything went exactly as planned by my worst ideas.",
        "Flawless execution, in the sense that every flaw executed.",
    ]
    return f'"{seed}" was easy. {random.choice(endings)}'


def _leedvermaak(seed: str) -> str:
    endings = [
        "Someone else made the same mistake first, which was deeply educational.",
        "I learned from a stranger's blooper reel and called it research.",
        "Watching someone else fail gave me confidence I did not earn.",
    ]
    return f'While working on "{seed}", {random.choice(endings)}'


def _taalhumor(seed: str) -> str:
    endings = [
        "People said it was a piece of cake, so I brought cake and no results.",
        "I asked for feedback and got feed-forward, so now my problems are in the future.",
        "It was all about context, and I still took it out of context.",
    ]
    return f'I used clever wording for "{seed}". {random.choice(endings)}'


def _overdrijving(seed: str) -> str:
    endings = [
        "It took seventeen tabs, nine snacks, and one emotional support playlist.",
        "By the end, historians were taking notes.",
        "I told one person and suddenly it became international news in my group chat.",
    ]
    return f'I worked on "{seed}" for a minute. {random.choice(endings)}'


def _understatement(seed: str) -> str:
    endings = [
        "It was slightly intense, if by slight you mean cinematic.",
        "There were a few tiny issues, roughly the size of a mountain.",
        "Nothing dramatic happened, except for all the drama.",
    ]
    return f'"{seed}" went fine. {random.choice(endings)}'


def _slimme_observatie(seed: str) -> str:
    endings = [
        "Why does everyone say a quick meeting and then unpack their life story?",
        "Why do we call it multitasking when it is just panic with tabs?",
        "Why does every simple task require one update, two reminders, and a miracle?",
    ]
    return f'I started "{seed}" and noticed this: {random.choice(endings)}'


def _plotselinge_ommezwaai(seed: str) -> str:
    endings = [
        "Step one: focus. Step two: plan. Step three: buy a ukulele.",
        "I made a list: start early, stay calm, accidentally become a detective.",
        "Everything made sense until the sentence ended with a llama.",
    ]
    return f'For "{seed}", I had a solid structure. {random.choice(endings)}'


def _verkeerde_opmerking(seed: str) -> str:
    endings = [
        "I said exactly what everyone thought and nobody invited me back.",
        "It was honest, unnecessary, and technically correct.",
        "My inside voice took a day off.",
    ]
    return f'During "{seed}", I made a bold comment. {random.choice(endings)}'


def _cirkelhumor(seed: str) -> str:
    endings = [
        'I stopped doing it to be efficient, which gave me time to do it again.',
        "I solved the problem by proving the problem still existed.",
        "The conclusion was the same as the introduction, but with more confidence.",
    ]
    return f'"{seed}" taught me circular logic: {random.choice(endings)}'


def _antihumor(seed: str) -> str:
    endings = [
        "Then I completed it and that was the whole story.",
        "There was no punchline. The task simply ended.",
        "Nothing unexpected happened, which was unexpectedly nice.",
    ]
    return f'Why did I do "{seed}"? Because it was on my list. {random.choice(endings)}'


_TEMPLATES = [
    HumorTemplate(
        key="domheid",
        name="Domheid (Stupidity)",
        description="Laughing at foolish behavior or pretending to be foolish.",
        generator=_domheid,
    ),
    HumorTemplate(
        key="zelfspot",
        name="Zelfspot (Self-mockery)",
        description="Making fun of yourself with insight and confidence.",
        generator=_zelfspot,
    ),
    HumorTemplate(
        key="primitieve_humor",
        name="Primitieve humor (Primitive humor)",
        description="Basic, physical, or taboo humor that breaks etiquette.",
        generator=_primitieve_humor,
    ),
    HumorTemplate(
        key="zwarte_humor",
        name="Zwarte humor (Black humor)",
        description="Joking about heavy themes to cope with tension.",
        generator=_zwarte_humor,
    ),
    HumorTemplate(
        key="ironie",
        name="Ironie (Irony)",
        description="Saying the opposite of what is meant in a playful way.",
        generator=_ironie,
    ),
    HumorTemplate(
        key="leedvermaak",
        name="Leedvermaak (Schadenfreude)",
        description="Enjoying another person's harmless mishap.",
        generator=_leedvermaak,
    ),
    HumorTemplate(
        key="taalhumor",
        name="Taalhumor (Language humor)",
        description="Wordplay, ambiguity, and jokes around phrasing.",
        generator=_taalhumor,
    ),
    HumorTemplate(
        key="overdrijving",
        name="Overdrijving (Exaggeration)",
        description="Stretching reality to absurd scale for effect.",
        generator=_overdrijving,
    ),
    HumorTemplate(
        key="understatement",
        name="Understatement",
        description="Deliberately downplaying a big event.",
        generator=_understatement,
    ),
    HumorTemplate(
        key="slimme_observatie",
        name="De slimme observatie (Clever observation)",
        description="Pointing out odd things in normal daily behavior.",
        generator=_slimme_observatie,
    ),
    HumorTemplate(
        key="plotselinge_ommezwaai",
        name="De plotselinge ommezwaai (Sudden twist)",
        description="Setting expectation, then sharply breaking it.",
        generator=_plotselinge_ommezwaai,
    ),
    HumorTemplate(
        key="verkeerde_opmerking",
        name="De verkeerde opmerking (Inappropriate remark)",
        description="Breaking social etiquette with blunt or shocking comments.",
        generator=_verkeerde_opmerking,
    ),
    HumorTemplate(
        key="cirkelhumor",
        name="Cirkelhumor (Circular humor)",
        description="Paradoxes, loops, and self-referential joke logic.",
        generator=_cirkelhumor,
    ),
    HumorTemplate(
        key="antihumor",
        name="Antihumor",
        description="Intentionally flat jokes or no punchline at all.",
        generator=_antihumor,
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
    return template.generator(seed)
