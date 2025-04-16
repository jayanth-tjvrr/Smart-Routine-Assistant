from PIL import Image
import torch
import torchvision.transforms as T
from torchvision import models
import numpy as np

# Load model once
def get_model():
    if not hasattr(get_model, "model"):
        model = models.mobilenet_v2(pretrained=True)
        model.eval()
        get_model.model = model
    return get_model.model

# ImageNet class labels
LABELS = None
def get_labels():
    global LABELS
    if LABELS is None:
        import urllib.request
        import json
        url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        LABELS = urllib.request.urlopen(url).read().decode().splitlines()
    return LABELS

FOOD_KEYWORDS = ["pizza", "sandwich", "plate", "hotdog", "spaghetti", "burrito", "cheeseburger", "cake", "ice cream", "food", "dish", "soup", "salad", "omelet", "bagel", "pretzel", "meat loaf", "guacamole", "carbonara", "pancake", "red wine", "espresso", "coffee"]
EXERCISE_KEYWORDS = ["running shoe", "sneaker", "tennis shoe", "dumbbell", "barbell", "soccer ball", "basketball", "volleyball", "rugby ball", "bicycle", "unicycle"]

transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def verify_photo(uploaded_file, target_type):
    try:
        img = Image.open(uploaded_file).convert('RGB')
        x = transform(img).unsqueeze(0)
        model = get_model()
        with torch.no_grad():
            outputs = model(x)
            _, indices = outputs.topk(3)
            labels = [get_labels()[idx] for idx in indices[0]]
        # Check for food
        if target_type == 'meal':
            if any(any(fk in label.lower() for fk in FOOD_KEYWORDS) for label in labels):
                return f"Meal verified! ({labels[0]})"
            else:
                return f"Photo does not look like food. Detected: {labels}"
        elif target_type == 'exercise':
            if any(any(ek in label.lower() for ek in EXERCISE_KEYWORDS) for label in labels):
                return f"Exercise verified! ({labels[0]})"
            else:
                return f"Photo does not look like exercise. Detected: {labels}"
        else:
            return f"Unknown verification. Detected: {labels}"
    except Exception as e:
        return f'Error: {e}'
