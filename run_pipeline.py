# run_pipeline.py
# ─────────────────────────────────────────────
# MASTER PIPELINE RUNNER
# Run this single file to execute all steps
# end-to-end automatically
#
# Usage:
#   python run_pipeline.py
#   python run_pipeline.py --skip-train   (if model already trained)
# ─────────────────────────────────────────────

import subprocess
import sys
import time
import argparse
import os

STEPS = [
    ("Step 1 — Load Dataset",       "src/load_data.py"),
    ("Step 2 — Preprocess Text",     "src/preprocess.py"),
    ("Step 3 — Train BERT Model",    "src/train.py"),
    ("Step 4 — Run Inference",       "src/predict.py"),
    ("Step 5 — Topic Modeling",      "src/topic_modeling.py"),
    ("Step 6 — Export for Power BI", "src/export.py"),
]

def run_step(name: str, script: str) -> bool:
    print(f"\n{'='*60}")
    print(f"  🚀 {name}")
    print(f"{'='*60}")
    start = time.time()
    result = subprocess.run([sys.executable, script], capture_output=False)
    elapsed = round(time.time() - start, 1)
    if result.returncode == 0:
        print(f"  ✅ Completed in {elapsed}s")
        return True
    else:
        print(f"  ❌ FAILED after {elapsed}s (exit code {result.returncode})")
        return False

def main():
    parser = argparse.ArgumentParser(description="Customer Sentiment Analysis Pipeline")
    parser.add_argument("--skip-train", action="store_true", help="Skip BERT training step")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("  Customer Sentiment Analysis — Full Pipeline")
    print("  150K+ Reviews | BERT | BERTopic | Power BI")
    print("="*60)

    overall_start = time.time()
    failed_steps  = []

    for name, script in STEPS:
        # Skip training if flag is set and model exists
        if args.skip_train and "train" in script:
            if os.path.exists("models/bert_finetuned/config.json"):
                print(f"\n⏭️  Skipping {name} (model already exists)")
                continue

        success = run_step(name, script)
        if not success:
            failed_steps.append(name)
            print(f"\n[ERROR] Pipeline stopped at: {name}")
            print("Fix the error above and re-run.")
            sys.exit(1)

    total_time = round((time.time() - overall_start) / 60, 1)
    print(f"\n{'='*60}")
    print(f"  🎉 Pipeline Complete! Total time: {total_time} mins")
    print(f"{'='*60}")
    print("\n  📂 Output Files:")
    print("     powerbi/powerbi_ready.csv   → Import into Power BI")
    print("     powerbi/topic_summary_powerbi.csv")
    print("     powerbi/kpi_metrics.csv")
    print("     outputs/confusion_matrix.png")
    print("     outputs/topics_all.png")
    print("\n  ✅ All done! Open Power BI Desktop and import the files above.")

if __name__ == "__main__":
    main()
