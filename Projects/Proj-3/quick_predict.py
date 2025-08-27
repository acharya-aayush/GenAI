from pathlib import Path
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

# Config
images = ['cats.jpg', 'dogs.jpg']
model_path = 'cats_dogs_cnn_quick.pth'
classes = ['cats', 'dogs']

# Model definition (must match training)
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=2):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2,2)
        self.fc1 = nn.Linear(64 * 16 * 16, 128)
        self.fc2 = nn.Linear(128, num_classes)
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = F.relu(self.conv3(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Transforms
transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])
])

# Load model
device = torch.device('cpu')
if not Path(model_path).exists():
    print(f"Model file '{model_path}' not found. Please run training.")
    raise SystemExit(1)
model = SimpleCNN(num_classes=len(classes))
state = torch.load(model_path, map_location=device)
model.load_state_dict(state)
model.to(device).eval()

# Predict
for img_name in images:
    p = Path(img_name)
    if not p.exists():
        print(f"Image not found: {img_name}")
        continue
    img = Image.open(p).convert('RGB')
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(x)
        probs = torch.softmax(out, dim=1)[0]
        idx = int(probs.argmax().item())
        conf = float(probs[idx].item())
    print(f"{img_name} -> {classes[idx]} (confidence: {conf:.3f}) | probs: {{'cats':{probs[0]:.3f}, 'dogs':{probs[1]:.3f}}}")
