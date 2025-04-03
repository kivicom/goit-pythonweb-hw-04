import argparse
import asyncio
import logging
import shutil
from pathlib import Path
import aiofiles

# Configure logging to track errors and info
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("sort_files.log"),  # Log to a file
        logging.StreamHandler(),  # Also log to console
    ],
)
logger = logging.getLogger(__name__)


async def read_folder(source: Path, output: Path) -> None:
    """
    Asynchronously read all files in the source folder and its subfolders.

    Args:
        source (Path): Path to the source folder.
        output (Path): Path to the output folder.
    """
    try:
        # Iterate over all items in the source folder
        for item in source.iterdir():
            if item.is_file():
                # If the item is a file, copy it to the appropriate folder
                await copy_file(item, output)
            elif item.is_dir():
                # If the item is a directory, recursively read it
                await read_folder(item, output)
    except Exception as e:
        logger.error(f"Error reading folder {source}: {e}")


async def copy_file(file_path: Path, output: Path) -> None:
    """
    Asynchronously copy a file to the output folder based on its extension.

    Args:
        file_path (Path): Path to the file to be copied.
        output (Path): Path to the output folder.
    """
    try:
        # Get the file extension (e.g., 'jpg', 'pdf'); use 'no_extension' if none
        extension = file_path.suffix[1:].lower() or "no_extension"
        # Create a subfolder in the output directory based on the extension
        target_folder = output / extension
        target_folder.mkdir(parents=True, exist_ok=True)

        # Define the target path for the file
        target_path = target_folder / file_path.name

        # Copy the file using shutil (aiofiles is not needed for copying)
        shutil.copy2(file_path, target_path)
        logger.info(f"Copied {file_path} to {target_path}")

    except Exception as e:
        logger.error(f"Error copying file {file_path}: {e}")


def parse_arguments() -> tuple[Path, Path]:
    """
    Parse command-line arguments for source and output folders.

    Returns:
        tuple[Path, Path]: Paths to the source and output folders.
    """
    parser = argparse.ArgumentParser(
        description="Asynchronously sort files by extension into subfolders."
    )
    parser.add_argument(
        "source", type=str, help="Path to the source folder containing files to sort."
    )
    parser.add_argument(
        "output",
        type=str,
        help="Path to the output folder where sorted files will be placed.",
    )
    args = parser.parse_args()

    # Convert string paths to Path objects
    source_path = Path(args.source)
    output_path = Path(args.output)

    # Validate that the source folder exists
    if not source_path.exists() or not source_path.is_dir():
        raise ValueError(
            f"Source folder {source_path} does not exist or is not a directory."
        )

    # Create the output folder if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    return source_path, output_path


async def main() -> None:
    """
    Main function to start the asynchronous file sorting process.
    """
    # Parse command-line arguments
    source, output = parse_arguments()

    # Start the recursive reading and copying process
    await read_folder(source, output)


if __name__ == "__main__":
    # Run the main asynchronous function
    asyncio.run(main())
