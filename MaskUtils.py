import matplotlib.pyplot as plt
import numpy as np

class MaskUtils:
    def show_mask(self, mask, ax, random_color=False):
        if random_color:
            color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
        else:
            color = np.array([30/255, 144/255, 255/255, 0.6])
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        ax.imshow(mask_image)
        
    def show_points(self, coords, labels, ax, marker_size=375):
        pos_points = coords[labels==1]
        neg_points = coords[labels==0]
        ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
        ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
        
    def show_box(self, box, ax):
        x0, y0 = box[0], box[1]
        w, h = box[2] - box[0], box[3] - box[1]
        ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))  

    def showMasksInOneFigure(self, masks, scores, image, input_point, input_label):
        # use subplots to show all masks
        fig, axes = plt.subplots(1, len(masks), figsize=(10, 10))
        for i, (mask, score, ax) in enumerate(zip(masks, scores, axes)):
            ax.imshow(image)
            self.show_mask(mask, ax)
            self.show_points(input_point, input_label, ax)
            ax.set_title(f"Mask {i+1}, Score: {score:.3f}", fontsize=18)
            ax.axis('off')
        plt.show()