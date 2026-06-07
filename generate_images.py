"""Generera varma, ömsinta illustrationer till Maries förlossningskurs.

Återanvänder GLAS aicontentgenerator-skillens Gemini-tjänst (ingen rå curl).
Kör med skillens venv:
  GOOGLE_API_KEY=$(cat ~/.config/glas/gemini-api-key) \
  /Users/christoffersundberg/Projects/glaseyewear/content/.claude/skills/aicontentgenerator/.venv/bin/python generate_images.py
"""
import asyncio
import os
import sys
from pathlib import Path

SKILL = Path("/Users/christoffersundberg/Projects/glaseyewear/content/.claude/skills/aicontentgenerator")
sys.path.insert(0, str(SKILL))

from services import gemini  # noqa: E402

MODEL = "gemini-3-pro-image-preview"
OUT = Path("/Users/christoffersundberg/Projects/marie-forlossningskurs/images")
OUT.mkdir(parents=True, exist_ok=True)

STYLE = (
    "Soft, tender hand-painted gouache-style illustration. Warm, intimate, reassuring mood. "
    "Limited cohesive palette: warm cream background, terracotta, soft blush pink, sage green, "
    "muted gold ochre. Gentle rounded organic shapes, soft edges, subtle paper-grain texture, "
    "painterly. Minimal and uncluttered with generous negative space. Calm and editorial. "
    "A warm, tender expecting couple. "
    "ABSOLUTELY NO text, no letters, no words, no numbers, no captions anywhere in the image."
)

SCENES = {
    "01-hero": "An expecting couple in a tender embrace, the partner's hand resting gently on the pregnant belly, soft warm light, hopeful and calm.",
    "03-start": "A calm pregnant woman at home leaning on a kitchen counter during an early contraction, her partner nearby with a hand on her back, cozy domestic warmth, soft morning light.",
    "05-latens": "A pregnant woman resting peacefully on a sofa at home under a blanket in warm lamp light, her partner bringing a glass of water, restful and unhurried.",
    "06-aktiv": "A laboring woman standing and swaying, leaning forward onto her partner who supports her and presses gently on her lower back, focused and connected, a warm soft birth room.",
    "07-overgang": "An intimate close moment: the partner holding the laboring woman's face with both hands, foreheads nearly touching, eye contact, reassurance and quiet strength.",
    "08-krystning": "A tender emotional moment near birth shown through feeling rather than anatomy — the partner holding the mother's hand and shoulder, both focused, a sense of an arrival about to happen, warm soft light, gentle and non-graphic.",
    "09-hudmothud": "A newborn baby wrapped and resting skin-to-skin on the mother's chest, the mother gazing down with love, the partner leaning in close, profound tenderness, soft warm glow.",
    "10-profylax": "A pregnant woman and her partner practicing calm breathing together, seated on a floor cushion, eyes closed, peaceful and serene, one hand gently guiding.",
    "11-smartlindring": "A pregnant woman in labor using comfort measures — sitting and leaning forward on a birth ball while her partner massages her back, soothing and supportive.",
    "14-trygghet": "A reassuring midwife in a warm birth room gently talking with the expecting couple, a calm and safe atmosphere, supportive.",
    "16-forsta-timmarna": "New parents resting together holding their newborn, tired and overjoyed, warm soft light, an intimate family moment.",
}

sem = asyncio.Semaphore(3)


async def one(name: str, scene: str):
    prompt = f"{STYLE}\n\nScene: {scene}"
    async with sem:
        for attempt in range(3):
            try:
                img = await gemini.generate_image(
                    model=MODEL,
                    prompt=prompt,
                    aspect_ratio="3:4",
                    image_size="2K",
                )
                path = OUT / f"{name}.png"
                img.save(path)
                print(f"OK  {name} -> {path}")
                return
            except Exception as e:
                print(f"retry {name} ({attempt+1}/3): {e}")
                await asyncio.sleep(3)
        print(f"FAIL {name}")


async def main():
    await asyncio.gather(*(one(n, s) for n, s in SCENES.items()))
    print(f"\nCost estimate: ${gemini.get_cost_estimate():.2f}")


if __name__ == "__main__":
    asyncio.run(main())
