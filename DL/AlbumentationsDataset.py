import numpy as np
from torchvision import datasets
from PIL import Image
import torch

class AlbumentationsDataset(datasets.ImageFolder):
    def __init__(self, root, transform=None, cutmix=None):
        super(AlbumentationsDataset, self).__init__(root, transform=None)
        self.albumentations_transform = transform
        self.cutmix = cutmix

    def __getitem__(self, index):
        path, target = self.samples[index]
        sample = self.loader(path)
        if self.albumentations_transform is not None:
            sample = self.albumentations_transform(image=np.array(sample))['image']

        if self.cutmix and np.random.rand() < self.cutmix.prob:
            # 배치가 아닌 경우 에러가 발생하므로, 이를 방지하기 위한 조건
            if isinstance(sample, torch.Tensor) and sample.dim() == 4:  # 배치인지 확인
                sample, target_a, target_b, lam = self.cutmix(sample, torch.tensor([target]))
                return sample, target_a, target_b, lam

        return sample, target
