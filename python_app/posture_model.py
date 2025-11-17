# posture_model.py
import cv2
import mediapipe as mp
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier

mp_pose = mp.solutions.pose

def extract_pose_features(frame, pose):
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if not results.pose_landmarks:
        return None

    lm = results.pose_landmarks.landmark

    def get_xy(l):
        return np.array([l.x, l.y])

    left_shoulder = get_xy(lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
    right_shoulder = get_xy(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
    left_hip = get_xy(lm[mp_pose.PoseLandmark.LEFT_HIP.value])
    right_hip = get_xy(lm[mp_pose.PoseLandmark.RIGHT_HIP.value])
    left_knee = get_xy(lm[mp_pose.PoseLandmark.LEFT_KNEE.value])
    right_knee = get_xy(lm[mp_pose.PoseLandmark.RIGHT_KNEE.value])

    # 5 biomechanical features
    shoulder_width = np.linalg.norm(left_shoulder - right_shoulder)
    hip_width = np.linalg.norm(left_hip - right_hip)
    left_leg_length = np.linalg.norm(left_hip - left_knee)
    right_leg_length = np.linalg.norm(right_hip - right_knee)
    body_tilt = np.linalg.norm(left_shoulder - left_hip)

    return np.array([shoulder_width, hip_width, left_leg_length, right_leg_length, body_tilt])

def train_dummy_model():
    X = np.random.rand(100, 5)
    y = np.random.randint(0, 2, 100)
    model = RandomForestClassifier()
    model.fit(X, y)
    os.makedirs("python_app/data", exist_ok=True)
    with open("python_app/data/posture_model.pkl", "wb") as f:
        pickle.dump(model, f)

def analyze_video(video_path):
    with open("python_app/data/posture_model.pkl", "rb") as f:
        model = pickle.load(f)

    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose()
    frame_count, correct = 0, 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        features = extract_pose_features(frame, pose)
        if features is not None:
            frame_count += 1
            pred = model.predict([features])[0]
            if pred == 1:
                correct += 1

    cap.release()
    accuracy = round((correct / frame_count) * 100, 2) if frame_count > 0 else 0
    feedback = "✅ Excellent posture!" if accuracy > 80 else "⚠️ Needs improvement."
    return accuracy, feedback
