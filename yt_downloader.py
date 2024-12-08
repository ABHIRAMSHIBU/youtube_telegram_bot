import tempfile
import os
from time import sleep
import shutil

from command_executor import Executor


class YT_Downloader:
    def __init__(self):
        pass

    def setUrl(self, url):
        self.url = url

    def setResolution(self, resolution):
        pass

    def setFormat(self, format):
        pass

    def download(self):
        pass

    def download_audio(self):
        pass


class YT_DLP_Downloader(YT_Downloader):
    def __init__(self):
        self.video = "bestvideo"
        self.audio = "bestaudio"

    def download(self):
        pwd = os.getcwd()
        output_file = None

        with tempfile.TemporaryDirectory() as self.temp_dir:
            os.chdir(self.temp_dir)

            executor = Executor()
            executor.execute(f'yt-dlp -f {self.video}+{self.audio} {self.url}')
            executor.join()
            # Print stdout and stderr
            print(executor.get_output().decode())
            print(executor.get_error().decode())
            if executor.get_status() == 0:
                print("Download completed")
            # Move the downloaded files to the current directory
            for file in os.listdir(self.temp_dir):
                extension = os.path.splitext(file)[1]
                if file.endswith((".mp4", ".webm", ".mkv")):
                    output_file = os.path.join(pwd, f"output{extension}")
                    shutil.move(os.path.join(self.temp_dir, file), output_file)
                    print(f"Moved {file} to {pwd}")
                    break

        os.chdir(pwd)
        return output_file

    def download_audio(self):
        pwd = os.getcwd()
        output_file = None

        with tempfile.TemporaryDirectory() as self.temp_dir:
            os.chdir(self.temp_dir)

            executor = Executor()
            executor.execute(f'yt-dlp --no-playlist -f {self.audio} {self.url}')
            executor.join()
            # Print stdout and stderr
            print(executor.get_output().decode())
            print(executor.get_error().decode())
            if executor.get_status() == 0:
                print("Download completed")
            # Move the downloaded files to the current directory
            for file in os.listdir(self.temp_dir):
                file_name_with_extension = os.path.basename(file)
                if file.endswith((".mp3", ".wav", ".ogg", ".webm")):
                    output_file = os.path.join(pwd, file_name_with_extension)
                    shutil.move(os.path.join(self.temp_dir, file), output_file)
                    print(f"Moved {file} to {pwd}")
                    break

        os.chdir(pwd)
        return output_file