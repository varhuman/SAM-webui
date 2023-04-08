import matplotlib.pyplot as plt
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import os
import cv2

class MaskUtils:
    def __init__(self, predictor):
        self.sam_predictor:SamPredictor = predictor

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

    def get_masks(self, input_point, input_label):
        masks, scores, logits = self.sam_predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
        )
        return masks, scores, logits

    def get_color(self, label):
        if label == 1:
            return (0, 255, 0)  # Green
        elif label == 2:
            return (255, 0, 0)  # Red
        elif label == 3:
            return (0, 0, 255)  # Blue
        else:
            return (255, 255, 255)  # White

    
    def get_masks_by_masks(self, input_point, input_label, mask_input):
        masks, scores, logits = self.sam_predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            mask_input=mask_input[None, :, :],
            multimask_output=False,
        )
        return masks, scores, logits

    def show_masks_one_figure(self, image, input_point, input_label):
        self.sam_predictor.set_image(image)

        masks, scores, logits = self.get_masks(input_point, input_label)
        # use subplots to show all masks
        fig, axes = plt.subplots(1, len(masks), figsize=(10, 10))
        for i, (mask, score, ax) in enumerate(zip(masks, scores, axes)):
            ax.imshow(image)
            self.show_mask(mask, ax)
            self.show_points(input_point, input_label, ax)
            ax.set_title(f"Mask {i+1}, Score: {score:.3f}", fontsize=18)
            ax.axis('off')
        plt.show() 

    # def show_best_mask(self, image, input_point, input_label, save=False):
    #     self.sam_predictor.set_image(image)
    #     _, scores, logits = self.get_masks(input_point, input_label)

    #     mask_input = logits[np.argmax(scores), :, :]
    #     masks, _, _ = self.get_masks_by_masks(input_point, input_label, mask_input)

    #     plt.figure(figsize=(10, 10))
    #     plt.imshow(image)
    #     self.show_mask(masks, plt.gca())
    #     self.show_points(input_point, input_label, plt.gca())
    #     plt.axis('off')

    #     if save:
    #         output_path = os.path.join("output", f".png")
    #         plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    #         return output_path
    #     else:
    #         plt.show()

    def show_best_mask(self, image, input_point, input_label, save=False):
        self.sam_predictor.set_image(image)
        _, scores, logits = self.get_masks(input_point, input_label)

        mask_input = logits[np.argmax(scores), :, :]
        masks, _, _ = self.get_masks_by_masks(input_point, input_label, mask_input)

        # Create a color mask
        color_mask = np.zeros_like(image)
        for i in range(len(input_label)):
            color_mask[masks[i] > 0] = self.get_color(input_label[i])

        # Blend the original image with the color mask
        blended_image = cv2.addWeighted(image, 0.7, color_mask, 0.3, 0)

        # Draw points on the blended image
        for i in range(len(input_point)):
            x, y = input_point[i]
            label = input_label[i]
            color = self.get_color(label)
            cv2.circle(blended_image, (x, y), 10, color, -1)

        if save:
            output_path = os.path.join("output", f"output.png")
            cv2.imwrite(output_path, cv2.cvtColor(blended_image, cv2.COLOR_RGB2BGR))
            return output_path
        else:
            cv2.imshow("Blended Image", cv2.cvtColor(blended_image, cv2.COLOR_RGB2BGR))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
