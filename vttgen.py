import os
import cv2
import shutil
import numpy as np

# Path to the directory containing the images
videoFile = './media/input/468.mp4'
outputDir = './media/output/'

# Configurations
chunk_size_m = 3
time_interval_s = 14
scale_factor = 0.25

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
    frames = []
    cap = cv2.VideoCapture(videoFile)
    for sec in range(0, int(video_duration)):
        if (sec % time_interval_s) == 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, (sec * video_fps) - 1)
            ret, frame = cap.read()

            if not ret:
                break

            print('Frame: ' + str(sec) + ' of ' + str(int(video_duration)))
            frames.append(resizeFrame(frame))


    cap.release()
    cv2.destroyAllWindows()
    return frames


def main():
    if os.path.isfile(videoFile):
        print('Video file found: ' + videoFile)
        clean()
        load_video_info()
        frames = get_video_frames()

        frames_count = len(frames)
        wide_img_quantity = int(frames_count / chunk_size_m)

        if (frames_count % chunk_size_m) != 0:
            print('Warning: frames count is not multiple of chunk size')
            blank_images_quantity = chunk_size_m - (frames_count - (wide_img_quantity * chunk_size_m))
            frame_size_width = int(frames[0].shape[0])
            frame_size_height = int(frames[0].shape[1])
            blank_image = np.zeros((frame_size_width, frame_size_height, 3), np.uint8)

            for i in range(0, blank_images_quantity):
                frames.append(blank_image)

            wide_img_quantity += 1

        print('frames: ' + str(len(frames)))

        for i in range(0, wide_img_quantity):
            list_of_images = []
            for j in range(0 + (i * chunk_size_m), chunk_size_m * (i + 1)):
                list_of_images.append(frames[j])

            x = np.concatenate(list_of_images, axis=1)
            cv2.imwrite('./media/output/' + str(i) + '.jpg', x)

        print('Done!')



    else:
        print('Video file not found: ' + videoFile)
        exit()


if __name__ == '__main__':
    main()
