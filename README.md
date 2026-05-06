# 🏃 Strava Cheater - Activity Modifier

Modify your Garmin activity files to simulate different performance levels. Change activity speed, adjust timestamps, and re-import into Garmin Connect or Strava.

**Disclaimer:** This tool is for testing, training simulation, and educational purposes only. Do not use to artificially boost your public activity records on Strava or Garmin Connect.

## 📋 Features

- ✅ **GPX File Support** - Adjust timestamps to simulate faster/slower activities
- ✅ **TCX File Support** - Full support including cadence adjustments
- ✅ **Speed Multiplier** - Precise control over activity speed changes
- ✅ **Detailed Output** - View before/after duration and speed changes
- ✅ **Error Handling** - Graceful handling of missing or invalid files
- ✅ **Easy Integration** - Re-import modified files into Garmin Connect or your device

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/snmslavk/strava-cheater.git
cd strava-cheater

# No dependencies required! The script uses only Python standard library.
# Tested with Python 3.7+
```

### Basic Usage

```bash
# Increase speed by 10% (activity completes 10% faster)
python modify_activity.py activity.gpx --speed 1.1

# Decrease speed by 20% (activity takes 20% longer)
python modify_activity.py activity.tcx --speed 0.8

# Save to custom output file
python modify_activity.py activity.gpx --speed 1.15 --output my_modified_activity.gpx
```

## 📖 How It Works

### GPX Files
1. Parses all trackpoints from the GPX file
2. Calculates the original activity duration
3. Computes new duration based on speed multiplier: `new_duration = original_duration / speed_multiplier`
4. Adjusts all trackpoint timestamps proportionally
5. Saves the modified file

### TCX Files
1. Parses all trackpoints from the TCX file
2. Adjusts timestamps (same as GPX)
3. **Bonus:** Proportionally adjusts cadence values to simulate faster/slower movement
4. Saves the modified file with all metrics updated

### Example Output

```
🔄 Processing GPX file...
📍 Speed multiplier: 1.1x

✅ GPX file modified successfully!
📁 Original file: my_run.gpx
📁 Modified file: my_run_modified.gpx

⏱️  Duration changes:
   Original: 00:30:45
   Modified: 00:27:54
   Time saved: 00:02:51

🏃 Speed multiplier: 1.10x
📊 Effective speed change: +10.0%

🎉 Done! You can now import 'my_run_modified.gpx' into Garmin Connect or your device.
```

## 🎯 Speed Multiplier Reference

| Multiplier | Effect | Use Case |
|-----------|--------|----------|
| 0.8 | 20% slower | Simulate easier pace |
| 0.9 | 10% slower | Simulate recovery run |
| 1.0 | No change | Keep original |
| 1.1 | 10% faster | Simulate faster pace |
| 1.2 | 20% faster | Simulate hard effort |
| 1.5 | 50% faster | Simulate sprint |

## 📥 Getting Your Activity Files

### From Garmin Device
1. Connect your Garmin device to your computer
2. Navigate to: `Garmin/Activities/`
3. Copy the `.fit` file to your computer
4. Convert `.fit` to `.gpx` or `.tcx` using:
   - [Garmin BaseCamp](https://www.garmin.com/en-US/software/basecamp/)
   - [FitCSVTool](https://forums.garmin.com/sports-fitness/f/garmin-sports-fitness-forum-archive/4302/fit-csv-tool-fit-file-sdk)
   - [Online FIT converter](https://www.fitfiletools.com/)

### From Garmin Connect
1. Go to [Garmin Connect](https://connect.garmin.com)
2. Find your activity
3. Click the download icon (⬇️)
4. Select "GPX" or "TCX" format
5. Save the file

### From Strava
1. Go to your activity on Strava
2. Click "Export this activity"
3. Choose "GPX" format
4. Save the file

## 💻 Advanced Usage

### Batch Processing

Process multiple files:

```bash
for file in *.gpx; do
  python modify_activity.py "$file" --speed 1.1
done
```

### Chain Multiple Modifications

```bash
# First increase speed by 10%
python modify_activity.py activity.gpx --speed 1.1 --output activity_v1.gpx

