import face_recognition

image = face_recognition.load_image_file("0001.jpg")
face_locations = face_recognition.face_locations(image, model="cnn")
