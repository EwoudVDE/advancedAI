import argparse
import torch
from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2
import os

def apply_colormap_on_image(org_im, activation, colormap_name='JET'):
    color_map = cv2.applyColorMap(np.uint8(255 * activation), cv2.COLORMAP_JET)
    color_map = np.float32(color_map) / 255
    org_im = np.float32(org_im) / 255
    cam = 0.3 * color_map + 0.5 * org_im
    cam = cam / np.max(cam)
    return np.uint8(255 * cam)

def main():
    parser = argparse.ArgumentParser(description="YOLOv8 GradCAM")
    parser.add_argument("--model", type=str, default="runs/detect/train2/weights/best.pt", help="YOLOv8 model path")
    parser.add_argument("--image", type=str, default="testImages/Screenshot.png", help="Input image path")
    parser.add_argument("--output", type=str, default="gradcam_output.jpg", help="Grad-CAM output path")
    args = parser.parse_args()

    model = YOLO(args.model)
    model.model.eval()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.model.to(device)

    results = model(args.image)

    img = cv2.imread(args.image)
    img = cv2.resize(img, (640, 640))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if not results or not results[0].boxes:
        print("No detections found.")
        return

    # Pick the last Conv layer
    target_layer = model.model.model[-2]

    # Register hook to get activations
    activations = []
    def hook_fn(module, input, output):
        activations.append(output)

    handle = target_layer.register_forward_hook(hook_fn)

    # Forward pass to trigger the hook
    model.predict(args.image, device=device, verbose=False)

    handle.remove()

    if not activations:
        print("Failed to extract activations.")
        return

    # Take the first detection and generate CAM
    activation_map = activations[0].squeeze().mean(0).cpu().numpy()
    activation_map = cv2.resize(activation_map, (img.shape[1], img.shape[0]))
    activation_map = (activation_map - activation_map.min()) / (activation_map.max() - activation_map.min() + 1e-8)

    heatmap_img = apply_colormap_on_image(img_rgb, activation_map)

    # Save result
    output_img = Image.fromarray(heatmap_img)
    output_img.save(args.output)
    print(f"Saved Grad-CAM output to {args.output}")
    plt.imshow(output_img)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
