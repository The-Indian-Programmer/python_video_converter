from apis_backend.models import Users
from ..helper.function import getFilePath
from django.conf import settings
import os
import cv2
import re
from .cartoonize import WB_Cartoonize
import time
class authService:
    def __init__(self):
        self.users = Users()
        weights_dir = os.path.join('apis_backend/services', "saved_models")
        self.cartoonizer = WB_Cartoonize(weights_dir, gpu=False)

    def register(self, form_data, files):

        start_time = time.time()


        folderName = getFilePath(files)
        fileName = folderName['fileName']
        upload_directory = os.path.join(settings.MEDIA_ROOT, folderName['path'])
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)
            
        with open(os.path.join(upload_directory, fileName), 'wb+') as destination:
            for chunk in files['file_field'].chunks():
                destination.write(chunk)
            
        # Extract Frames from video
        video_path = os.path.join(upload_directory, fileName)
        
        video = cv2.VideoCapture(video_path)
        frame_count = 0
        
        images_path2 = os.path.join(settings.MEDIA_ROOT, 'frames_images')
        images_path = os.path.join(images_path2, folderName['fileName'].split('.')[0])
        cap = cv2.VideoCapture(video_path)

        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # video_writer = cv2.VideoWriter('results\output.avi', cv2.VideoWriter_fourcc('D','I','V','X'),  fps, (width, height))

        #Loop through each frame
        # for frame_idx in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):

        #     #Reads each frame
        #     ret, frame = cap.read()

        #     cartoon_image = cv2.stylization(frame, sigma_s=150, sigma_r=0.25) 

        #     cv2.imshow('Video Player', cartoon_image)

        #     video_writer.write(cartoon_image)

        #     if cv2.waitKey(10) & 0xFF == ord('q'):
        #         break

        #     #Closes down everything
        #     cap.release()
        #     cv2.destroyAllWindows()

        #     video_writer.release()

        if not os.path.exists(images_path):
            os.makedirs(images_path)
        
        while True:
            success, frame = video.read()
            if not success:
                break
            uploadedFileName = f"frame_{frame_count}.jpg"
            cv2.imwrite(os.path.join(images_path, uploadedFileName), frame)
            frame_count += 1
            
        video.release()
        
        # Now cartoonize each image inside the folder and save these images in another folder
        cartoon_images_path = os.path.join(settings.MEDIA_ROOT, 'cartoon_images', folderName['fileName'].split('.')[0])
        
        if not os.path.exists(cartoon_images_path):
            os.makedirs(cartoon_images_path)
        
        for image in os.listdir(images_path):
            image_path = os.path.join(images_path, image)
            
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            cartoon_image = self.cartoonizer.infer(img)
            
            
            cartoon_image = cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(cartoon_images_path, image), cartoon_image)
            
        # Now create a video from the cartoon images
        cartoon_video_path = os.path.join(settings.MEDIA_ROOT, 'cartoon_videos', folderName['fileName'].split('.')[0])
        
        if not os.path.exists(cartoon_video_path):
            os.makedirs(cartoon_video_path)
        
        def natural_sort(list_of_strings):
            def convert_to_int(text):
                return int(text) if text.isdigit() else text
            def alphanum_key(key):
                return [convert_to_int(c) for c in re.split('([0-9]+)', key)]
            return sorted(list_of_strings, key=alphanum_key)

        images = [img for img in natural_sort(os.listdir(cartoon_images_path)) if img.endswith(".jpg")]
        frame = cv2.imread(os.path.join(cartoon_images_path, images[0]))
        
        height, width, layers = frame.shape
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        newvideo = cv2.VideoWriter(os.path.join(cartoon_video_path, 'cartoon_video.mp4'), fourcc, 30, (width, height))
        
        for image in images:
            image_path = os.path.join(cartoon_images_path, image)
            frame = cv2.imread(image_path)
            newvideo.write(frame)
            
        cv2.destroyAllWindows()
        newvideo.release()

        end_time = time.time()

        time_taken = end_time - start_time

        print(time_taken, 'time taken')

        print("Total time taken : ", time_taken)
        
        return {'status': True, 'message': 'User registered successfully', 'data': time_taken}


    
    def login(self, form_data):

        def natural_sort(list_of_strings):
            def convert_to_int(text):
                return int(text) if text.isdigit() else text
            def alphanum_key(key):
                return [convert_to_int(c) for c in re.split('([0-9]+)', key)]
            return sorted(list_of_strings, key=alphanum_key)

        cartoon_images_path = os.path.join("frames_images", "bdb0c4a6-b415-4878-a4f0-1126f1a4e8bf")

        images = [img for img in natural_sort(os.listdir(cartoon_images_path)) if img.endswith(".jpg")]
        frame = cv2.imread(os.path.join(cartoon_images_path, images[0]))
        
        height, width, layers = frame.shape

        cartoon_video_path = os.path.join("cartoon_videos", "bdb0c4a6-b415-4878-a4f0-1126f1a4e8bf")
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        newvideo = cv2.VideoWriter(os.path.join(cartoon_video_path, 'cartoon_video.mp4'), fourcc, 30, (width, height))

        for image in images:
            image_path = os.path.join(cartoon_images_path, image)
            frame = cv2.imread(image_path)
            newvideo.write(frame)
            
        cv2.destroyAllWindows()
        newvideo.release()

    
    def adminLogin(self, form_data):
        email = form_data['email']
        password = form_data['password']

        user = self.users.get(email=email, password=password)
        return {'status': True, 'message': 'Admin logged in successfully', 'data': user}
    
    def refreshToken(self, user_data):
        user = self.users.get(id=user_data['id'])
        return {'status': True, 'message': 'Token refreshed successfully', 'data': user}
    
