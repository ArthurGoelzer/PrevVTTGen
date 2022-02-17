import os
import cv2
import shutil

# Path to the directory containing the images
videoFile = './media/input/468.mp4'
outputDir = './media/output/'

# Configurations
chunk_size_m = 3
time_interval_s = 15
scale_factor = 1

# Global video variables:
video_width = 0
video_height = 0
video_frames = 0
video_fps = 0
video_duration = 0


def clean():
    for filename in os.listdir(outputDir):
        file_path = os.path.join(outputDir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            exit()
    print('Deleted: ' + outputDir + ' content')


def load_video_info():
    global video_height
    global video_width
    global video_frames
    global video_fps
    global video_duration

    cv2video = cv2.VideoCapture(videoFile)
    video_height = cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    video_width = cv2video.get(cv2.CAP_PROP_FRAME_WIDTH)
    video_frames = cv2video.get(cv2.CAP_PROP_FRAME_COUNT)
    video_fps = cv2video.get(cv2.CAP_PROP_FPS)
    video_duration = (video_frames / video_fps)

    print("Video info: fps {}, frames: {}, duration {}, size {}x{}".format(int(video_fps), int(video_frames),
                                                                           int(video_duration), video_width,
                                                                           video_height))


def resizeFrame(frame):
    return cv2.resize(frame, (int(frame.shape[1] * scale_factor), int(frame.shape[0] * scale_factor)), interpolation=cv2.INTER_AREA)


def get_video_frames():
    cap = cv2.VideoCapture(videoFile)

    for sec in range(0, int(video_duration)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, (sec * video_fps) - 1)
        ret, frame = cap.read()

        if not ret:
            break

        if (sec % time_interval_s) == 0:
            print('Frame: ' + str(sec) + ' of ' + str(int(video_duration)))
            cv2.imwrite('./media/output/thumb' + str(sec) + '.jpg', resizeFrame(frame))


    cap.release()
    cv2.destroyAllWindows()


def main():
    if os.path.isfile(videoFile):
        print('Video file found: ' + videoFile)
        clean()
        load_video_info()
        get_video_frames()

    else:
        print('Video file not found: ' + videoFile)
        exit()


if __name__ == '__main__':
    main()
