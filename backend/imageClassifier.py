import torchvision
from torchvision import transforms
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F

class ResNet9(nn.Module):
    def __init__(self, in_channels, num_classes):
        super(ResNet9, self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1)
        self.res1 = nn.Sequential(nn.Conv2d(128, 128, kernel_size=3, padding=1), nn.ReLU(), nn.Conv2d(128, 128, kernel_size=3, padding=1))

        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1)
        self.conv4 = nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1)
        self.res2 = nn.Sequential(nn.Conv2d(512, 512, kernel_size=3, padding=1), nn.ReLU(), nn.Conv2d(512, 512, kernel_size=3, padding=1))

        self.classifier = nn.Sequential(nn.MaxPool2d(4), nn.Flatten(), nn.Linear(512, num_classes))

    def forward(self, xb):
        out = F.relu(self.conv1(xb))
        out = F.relu(self.conv2(out))
        out = self.res1(out) + out
        out = F.relu(self.conv3(out))
        out = F.relu(self.conv4(out))
        out = self.res2(out) + out
        out = self.classifier(out)
        return out
model = torch.load("plant-disease-model-complete.pth", map_location=torch.device('cpu'))
classes=['Apple___Apple_scab',
 'Apple___Black_rot',
 'Apple___Cedar_apple_rust',
 'Apple___healthy',
 'Blueberry___healthy',
 'Cherry_(including_sour)___Powdery_mildew',
 'Cherry_(including_sour)___healthy',
 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 'Corn_(maize)___Common_rust_',
 'Corn_(maize)___Northern_Leaf_Blight',
 'Corn_(maize)___healthy',
 'Grape___Black_rot',
 'Grape___Esca_(Black_Measles)',
 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 'Grape___healthy',
 'Orange___Haunglongbing_(Citrus_greening)',
 'Peach___Bacterial_spot',
 'Peach___healthy',
 'Pepper,_bell___Bacterial_spot',
 'Pepper,_bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Raspberry___healthy',
 'Soybean___healthy',
 'Squash___Powdery_mildew',
 'Strawberry___Leaf_scorch',
 'Strawberry___healthy',
 'Tomato___Bacterial_spot',
 'Tomato___Early_blight',
 'Tomato___Late_blight',
 'Tomato___Leaf_Mold',
 'Tomato___Septoria_leaf_spot',
 'Tomato___Spider_mites Two-spotted_spider_mite',
 'Tomato___Target_Spot',
 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato___Tomato_mosaic_virus',
 'Tomato___healthy']
from PIL import Image

transform = transforms.Compose([
    transforms.Resize((256, 256)), 
    transforms.ToTensor(),  
])

def predict_image(image_path, model):
    image = Image.open(image_path)  
    image = transform(image).unsqueeze(0)
    model.eval()

    with torch.no_grad():  
        output = model(image)
    
    _, predicted_class = torch.max(output, 1)
    return predicted_class.item()

