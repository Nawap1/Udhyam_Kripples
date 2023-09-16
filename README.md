# The Kripples
## Project Idea:
We intend to improve public transportation in Nepal using AI. We are aware of the difficulties travelers face, such as the unavailability of vehicles in uniform time and concerns about safety. Our project leverages face recognition technology to make using public transportation more convenient. When a passenger approaches the ticketing gate or boarding point, our technology scans their faces for verification. Passengers may quickly and simply register their faces. This reduces waiting times and increases overall security by doing away with the requirement for actual tickets or smartcards. Our working prototype demonstrates how easy, quick, and efficient this approach is. By implementing face recognition, we hope to enhance the user experience and increase the effectiveness and security of public transit in Nepal.

## Project Overview
- Project Demo
- Dependencies
- Face Recognition
- Drowsiness Classifier
- Price Prediction Based on Distance
- Realtime Bus Tracking

  ### Project Demo

  ### Dependencies
  - Python 3.10
  - Numpy
  - OpenCV
  - DeepFace
  - HTML, CSS, and JS
  - OSM and LeafLeet
  - PyTorch
  - Mediapipe

  ### Face Recognition
  We are using the power of DeepFace for facial recognition. Deepface is a lightweight face recognition and facial attribute analysis (age, gender, emotion, and race) framework for Python. It is a hybrid face recognition framework wrapping state-of-the-art models: VGG-Face, Google FaceNet, OpenFace, Facebook DeepFace, DeepID, ArcFace, Dlib, and SFace. We are going to use a camera at the entrance and the exit of the bus. When the Passenger comes to the entrance, they will have their photo taken and the photo is stored in the database, the picture is turned into a face embedding using a DeepFace model. Then at the exit, the picture is taken using the camera at the exit, the face embedding is calculated of the image at the exit and it is compared with other embeddings in the database. If the distance is very low, it'll recognize that person.

  ### Mask Detection
  It is checked if the person is wearing a mask before taking the data for facial recognition as it can hinder the performance of the facial recognition model. Masks cover over half of the face which can lead to poor performance of our facial recognition model which may even lead to false positives or false negatives. If the person is wearing a mask, they are instructed to take off the mask while entering and leaving the bus.
  
  ### Drowsiness Classifier
  For this, we used a library called Mediapipe which is owned by Google. It was released in early 2019. MediaPipe is an open-source framework for building pipelines to perform computer vision inference over arbitrary sensory data such as video or audio. In the case of the drowsiness classifier, we used mediapipe to check if the person was closing his/her eyes. If the person closes their eyes for a particular duration of time alert is sent to the driver. This ensures that the driver is driving with his full attention and doesn't fall asleep and put the passengers' lives in danger. It can especially be quite useful in long drives and night drivers as drivers as bus drivers are prone to fall asleep in these conditions.
  
    ### Price Prediction Based on Distance
  Leaflet, a popular javascript library used for interactive maps is used to predict the distance from point A to point B according to the route the bus took. An array of geolocation coordinates is kept as the bus moves using GPS, so the array from point A to point B is sliced, and then the leaflet is used to compute the distance from those coordinate arrays.
  
    ### Realtime Bus Tracking
    Using GPS of the bus we are able to track the bus in real time using open street map (OSM) which will make it more accessable to the users.

  
  
