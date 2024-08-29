import cv2

# Carrega os classificadores de detecção de rosto e perfil
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

# Inicializa a captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Inicializa o tracker
tracker = cv2.TrackerCSRT_create()

# Flag para iniciar o tracker
tracking = False

# Pega a largura e altura do quadro da webcam
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_aspect_ratio = frame_width / frame_height

# Fator de aumento do crop (quanto maior, mais área ao redor do rosto será exibida)
crop_factor = 3.5 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if not tracking:
        # Detecta rostos frontais
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7, minSize=(60, 60))

        # Se nenhum rosto frontal for detectado, tenta detectar um perfil de rosto
        if len(faces) == 0:
            faces = profile_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7, minSize=(60, 60))

        # Se um rosto ou cabeça foi detectado
        if len(faces) > 0:
            (x, y, w, h) = faces[0]

            # Iniciar o tracker com o bounding box detectado
            tracker.init(frame, (x, y, w, h))
            tracking = True
    else:
        # Atualizar o tracker
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]

            # Calcular o centro do rosto
            center_x, center_y = x + w // 2, y + h // 2

            # Ajustar as dimensões do crop para manter a proporção original
            if frame_aspect_ratio > 1:
                box_w = int(w * crop_factor)
                box_h = int(box_w / frame_aspect_ratio)
            else:
                box_h = int(h * crop_factor)
                box_w = int(box_h * frame_aspect_ratio)

            # Calcular os limites do novo quadro mantendo a proporção
            start_x = max(center_x - box_w // 2, 0)
            start_y = max(center_y - box_h // 2, 0)
            end_x = min(center_x + box_w // 2, frame.shape[1])
            end_y = min(center_y + box_h // 2, frame.shape[0])

            # Reduzir o tamanho do crop se ultrapassar os limites do frame
            if end_x - start_x != box_w:
                box_w = end_x - start_x
                box_h = int(box_w / frame_aspect_ratio)
            if end_y - start_y != box_h:
                box_h = end_y - start_y
                box_w = int(box_h * frame_aspect_ratio)

            # Recorta o quadro original mantendo a proporção
            cropped_frame = frame[start_y:end_y, start_x:end_x]
            cropped_frame = cv2.resize(cropped_frame, (frame_width, frame_height))
            cv2.imshow('Video', cropped_frame)
        else:
            # Se o rastreamento falhar, reinicie a detecção
            tracking = False
            cv2.imshow('Video', frame)

    # Exibe o vídeo original se nada for detectado
    if not tracking and len(faces) == 0:
        cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
