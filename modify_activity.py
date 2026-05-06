#!/usr/bin/env python3
"""
Strava Activity Modifier - Modify GPX/TCX activity files to simulate different performance levels.

This script adjusts timestamps in activity files, effectively changing the speed at which 
the activity was completed. It supports both GPX and TCX formats.

Usage:
    python modify_activity.py activity.gpx --speed 1.1
    python modify_activity.py activity.tcx --speed 0.8 --output modified_activity.tcx
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET


def parse_iso_datetime(dt_str):
    """Parse ISO 8601 datetime string."""
    # Handle both formats: with and without microseconds
    try:
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except ValueError:
        return datetime.fromisoformat(dt_str.split('.')[0].replace('Z', '+00:00'))


def format_iso_datetime(dt):
    """Format datetime to ISO 8601 string."""
    return dt.isoformat() + 'Z'


def modify_gpx(input_file, speed_multiplier, output_file):
    """Modify GPX activity file by adjusting timestamps."""
    
    # Parse the GPX file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Define namespaces
    ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    
    # Find all trackpoints
    trackpoints = root.findall('.//gpx:trkpt', ns)
    
    if not trackpoints:
        print("❌ No trackpoints found in GPX file!")
        return False
    
    # Get first and last timestamps
    first_time_elem = trackpoints[0].find('gpx:time', ns)
    last_time_elem = trackpoints[-1].find('gpx:time', ns)
    
    if first_time_elem is None or last_time_elem is None:
        print("❌ Trackpoints don't have time information!")
        return False
    
    start_time = parse_iso_datetime(first_time_elem.text)
    end_time = parse_iso_datetime(last_time_elem.text)
    original_duration = end_time - start_time
    
    # Calculate new duration
    new_duration = original_duration / speed_multiplier
    duration_change_seconds = (original_duration - new_duration).total_seconds()
    
    # Adjust timestamps
    for i, trackpoint in enumerate(trackpoints):
        time_elem = trackpoint.find('gpx:time', ns)
        if time_elem is not None:
            current_time = parse_iso_datetime(time_elem.text)
            # Calculate proportion through the activity (0 to 1)
            proportion = (current_time - start_time) / original_duration
            # Apply the time adjustment
            new_time = current_time - (duration_change_seconds * proportion) * timedelta(seconds=1)
            time_elem.text = format_iso_datetime(new_time)
    
    # Save modified file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    # Calculate and display statistics
    original_hours = original_duration.total_seconds() / 3600
    new_hours = new_duration.total_seconds() / 3600
    actual_speed_multiplier = original_duration / new_duration
    
    print(f"\n✅ GPX file modified successfully!")
    print(f"📁 Original file: {input_file}")
    print(f"📁 Modified file: {output_file}")
    print(f"\n⏱️  Duration changes:")
    print(f"   Original: {format_duration(original_duration)}")
    print(f"   Modified: {format_duration(new_duration)}")
    print(f"   Time saved: {format_duration(original_duration - new_duration)}")
    print(f"\n🏃 Speed multiplier: {actual_speed_multiplier:.2f}x")
    print(f"📊 Effective speed change: +{(actual_speed_multiplier - 1) * 100:.1f}%")
    
    return True


def modify_tcx(input_file, speed_multiplier, output_file):
    """Modify TCX activity file by adjusting timestamps and proportional metrics."""
    
    # Parse the TCX file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Define namespaces
    ns = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
    
    # Find all trackpoints
    trackpoints = root.findall('.//tcx:Trackpoint', ns)
    
    if not trackpoints:
        print("❌ No trackpoints found in TCX file!")
        return False
    
    # Get first and last timestamps
    first_time_elem = trackpoints[0].find('tcx:Time', ns)
    last_time_elem = trackpoints[-1].find('tcx:Time', ns)
    
    if first_time_elem is None or last_time_elem is None:
        print("❌ Trackpoints don't have time information!")
        return False
    
    start_time = parse_iso_datetime(first_time_elem.text)
    end_time = parse_iso_datetime(last_time_elem.text)
    original_duration = end_time - start_time
    
    # Calculate new duration
    new_duration = original_duration / speed_multiplier
    duration_change_seconds = (original_duration - new_duration).total_seconds()
    
    # Adjust timestamps and cadence
    for i, trackpoint in enumerate(trackpoints):
        time_elem = trackpoint.find('tcx:Time', ns)
        if time_elem is not None:
            current_time = parse_iso_datetime(time_elem.text)
            # Calculate proportion through the activity (0 to 1)
            proportion = (current_time - start_time) / original_duration
            # Apply the time adjustment
            new_time = current_time - (duration_change_seconds * proportion) * timedelta(seconds=1)
            time_elem.text = format_iso_datetime(new_time)
            
            # Adjust cadence proportionally if it exists
            cadence_elem = trackpoint.find('tcx:Cadence', ns)
            if cadence_elem is not None:
                try:
                    original_cadence = float(cadence_elem.text)
                    new_cadence = original_cadence * speed_multiplier
                    # Cap cadence at realistic values (typically 180-220 for running)
                    new_cadence = min(new_cadence, 220)
                    cadence_elem.text = str(int(new_cadence))
                except (ValueError, TypeError):
                    pass
    
    # Save modified file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    # Calculate and display statistics
    actual_speed_multiplier = original_duration / new_duration
    
    print(f"\n✅ TCX file modified successfully!")
    print(f"📁 Original file: {input_file}")
    print(f"📁 Modified file: {output_file}")
    print(f"\n⏱️  Duration changes:")
    print(f"   Original: {format_duration(original_duration)}")
    print(f"   Modified: {format_duration(new_duration)}")
    print(f"   Time saved: {format_duration(original_duration - new_duration)}")
    print(f"\n🏃 Speed multiplier: {actual_speed_multiplier:.2f}x")
    print(f"📊 Effective speed change: +{(actual_speed_multiplier - 1) * 100:.1f}%")
    print(f"⚠️  Cadence values have been adjusted proportionally")
    
    return True


def format_duration(td):
    """Format timedelta to HH:MM:SS string."""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def main():
    parser = argparse.ArgumentParser(
        description='Modify GPX/TCX activity files to simulate different performance levels',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Increase speed by 10%%:
    python modify_activity.py activity.gpx --speed 1.1
  
  Decrease speed by 20%%:
    python modify_activity.py activity.tcx --speed 0.8
  
  Save to custom output file:
    python modify_activity.py activity.gpx --speed 1.15 --output my_activity.gpx
        """
    )
    
    parser.add_argument('input_file', help='Path to the activity file (GPX or TCX)')
    parser.add_argument(
        '--speed',
        type=float,
        required=True,
        help='Speed multiplier (1.0 = original, 1.1 = 10%% faster, 0.9 = 10%% slower)'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: input_filename_modified.ext)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: File '{args.input_file}' not found!")
        sys.exit(1)
    
    # Determine file format
    file_ext = input_path.suffix.lower()
    if file_ext not in ['.gpx', '.tcx']:
        print(f"❌ Error: File must be GPX or TCX format, got {file_ext}")
        sys.exit(1)
    
    # Validate speed multiplier
    if args.speed <= 0:
        print("❌ Error: Speed multiplier must be greater than 0")
        sys.exit(1)
    
    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_modified{file_ext}"
    
    # Process file
    try:
        print(f"🔄 Processing {file_ext.upper()} file...")
        print(f"📍 Speed multiplier: {args.speed}x")
        
        if file_ext == '.gpx':
            success = modify_gpx(input_path, args.speed, output_path)
        else:  # .tcx
            success = modify_tcx(input_path, args.speed, output_path)
        
        if success:
            print(f"\n🎉 Done! You can now import '{output_path}' into Garmin Connect or your device.")
            sys.exit(0)
        else:
            sys.exit(1)
            
    except ET.ParseError as e:
        print(f"❌ Error parsing XML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
