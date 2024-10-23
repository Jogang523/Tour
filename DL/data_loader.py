import os
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torch.utils.data import DataLoader
from AlbumentationsDataset import AlbumentationsDataset
from cutmix import CutMix  # CutMix 임포트

def get_dataloaders(data_dir, batch_size=32, cutmix_prob=0.5):
    train_dir = os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')
    test_dir = os.path.join(data_dir, 'test')

    # 데이터 증강 및 전처리
    train_transform = A.Compose([
        A.Resize(224, 224),
        A.RandomRotate90(),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

    # CutMix 적용
    cutmix_transform = CutMix(size=(224, 224), beta=1.0, prob=cutmix_prob)

    val_test_transform = A.Compose([
        A.Resize(224, 224),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

    image_datasets = {
        'train': AlbumentationsDataset(train_dir, transform=train_transform, cutmix=cutmix_transform),
        'val': AlbumentationsDataset(val_dir, transform=val_test_transform),
        'test': AlbumentationsDataset(test_dir, transform=val_test_transform),
    }

    dataloaders = {
        'train': DataLoader(image_datasets['train'], batch_size=batch_size, shuffle=True),
        'val': DataLoader(image_datasets['val'], batch_size=batch_size, shuffle=False),
        'test': DataLoader(image_datasets['test'], batch_size=batch_size, shuffle=False),
    }

    return dataloaders, len(image_datasets['train'].classes)
