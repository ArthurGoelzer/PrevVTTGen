import os
import cv2

# Configurations:
videoFile = './media/input/468.mp4'
video_width = 0
video_height = 0
video_duration = 0


def load_video_info():
    global video_height
    global video_width
    global video_duration

    cv2video = cv2.VideoCapture(videoFile)
    video_height = cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    video_width = cv2video.get(cv2.CAP_PROP_FRAME_WIDTH)

    frame_count = cv2video.get(cv2.CAP_PROP_FRAME_COUNT)
    frames_per_sec = cv2video.get(cv2.CAP_PROP_FPS)
    video_duration = (frame_count / frames_per_sec)

    print("Video info: fps {}, duration {}, size {}x{}".format(int(frames_per_sec), int(video_duration), video_width, video_height))


def main():
    if os.path.isfile(videoFile):
        print('Video file found: ' + videoFile)
        load_video_info()

    else:
        print('Video file not found: ' + videoFile)
        exit()


if __name__ == '__main__':
    main()
