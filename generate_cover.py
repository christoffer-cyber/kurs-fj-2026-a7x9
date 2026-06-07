"""Generera personligt omslag (likhet från foto) i samma gouache-stil.

Kör med skillens venv + GOOGLE_API_KEY.
"""
import asyncio
import sys
from pathlib import Path
from PIL import Image

SKILL = Path("/Users/christoffersundberg/Projects/glaseyewear/content/.claude/skills/aicontentgenerator")
sys.path.insert(0, str(SKILL))
from services import gemini  # noqa: E402

MODEL = "gemini-3-pro-image-preview"
REF = Path("/Users/christoffersundberg/Downloads/4P0A4197.JPG")
OUT = Path("/Users/christoffersundberg/Projects/marie-forlossningskurs/images/_cover_candidates")
OUT.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "Soft, tender hand-painted gouache-style illustration, like a warm editorial / picture-book "
    "painting. Limited cohesive palette: warm cream background, terracotta, soft blush pink, sage "
    "green, muted gold ochre. Gentle rounded organic shapes, soft edges, subtle paper-grain texture, "
    "painterly brushwork, generous negative space. Calm, intimate, reassuring mood.\n\n"
    "Depict THIS specific expecting couple from the reference photo, keeping their likeness but "
    "rendered as a stylized painting (NOT photorealistic): a man with short light blond hair and "
    "light stubble, and a pregnant woman with long wavy blonde hair and a warm smile. He stands "
    "close beside and slightly behind her with his hands resting gently on her pregnant belly; she "
    "leans her head tenderly against him. Soft blush-pink cherry-blossom branches behind them. Both "
    "look happy, calm and in love. Portrait composition, the couple centered with airy space around.\n\n"
    "ABSOLUTELY NO text, no letters, no words, no numbers anywhere in the image."
)


async def one(idx: int, ref: Image.Image):
    for attempt in range(3):
        try:
            img = await gemini.generate_image(
                model=MODEL,
                prompt=PROMPT,
                reference_images=[ref],
                aspect_ratio="3:4",
                image_size="2K",
            )
            path = OUT / f"cover-{chr(97+idx)}.png"
            img.save(path)
            print(f"OK  cover-{chr(97+idx)} -> {path}")
            return
        except Exception as e:
            print(f"retry {idx} ({attempt+1}/3): {e}")
            await asyncio.sleep(3)
    print(f"FAIL cover-{idx}")


async def main():
    ref = Image.open(REF).convert("RGB")
    await asyncio.gather(*(one(i, ref) for i in range(3)))
    print(f"\nCost estimate: ${gemini.get_cost_estimate():.2f}")


if __name__ == "__main__":
    asyncio.run(main())
