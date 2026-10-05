# Inner-life skill（inner-life-guide）

Let AI assistants answer inner-life questions — moods, dreams, anxiety, grief, the inner critic — by looking up *A Field Guide to Your Inner Life* first: the relevant entries, cited by number, with the guide's three honesty layers kept apart. In a crisis, it hands over the hotlines before anything else.

Everything lives in [SKILL.md](SKILL.md); both tools read the same file.

## Install into Claude Code

Open Claude Code inside this repository and it just works — `.claude/skills/inner-life-guide/` already points at the rules.

To use it from any directory:

```bash
mkdir -p ~/.claude/skills/inner-life-guide && curl -fsSL -o ~/.claude/skills/inner-life-guide/SKILL.md "https://raw.githubusercontent.com/sparkshen029-ux/a-field-guide-to-your-inner-life/main/skills/inner-life-guide/SKILL.md"
```

Then ask *"why do I keep having the same nightmare"*, *"what does my anxiety want"*, or *"I feel envious of my friend and I hate it"* — or say explicitly "use inner-life-guide".

## Install into Codex

Same file, personal directory `~/.agents/skills/inner-life-guide/`. Copy it the same way.

## What it will not do

- It will not interpret a dream from a symbol table (entry 10 explains why).
- It will not read anyone else's mind from your dreams (entry 13).
- It will not diagnose, and in a crisis it will only signpost (entry 24).
- It will not pass tradition off as research — the Honesty notes travel with every answer.
