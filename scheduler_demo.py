#!/usr/bin/env python3
"""
Scheduler Demo Script

This script demonstrates the enhanced scheduler functionality:
1. Generates images with specific schedulers
2. Compares multiple schedulers
3. Shows how to use the command-line interface
"""

import subprocess
import sys
import os

def demo_single_scheduler():
    """Demonstrate single scheduler generation."""
    print("=" * 60)
    print("DEMO 1: Single Scheduler Generation")
    print("=" * 60)
    
    prompt = "a beautiful sunset over the ocean, digital art"
    scheduler = "EulerDiscrete"
    
    print(f"Generating image with scheduler: {scheduler}")
    print(f"Prompt: {prompt}")
    
    cmd = [
        sys.executable, "imagegeneration_schedulers.py",
        prompt,
        "--single", scheduler
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print("\nOutput:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("⚠️  Generation timed out (>5 minutes)")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_scheduler_comparison():
    """Demonstrate scheduler comparison."""
    print("\n" + "=" * 60)
    print("DEMO 2: Scheduler Comparison")
    print("=" * 60)
    
    prompt = "a majestic mountain landscape, photorealistic"
    schedulers = "EulerDiscrete,DPMSolverMultistep,DDIM"
    
    print(f"Comparing schedulers: {schedulers}")
    print(f"Prompt: {prompt}")
    
    cmd = [
        sys.executable, "imagegeneration_schedulers.py",
        prompt,
        schedulers
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        print("\nOutput:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("⚠️  Generation timed out (>10 minutes)")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_list_schedulers():
    """Demonstrate listing available schedulers."""
    print("\n" + "=" * 60)
    print("DEMO 3: Available Schedulers")
    print("=" * 60)
    
    cmd = [sys.executable, "imagegeneration_schedulers.py", "--list"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print("Available schedulers:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main demo function."""
    print("🎨 Stable Diffusion Scheduler Demo")
    print("This demo shows the enhanced scheduler functionality")
    print("\nNote: This demo requires CUDA and may take several minutes to complete.")
    
    # Check if we should run the demos
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        print("\n🏃 Quick mode: Only listing schedulers")
        demo_list_schedulers()
        return
    
    response = input("\n❓ Do you want to run the full demo? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("👋 Running quick demo (schedulers list only)")
        demo_list_schedulers()
        return
    
    print("\n🚀 Starting full demo...")
    
    # Run all demos
    demo_list_schedulers()
    demo_single_scheduler()
    demo_scheduler_comparison()
    
    print("\n" + "=" * 60)
    print("✨ Demo completed!")
    print("=" * 60)
    print("\nGenerated images can be found in the 'scheduler_outputs' directory.")
    print("You can also use the FastAPI endpoints for more advanced functionality.")
    print("\nUsage examples:")
    print("  python imagegeneration_schedulers.py \"your prompt\" --single EulerDiscrete")
    print("  python imagegeneration_schedulers.py \"your prompt\" \"Euler,DDIM,DPM\"")
    print("  python imagegeneration_schedulers.py --list")

if __name__ == "__main__":
    main()
