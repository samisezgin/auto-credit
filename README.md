# Student Grade Entry Automation

Automates radio button selection on a web-based grade entry page using
Tab+Arrow keyboard navigation. Unit-based structure with expandable tabs.
No coordinate mapping, no DPI/scroll issues. Pure keyboard input.

## Quick Start

1. Open the grade entry page in your browser
2. Double-click **`start.bat`**
3. Answer the prompts (unit count, questions per unit, grade)
4. When countdown starts, switch to browser and click the first radio button
5. After each student: enter new grade, press Enter to keep the same, or `q` to quit

Previous settings are remembered — just press Enter to reuse them.

## How It Works

### Within a unit
1. **2x Tab** to move to the next question (skips the row number column)
2. **Arrow keys** to select grade (1-4):
   - Grade 1: Right + Left (move to 2, back to 1)
   - Grade 2: Right (1 press)
   - Grade 3: Right (2 presses)
   - Grade 4: Right (3 presses)

### Between units
1. **2x Tab + Enter** to open the next unit tab
2. **1x Tab + Arrow** for the first question of the new unit

### Notes
- First question of the first unit is skipped (user clicks it manually for focus)
- Same grade is applied to all questions of a student
- Grade can be changed between students without restarting

## Human-like Behavior

- **Variable timing:** All delays use `random.uniform` for natural variation
- **Fatigue simulation:** Slows down over time (first 20 rows fast, then slower)

## Safety

- **Fail-Safe:** Move mouse to top-left corner to stop the script
- **Log:** All actions are logged to `log.txt`
- **Settings:** Previous run settings saved in `settings.json`

## Tips

- Don't touch the keyboard while the script is running
- Keep an eye on the screen — the script can't detect page errors

## Bot Detection Test

```bash
pip install selenium
python test/test_runner.py
```

Opens Chrome, fills 3 units x 7 questions with Tab+Arrow, checks bot detection score.
Score should be 0 with verdict INSAN (human).

## File Structure

```
start.bat             -> One-click launcher (installs Python if needed)
automation.py         -> Main automation script
requirements.txt      -> Python dependencies
settings.json         -> Auto-generated: saved settings
log.txt               -> Auto-generated: action log
test/
  index.html          -> Test page with bot detection (expandable unit tabs)
  test_runner.py      -> Automated test runner
  start.bat           -> Test launcher
```
