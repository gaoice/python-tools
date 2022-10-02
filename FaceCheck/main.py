import cv2
import time
import configparser
import face_recognition
import email_helper
import email_text

# python3

# config
config = configparser.ConfigParser()
config.read("facecheck.ini", encoding='UTF-8')
# DEFAULT
cam_num = int(config.get("DEFAULT", "cam_num"))
tolerance = float(config.get("DEFAULT", "tolerance"))
recognition_times = int(config.get("DEFAULT", "recognition_times"))
min_right_times = int(config.get("DEFAULT", "min_right_times"))
send_mail = config.get("DEFAULT", "send_mail") == 'true'
# DEBUG
debug = config.get("DEBUG", "debug") == 'true'
debug_send_mail = config.get("DEBUG", "debug_send_mail") == 'true'
# EMAIL
from_addr = config.get("EMAIL", "from_addr")
password = config.get("EMAIL", "password")
to_addr = config.get("EMAIL", "to_addr")
smtp_server = config.get("EMAIL", "smtp_server")

win_name = 'FaceCheck Debug'
mail = email_helper.EmailHelper(from_addr, password, to_addr, smtp_server)

video_capture = cv2.VideoCapture(cam_num)
i_image = face_recognition.load_image_file("me.jpg")
i_face_encoding = face_recognition.face_encodings(i_image)[0]
count = 0
right_count = 0
while True:

    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    is_me = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([i_face_encoding], face_encoding, tolerance)
        if True in matches:
            is_me.append(1)
        else:
            is_me.append(0)

    if debug:
        if debug_send_mail:
            mail.thread_send_mail(email_text.debug_header, email_text.debug_text)
            debug_send_mail = False
        for (top, right, bottom, left), this_is_me in zip(face_locations, is_me):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            color = (101, 67, 254)
            name = 'stranger'
            if this_is_me == 1:
                color = (155, 175, 131)
                name = 'me'
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
        cv2.imshow(win_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty(win_name, cv2.WND_PROP_AUTOSIZE) < 1:
            break
    else:
        cv2.waitKey(5)
        print(count, ",", right_count)
        if is_me:
            count += 1
            if 1 in is_me:
                right_count += 1
            if count >= recognition_times:
                print(count, ",", right_count)
                if right_count < min_right_times:
                    file_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + ".jpg"
                    cv2.imwrite(file_name, frame)
                    if send_mail:
                        mail.thread_send_mail(email_text.header, email_text.text, file_name)
                        mail.thread_join()
                break

video_capture.release()
cv2.destroyAllWindows()
