import os
from PIL import Image
from torch.utils.data import Dataset
import numpy as np

class SegmentationDataset(Dataset):
    """Dataset for segmentation"""
    def __init__(self, images_dir, masks_dir, transform=None):
        """Initialize the dataset

        Parameters
        ----------
        images_dir: str
            Path to the directory containing the images
        masks_dir: str
            Path to the directory containing the masks
        transform: Callable
            Tranformation function to be applied to the images and masks in order to perform data augmentation.
        """
        self.image_dir = images_dir
        self.mask_dir = masks_dir
        self.transform = transform
        self.images = os.listdir(images_dir)
        self.masks = os.listdir(masks_dir)
    
    def __getitem__(self, idx):
        image_path = os.path.join(self.image_dir, self.images[idx])
        mask_path = os.path.join(self.mask_dir, self.masks[idx])

        image = np.array(Image.open(image_path).convert("RGB"))
        mask = np.array(Image.open(mask_path).convert("L"), dtype=np.float32)   # so [0-255]
        mask[mask == 255.0] = 1.0   # Convert 255 to 1, indicating the probability of the pixel being the object

        if self.transform is not None:
            augmentations = self.transform(image=image, mask=mask)
            image = augmentations["image"]
            mask = augmentations["mask"]

        return image, mask