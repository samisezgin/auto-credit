# Student Grade Entry Automation

Automates radio button selection on a web-based grade entry page using
Tab+Arrow keyboard navigation. No coordinate mapping, no DPI/scroll issues.
Pure keyboard input.

## Quick Start

1. Open the grade entry page in your browser
2. Double-click **`start.bat`**
3. Answer the prompts (question count, grade)
4. When countdown starts, switch to browser and click the first radio button

One student is processed per run. Run again for the next student.
Previous settings are remembered — just press Enter to reuse them.

## How It Works

1. **2x Tab** to move to the next row (skips the row number column)
2. **Arrow keys** to select grade (1-4):
   - Grade 1: Right + Left (move to 2, back to 1)
   - Grade 2: Right (1 press)
   - Grade 3: Right (2 presses)
   - Grade 4: Right (3 presses)
3. First question is skipped (user clicks it manually for focus)
4. After all rows, **Enter** to save

## Human-like Behavior

- **Variable timing:** All delays use `random.uniform` for natural variation
- **Fatigue simulation:** Slows down over time (first 20 rows fast, then slower)

## Safety

- **Fail-Safe:** Move mouse to top-left corner to stop the script
- **Log:** All actions are logged to `log.txt`
- **Settings:** Previous run settings saved in `settings.json`

## Tips

- Plan 1-2 hour sessions per day
- Don't touch the keyboard while the script is running
- Keep an eye on the screen — the script can't detect page errors

## Bot Detection Test

```bash
pip install selenium
python test/test_runner.py
```

Opens Chrome, fills 80 radio buttons with Tab+Arrow, checks bot detection score.
Score should be 0 with verdict INSAN (human).

## File Structure

```
start.bat             -> One-click launcher (installs Python if needed)
automation.py         -> Main automation script
requirements.txt      -> Python dependencies
settings.json         -> Auto-generated: saved settings
log.txt               -> Auto-generated: action log
test/
  index.html          -> Test page with bot detection
  test_runner.py      -> Automated test runner
  start.bat           -> Test launcher
```
