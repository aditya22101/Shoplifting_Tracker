from inference_sdk import InferenceHTTPClient
import supervision as sv
from shoplifting_classifier import output
import pandas as pd
import os
import streamlit as st
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=st.secrets["ROBOFLOW_API_KEY"]
)
def extract_person_coordinate(img):

    result = CLIENT.infer(img, model_id="person-detection-9a6mk/6")
    return result

def saving_annotated_video(name,progress_bar):


    stride=2
    smoother=sv.DetectionsSmoother()
    tracker=sv.ByteTrack()
    generator=sv.get_video_frames_generator(name,stride=stride)
    info=sv.VideoInfo.from_video_path(name)
    fps = info.fps
    total_frames = info.total_frames
    duration = total_frames / fps  # In seconds
    annotator=sv.BoxAnnotator()
    label_annotator=sv.LabelAnnotator()
    
    csv={'Time':[],'ID':[]}
    with sv.VideoSink('out.mp4',video_info=info) as f:
        frame_num=0
        for frame in generator:
            print(type(frame))
            result=extract_person_coordinate(frame)
            detections=sv.Detections.from_inference(result)
            detections=tracker.update_with_detections(detections)
            detections=smoother.update_with_detections(detections)
            target={}
            out=output(frame)
            for tracker_id, xyxy in zip(detections.tracker_id, detections.xyxy):
                x1, y1, x2, y2 = xyxy
                # out=output(frame[int(y1)+4:int(y2)+4,int(x1)+4:int(x2)+4])
                out=output(frame)


                if out==0:
                    csv['Time'].append((frame_num/total_frames)*duration)
                    csv['ID'].append(tracker_id)
                    target[tracker_id]='Shoplifting'
                else:
                    target[tracker_id]='Normal'
            

            frame_num+=stride

            print(target)
            
            labels = [f"#{tracker_id}/{target[tracker_id]}" for tracker_id in detections.tracker_id]
            
            annotated_image=annotator.annotate(scene=frame.copy(),detections=detections)
            annotated_image=label_annotator.annotate(scene=annotated_image.copy(),detections=detections,labels=labels)
            f.write_frame(frame=annotated_image)
            progress_bar.progress(min(frame_num/total_frames, 1.0),text=f"{min(100,round(frame_num/total_frames*100,2))}%")


    data=pd.DataFrame(csv)
    data.to_csv('out.csv')
    print("Saved Successfully")




