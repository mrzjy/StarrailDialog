import argparse
import glob
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        default="data",
        type=str,
        required=True,
        help="dir for extracted data",
    )
    args = parser.parse_args()

    for file in glob.iglob(os.path.join(args.repo, "dialogues"))