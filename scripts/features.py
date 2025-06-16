import torch
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms
from ultralytics import YOLO

# Load your YOLOv8 model (with your custom weights)
model = YOLO('external/ultralytics/runs/detect/train/weights/best.pt')

# Prepare your input image
img_path = 'testImages/Capture.png'
img = Image.open(img_path).convert("RGB")
transform = transforms.Compose([
    transforms.Resize((640, 640)),
    transforms.ToTensor(),
])
input_tensor = transform(img).unsqueeze(0)  # batch size 1

# Layer names from your list (index matches model.model.model layers)
layer_names = [
    "Conv", "CBAM", "Conv", "CBAM", "C2f", "Conv", "CBAM", "C2f", "Conv", "CBAM",
    "C2f", "Conv", "CBAM", "C2f", "SPPF", "Upsample", "Concat", "C2f", "CBAM",
    "Upsample", "Concat", "C2f", "CBAM", "Conv", "Concat", "C2f", "CBAM", "Conv",
    "Concat", "C2f", "CBAM", "Conv", "Concat", "C2f"
]

# Dictionary to store activations from all layers
activations = {}

# Hook function to save output feature map
def hook_fn(module, input, output, layer_idx):
    if isinstance(output, tuple):
        activations[layer_idx] = output[0].detach()
    else:
        activations[layer_idx] = output.detach()
# Register hooks for all layers
hooks = []
for i, layer in enumerate(model.model.model):
    # Register hook with lambda capturing layer idx
    hooks.append(layer.register_forward_hook(lambda m, inp, out, i=i: hook_fn(m, inp, out, i)))

# Run forward pass
model.model.eval()
with torch.no_grad():
    _ = model.model(input_tensor)

# Visualize first 3 feature maps of each layer
for i, layer_name in enumerate(layer_names):
    if i in activations:
        feature_maps = activations[i][0]  # [channels, H, W]
        num_maps = min(6, feature_maps.shape[0])  # show up to 3 feature maps

        fig, axes = plt.subplots(1, num_maps, figsize=(5 * num_maps, 4))
        if num_maps == 1:
            axes = [axes]  # to iterate uniformly

        for j in range(num_maps):
            axes[j].imshow(feature_maps[j].cpu(), cmap='viridis')
            axes[j].axis('off')

        plt.suptitle(f"Layer {i} - {layer_name} feature maps")
        plt.show()
    else:
        print(f"No activation for layer {i} - {layer_name}")

# Remove hooks
for hook in hooks:
    hook.remove()
