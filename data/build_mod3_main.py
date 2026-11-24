# build_mod3_main.py: Orchestrates and writes mod3_answers.json
import json
import os
import sys

# Import SVGs from build_mod3
from build_mod3 import (
    svg_analog_input_block,
    svg_digital_input_block,
    svg_keyboard_matrix,
    svg_adc0808,
    svg_output_devices_block,
    svg_dac_triangular,
    svg_stepper_motor,
    svg_signal_conditioning
)

# Import topic builders
from build_mod3_part1 import get_topic_3_1
from build_mod3_part2 import get_topic_3_2, get_topic_3_3

OUTPUT_PATH = r"d:\LAST EXAM(MDM)\antigravity version\Embedded-Systems-Study-Guide\data\mod3_answers.json"

def main():
    print("Building Module 3 Study Guide JSON...")
    
    topic_3_1 = get_topic_3_1(
        svg_analog_input_block,
        svg_digital_input_block,
        svg_keyboard_matrix,
        svg_adc0808
    )
    
    topic_3_2 = get_topic_3_2(
        svg_output_devices_block,
        svg_dac_triangular,
        svg_stepper_motor
    )
    
    topic_3_3 = get_topic_3_3(
        svg_signal_conditioning
    )
    
    mod3_data = {
        "module": 3,
        "title": "Interfacing Analog and Digital Devices",
        "topics": [
            topic_3_1,
            topic_3_2,
            topic_3_3
        ]
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(mod3_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated {OUTPUT_PATH}")
    print(f"File size: {os.path.getsize(OUTPUT_PATH)} bytes")
    
    # Verify JSON validity by loading back
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        verified = json.load(f)
    print(f"Verified Module {verified['module']}: {verified['title']}")
    print(f"Number of topics: {len(verified['topics'])}")
    total_q = sum(len(t['questions']) for t in verified['topics'])
    print(f"Total questions: {total_q}")
    for t in verified['topics']:
        print(f"  Topic {t['id']}: {t['title']} ({len(t['questions'])} questions)")
        for q in t['questions']:
            print(f"    - {q['id']}: {q['question'][:50]}... [Tags: {q['tags']}]")

if __name__ == "__main__":
    main()
