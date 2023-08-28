# import cv2
# import mediapipe as mp
# from flask import Flask, render_template, Response
# import json
# import threading

# app = Flask(__name__)

# #detecção de postura por meio da webcam do pc
# def detect_pose(image):
#     mp_pose = mp.solutions.pose
#     pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = pose.process(image_rgb)

#     if results.pose_landmarks:
#         landmarks = results.pose_landmarks.landmark
        
#         left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
#         right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
#         left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
#         right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
#         left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
#         right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
        
#         if left_hip.y < left_knee.y and right_hip.y < right_knee.y and \
#            left_knee.y < left_ankle.y and right_knee.y < right_ankle.y:
#             return "Postura sentada correta"
#         else:
#             return "Postura sentada incorreta"
#     else:
#         return "Nenhuma postura detectada"

# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Chame a função para detecção de postura
#     result = detect_pose(frame)

#     cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#     cv2.imshow('Sitting Posture Detection', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



# from flask import Flask, render_template, Response
# import cv2
# import mediapipe as mp
# import json
# import threading

# app = Flask(__name__)

# # Função para detecção de postura
# def detect_pose(frame):
#     mp_pose = mp.solutions.pose
#     pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

#     image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = pose.process(image_rgb)

#     if results.pose_landmarks:
#         landmarks = results.pose_landmarks.landmark
#         left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#         right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
#         left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
#         right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
#         left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
#         right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
#         left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
#         right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

#         # Verifica a posição dos ombros, quadris, joelhos e tornozelos
#         if (left_shoulder.y > left_hip.y) and (right_shoulder.y > right_hip.y) and \
#            (left_hip.y > left_knee.y) and (right_hip.y > right_knee.y) and \
#            (left_knee.y > left_ankle.y) and (right_knee.y > right_ankle.y):
#             return "Postura sentada correta"
#         else:
#             return "Postura sentada incorreta"
#     else:
#         return "Nenhuma postura detectada"

# # Função para transmitir o vídeo da câmera
# def generate_frames():
#     cap = cv2.VideoCapture(0)
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/get_posture')
# def get_posture():
#     try:
#         # Chame a função para detecção de postura
#         cap = cv2.VideoCapture(0)
#         ret, frame = cap.read()
#         posture = detect_pose(frame)
#         cap.release()

#         return json.dumps({'posture': posture})
#     except Exception as e:
#         print('Erro ao obter postura:', e)
#         return json.dumps({'posture': 'Erro'})

# if __name__ == '__main__':
#     threading.Thread(target=app.run, args=('0.0.0.0', 5000), daemon=True).start()




from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import json
import threading

app = Flask(__name__)

# Variável para armazenar o estado de calibração
calibration_done = False

# Função para realizar a calibração inicial
def perform_calibration(frame):
    # Exibir instruções de calibração para o usuário
    cv2.putText(frame, "Ajuste sua postura correta na cadeira e pressione Enter para calibrar.", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # Exibir vídeo ao vivo com instruções
    while True:
        cv2.imshow("Calibração", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # Tecla Enter
            break
    
    cv2.destroyAllWindows()

    # Atualizar a variável calibration_done após a calibração
    global calibration_done
    calibration_done = True

# Função para detecção de postura
def detect_pose(frame):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

        # Verifica a posição dos ombros, quadris, joelhos e tornozelos
        if (left_shoulder.y > left_hip.y) and (right_shoulder.y > right_hip.y) and \
           (left_hip.y > left_knee.y) and (right_hip.y > right_knee.y) and \
           (left_knee.y > left_ankle.y) and (right_knee.y > right_ankle.y):
            return "Postura sentada correta"
        else:
            return "Postura sentada incorreta"
    else:
        return "Nenhuma postura detectada"

# Função para transmitir o vídeo da câmera
def generate_frames():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_posture')
def get_posture():
    try:
        global calibration_done
        if not calibration_done:
            # Realiza a calibração inicial antes de verificar a postura
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            perform_calibration(frame)
            cap.release()
            return json.dumps({'posture': 'Calibração realizada. Verificando postura...'})

        # Chame a função para detecção de postura
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        posture = detect_pose(frame)
        cap.release()

        return json.dumps({'posture': posture})
    except Exception as e:
        print('Erro ao obter postura:', e)
        return json.dumps({'posture': 'Erro'})

if __name__ == '__main__':
    threading.Thread(target=app.run, args=('0.0.0.0', 5000), daemon=True).start()
