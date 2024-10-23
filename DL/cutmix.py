import numpy as np
import torch

class CutMix:
    def __init__(self, size, beta=1.0, prob=0.5):
        self.size = size
        self.beta = beta
        self.prob = prob

    def __call__(self, image, label):
        lam = np.random.beta(self.beta, self.beta)
        rand_index = torch.randperm(image.size(0))  # 배치 단위 인덱스 생성
        target_a = label
        target_b = label[rand_index]  # 인덱스를 통해 라벨을 섞음

        bbx1, bby1, bbx2, bby2 = self._rand_bbox(image.size(), lam)
        image[:, :, bbx1:bbx2, bby1:bby2] = image[rand_index, :, bbx1:bbx2, bby1:bby2]

        lam = 1 - ((bbx2 - bbx1) * (bby2 - bby1) / (image.size()[-1] * image.size()[-2]))
        return image, target_a, target_b, lam

    def _rand_bbox(self, size, lam):
        W = size[2]
        H = size[3]
        cut_rat = np.sqrt(1. - lam)
        cut_w = int(W * cut_rat)
        cut_h = int(H * cut_rat)

        cx = np.random.randint(W)
        cy = np.random.randint(H)

        bbx1 = np.clip(cx - cut_w // 2, 0, W)
        bby1 = np.clip(cy - cut_h // 2, 0, H)
        bbx2 = np.clip(cx + cut_w // 2, 0, W)
        bby2 = np.clip(cy + cut_h // 2, 0, H)

        return bbx1, bby1, bbx2, bby2
