from torchvision import models
import torch.nn as nn

def get_vgg19_model(num_classes, pretrained=True):
    model = models.vgg19(pretrained=pretrained)
    num_ftrs = model.classifier[6].in_features
    model.classifier[6] = nn.Linear(num_ftrs, num_classes)
    return model
