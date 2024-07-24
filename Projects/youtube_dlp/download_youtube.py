import yt_dlp
import os
import subprocess
def list_video_formats(video_url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get('formats', [])
        format_list = []
        print("\nAvailable formats:")
        for idx, fmt in enumerate(formats):
            if fmt.get('vcodec') != 'none':  # Filter out audio-only formats
                format_list.append(fmt)
                print(f"{len(format_list)}: {fmt.get('format_note', 'unknown')} - {fmt.get('ext')} - {fmt.get('filesize', 'unknown size')} - {fmt.get('format_id')}")

    return format_list

def download_youtube_video(video_url, format_id, output_path):
    ydl_opts = {
        'format': format_id,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'concurrent-fragments': 4,  # Number of concurrent connections
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        print(f'Download completed successfully for {video_url}!')

if __name__ == "__main__":
    # Ensure ffmpeg is installed
    # ffmpeg_check = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, shell=True)
    # if ffmpeg_check.returncode != 0:
    #     print("Warning: ffmpeg not found. Please install ffmpeg to enable audio/video merging.")
    #     print("Visit https://ffmpeg.org/download.html for installation instructions.")
    #     exit(1)

    # Get user input for video URL
    # video_url = input("Enter the YouTube video URL: ")
    video_url = 'https://www.youtube.com/watch?v=BGTx91t8q50'
    video_url = 'https://www.youtube.com/watch?v=4XTsAAHW_Tc'

    # List available formats
    format_list = list_video_formats(video_url)

    # Get user input for desired format
    # for i, format in enumerate(format_list):
    #     print(f"{i}. {format}")
    selected_format_index = int(input("\nEnter the number corresponding to the desired format: "))
    selected_format_id = format_list[selected_format_index]['format_id']

    # Get user input for output path
    output_path = input("Enter the output directory (leave empty for current directory): ")
    
    # Use current directory if no output path is provided
    if not output_path:
        output_path = '.'
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Download the video in the selected format
    download_youtube_video(video_url, selected_format_id, output_path)
