import subprocess
import time
import logging

# Set up logging
logging.basicConfig(filename='logs/reddit_scraper_runner.log', level=logging.INFO)

# Constants for file paths and intervals
INPUT_FILE_NAME = "files/subreddits.txt"
OUTPUT_FILE_NAME = "files/mined_subreddits.txt"
REDDIT_PROGRAM_PATH = "src/trojan.py"
EXECUTION_INTERVAL = 6

# Read all lines from a file
def read_file_lines(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()


def main():
    i = 1
    num_lines_output = 0
    num_lines_input = len(read_file_lines(INPUT_FILE_NAME))

    # Run the scraper until all subreddits are mined
    while True:
        try:
            num_lines_output = len(read_file_lines(OUTPUT_FILE_NAME))

            subprocess.run(["python3", REDDIT_PROGRAM_PATH])

            if(num_lines_output == num_lines_input):
                logging.info(f"Run {i} finished.")
                break

            time.sleep(EXECUTION_INTERVAL)

        except KeyboardInterrupt:
            logging.error(f"Run {i} interrupted by the user.")
            break

        except Exception as e:
            logging.error(f"An error occurred on run {i}: {e}")

if __name__ == "__main__":
    main()

    logging.info("Program finished.")
    print("Program finished.")

    exit()