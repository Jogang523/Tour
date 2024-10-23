from torchvision import models
import torch.nn as nn

def get_efficientnet_model(num_classes, pretrained=True):
    model = models.efficientnet_b0(pretrained=pretrained)
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_ftrs, num_classes)
    return model