# Then increase by another 5%
python modify_activity.py activity_v1.gpx --speed 1.05 --output activity_v2.gpx
```

### TCX-Specific: Adjust Only Cadence

Since TCX files store cadence, modifications will adjust it proportionally:
- **Speed 1.2x**: Cadence increases by 20%
- **Speed 0.9x**: Cadence decreases by 10%

## 📤 Re-importing Modified Activities

### To Garmin Connect
1. Go to [Garmin Connect](https://connect.garmin.com)
2. Click "Import Activity" button
3. Select your modified `.gpx` or `.tcx` file
4. The activity will appear in your feed with updated metrics

### To Your Garmin Device
1. Convert `.gpx`/`.tcx` back to `.fit` using BaseCamp or converter tool
2. Connect device to computer
3. Copy file to `Garmin/Activities/`
4. Sync with Garmin Connect

### To Strava
1. Go to [Strava](https://strava.com)
2. Click the "+" button → "Upload Activity"
3. Select your modified `.gpx` file
4. Choose activity type and details
5. Upload

## ⚙️ Technical Details

### Supported Formats
- **GPX**: GPS Exchange Format (XML-based)
- **TCX**: Garmin Training Center XML format

### Timestamp Adjustment Algorithm
The script applies proportional time adjustments:
```
for each trackpoint:
    proportion = (trackpoint_time - start_time) / total_duration
    new_time = current_time - (time_adjustment * proportion)
```

This ensures smooth, realistic time distribution throughout the activity.

### What Gets Modified
✅ **Modified:**
- Trackpoint timestamps
- Activity duration
- Derived metrics (speed, average pace, etc. - calculated by Garmin/Strava)
- Cadence values (TCX only)

❌ **Not Modified:**
- GPS coordinates
- Elevation data
- Heart rate data
- Temperature
- Other sensors

## 🐛 Troubleshooting

### "No trackpoints found in GPX file!"
- Your GPX file may be corrupted or empty
- Try exporting the activity again from Garmin Connect or Strava

### "Trackpoints don't have time information!"
- The GPX/TCX file is missing timestamps
- This typically means it's an unsupported format variant
- Try converting with official Garmin tools

### Import fails in Garmin Connect
- The file structure might have been corrupted
- Verify the file can be opened with a text editor (should see XML)
- Try exporting from the device again and re-modifying

### Speed multiplier seems incorrect
- Remember: multiplier is inverted for time
  - **1.1x speed multiplier** = activity takes 1/1.1 = ~91% of original time
  - Duration decreases, but speed multiplier increases

## 📚 Examples

### Example 1: Make a training run look like a race
```bash
# Original: 10 km in 60 minutes (10:00/km pace)
python modify_activity.py training_run.gpx --speed 1.25

# Result: 10 km in 48 minutes (4:48/km pace)
```

### Example 2: Simulate a recovery run
```bash
# Original: 5 km in 30 minutes (6:00/km pace)
python modify_activity.py hard_run.gpx --speed 0.85

# Result: 5 km in 35 minutes (7:03/km pace)
```

### Example 3: Convert and compare performances
```bash
# Create multiple scenarios
python modify_activity.py my_run.gpx --speed 0.9 --output scenario_slower.gpx
python modify_activity.py my_run.gpx --speed 1.0 --output scenario_original.gpx
python modify_activity.py my_run.gpx --speed 1.1 --output scenario_faster.gpx

# Compare all three by importing to Garmin Connect
```

## ⚠️ Important Notes

1. **Ethical Use Only** - Use for testing, training simulation, and analysis
2. **Don't Cheat Public Records** - Artificially boosting public activities is against Strava/Garmin terms
3. **Backup Original** - Keep your original activity file as backup
4. **Device Sync** - Re-imported activities might get flagged as "manual" entries
5. **Privacy** - Only modify your own activities

## 🛠️ Development

### Requirements
- Python 3.7+
- No external dependencies

### Project Structure
```
strava-cheater/
├── modify_activity.py      # Main script
├── README.md               # This file
└── .gitignore              # Git ignore file
```

### Contributing
Feel free to fork, modify, and improve this project!

## 📄 License

MIT License - Feel free to use for personal and educational purposes.

## 🤝 Disclaimer

This tool is provided as-is for educational and personal use. Users are responsible for:
- Using it ethically and responsibly
- Not violating Strava/Garmin Terms of Service
- Obtaining necessary permissions for activity data
- Backing up original files before modification

The authors accept no responsibility for misuse or damages caused by this tool.

---

**Happy training! 🏃‍♂️🚴‍♀️🏊‍♂️**
