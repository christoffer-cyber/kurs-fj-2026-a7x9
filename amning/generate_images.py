import asyncio, sys
from pathlib import Path
SKILL = Path("/Users/christoffersundberg/Projects/glaseyewear/content/.claude/skills/aicontentgenerator")
sys.path.insert(0, str(SKILL))
from services import gemini
MODEL="gemini-3-pro-image-preview"
OUT=Path(__file__).parent/"images"; OUT.mkdir(exist_ok=True)
STYLE=("Soft, tender hand-painted gouache-style illustration. Warm, calm, reassuring mood. "
 "Limited cohesive palette: warm cream background, terracotta, soft blush pink, sage green, muted gold ochre. "
 "Gentle rounded organic shapes, soft edges, subtle paper-grain texture, painterly, generous negative space. "
 "Tasteful, modest and non-clinical. ABSOLUTELY NO text, no letters, no words, no numbers anywhere.")
SCENES={
 "cover":"A mother tenderly breastfeeding her newborn baby, gazing down with love, seated comfortably, warm soft light, serene and intimate.",
 "forsta":"A newborn baby resting skin-to-skin on the mother's chest in the first days, tiny and peaceful, the mother's hand gently cradling, warm glow.",
 "stallning":"A mother comfortably nursing her baby in a relaxed cradle hold, supported by soft pillows in a cozy armchair, calm and at ease.",
 "tag":"A tender close view of a mother and her nursing baby, cheeks soft and close, the baby calm and content, gentle warmth, non-clinical.",
 "partner":"A partner gently bringing a glass of water to a mother who is breastfeeding on a sofa, caring and supportive, cozy home.",
 "avslut":"A mother, her partner and their newborn resting together peacefully, the baby content after feeding, warm tender family calm.",
}
sem=asyncio.Semaphore(3)
async def one(name,scene):
    async with sem:
        for a in range(3):
            try:
                img=await gemini.generate_image(model=MODEL,prompt=f"{STYLE}\n\nScene: {scene}",aspect_ratio="3:4",image_size="2K")
                img.save(OUT/f"{name}.png"); print("OK",name); return
            except Exception as e:
                print("retry",name,e); await asyncio.sleep(3)
        print("FAIL",name)
async def main():
    await asyncio.gather(*(one(n,s) for n,s in SCENES.items()))
    print(f"cost ${gemini.get_cost_estimate():.2f}")
asyncio.run(main())
