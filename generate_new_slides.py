import asyncio, sys
from pathlib import Path
SKILL = Path("/Users/christoffersundberg/Projects/glaseyewear/content/.claude/skills/aicontentgenerator")
sys.path.insert(0, str(SKILL))
from services import gemini

MODEL="gemini-3-pro-image-preview"
OUT=Path("images"); OUT.mkdir(exist_ok=True)
STYLE=("Soft, tender hand-painted gouache-style illustration. Warm, calm, reassuring mood. "
 "Limited cohesive palette: warm cream background, terracotta, soft blush pink, sage green, muted gold ochre. "
 "Gentle rounded organic shapes, soft edges, subtle paper-grain texture, painterly, generous negative space. "
 "ABSOLUTELY NO text, no letters, no words, no numbers anywhere in the image.")
SCENES={
 "A-rummet":"A calm, inviting hospital birth room with NO people: an adjustable bed with soft linens, a birth ball on the floor, a softly dimmed warm lamp, a window with gentle light, a comfortable chair beside the bed for a partner, and a discreet monitor on a stand. Tidy, peaceful, warm and reassuring.",
 "D-jockes-plats":"A partner standing close at the side of the bed by a laboring woman's head, at her eye level, gently holding her hand with foreheads close, positioned beside her and out of the way. Tender, supportive, a warm calm birth room.",
}
sem=asyncio.Semaphore(2)
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
