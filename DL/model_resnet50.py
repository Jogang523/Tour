from torchvision import models
import torch.nn as nn

def get_resnet50_model(num_classes, pretrained=True):
    model = models.resnet50(pretrained=pretrained)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    return model
