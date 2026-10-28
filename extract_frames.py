import cv2
import argparse
from pathlib import Path
import hashlib
import re


def image_hash(image):
    """Small perceptual-ish hash used to reject nearly identical frames."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (32, 32))
    return hashlib.md5(small.tobytes()).hexdigest()


def extract_frames(video_path, output_dir, sample_fps=1.0, blur_threshold=None,
                   duplicate_window=None):
    if sample_fps <= 0:
        raise ValueError("sample_fps must be greater than 0.")

    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    try:
        native_fps = cap.get(cv2.CAP_PROP_FPS)
        if not native_fps or native_fps <= 0:
            native_fps = 30.0

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / native_fps if frame_count else 0

        sample_fps = min(sample_fps, native_fps)
        frame_interval = max(1, round(native_fps / sample_fps))

        saved = 0
        examined = 0
        last_hashes = []

        print(f"Video: {video_path}")
        print(f"FPS: {native_fps:.2f}, frames: {frame_count}, duration: {duration:.1f}s")
        print(f"Sampling approximately {sample_fps:.2f} FPS")

        frame_idx = 0

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            if frame_idx % frame_interval != 0:
                frame_idx += 1
                continue

            examined += 1

            if duplicate_window is not None:
                h = image_hash(frame)
                if h in last_hashes:
                    frame_idx += 1
                    continue
                last_hashes.append(h)
                if len(last_hashes) > duplicate_window:
                    last_hashes.pop(0)

            timestamp = frame_idx / native_fps
            filename = f"{video_path.stem}_t{timestamp:08.2f}s_f{frame_idx:07d}.jpg"
            ok_write = cv2.imwrite(str(output_dir / filename), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            if not ok_write:
                raise RuntimeError(f"Failed to write frame {filename} to {output_dir}")
            saved += 1

            frame_idx += 1

        print(f"Examined sampled frames: {examined}")
        print(f"Saved candidate frames: {saved}")
    finally:
        cap.release()


def process_folder(input_dir, output_dir, sample_fps=1.0, blur_threshold=None, duplicate_window=None):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder does not exist: {input_dir}")

    videos = []
    for ext in ("*.mp4", "*.mov", "*.avi", "*.mkv", "*.MP4", "*.MOV", "*.AVI", "*.MKV"):
        videos.extend(input_dir.glob(ext))

    videos = sorted(set(videos))

    if not videos:
        print(f"No supported videos found in {input_dir}")
        return

    print(f"Found {len(videos)} video(s) in {input_dir}")

    for video in videos:
        video_output = output_dir / video.stem
        print(f"\nProcessing: {video}")
        extract_frames(
            video,
            video_output,
            sample_fps=sample_fps,
            blur_threshold=blur_threshold,
            duplicate_window=duplicate_window
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract useful training-frame candidates from FreshAI food videos."
    )
    parser.add_argument("--input", required=True, help="Folder containing videos")
    parser.add_argument("--output", default="dataset/raw_frames",
                        help="Output folder for extracted frames")
    parser.add_argument("--fps", type=float, default=1.0,
                        help="Approximate frames per second to sample; lower values keep more candidate frames")
    parser.add_argument("--blur", type=float, default=None,
                        help="Optional blur threshold. Leave unset to disable blur filtering entirely.")
    parser.add_argument("--duplicate-window", type=int, default=None,
                        help="Optional duplicate window size. Leave unset to disable duplicate filtering entirely.")
    parser.add_argument("--chosen_image", "--chosen-image", dest="chosen_image",
                        help="Optional extracted frame filename; prints its source name after extraction.")

    args = parser.parse_args()

    if args.fps <= 0:
        raise ValueError("--fps must be greater than 0.")
    if args.blur is not None and args.blur < 0:
        raise ValueError("--blur must be non-negative.")
    if args.duplicate_window is not None and args.duplicate_window < 1:
        raise ValueError("--duplicate-window must be at least 1.")
    chosen_source = None
    if args.chosen_image:
        chosen_stem = Path(args.chosen_image).stem
        match = re.fullmatch(r"(.+)_t\d+(?:\.\d+)?s_f\d+", chosen_stem)
        if not match:
            raise ValueError(
                "--chosen_image must use an extracted frame filename, "
                "for example cannedfood_t00005.60s_f0000168.jpg."
            )
        chosen_source = match.group(1)

    process_folder(
        args.input,
        args.output,
        sample_fps=args.fps,
        blur_threshold=args.blur,
        duplicate_window=args.duplicate_window
    )

    if chosen_source:
        print(f"the chosen image is {chosen_source}")
        
