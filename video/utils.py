from moviepy.editor import VideoFileClip

def get_video_duration(video_path):
    try:
        with VideoFileClip(video_path) as video:
            duration_seconds = int(video.duration)
            
            hours, remainder = divmod(duration_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return None
