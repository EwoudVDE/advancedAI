# Setup

## 1. Download Dataset Files
Download and extract the following files from the [BelgiumTS dataset](https://btsd.ethz.ch/shareddata/):

- `DefinedTS.tar.gz`
- `reducedSetTS.txt`
- `Annotations/camera00.tar` through `camera07.tar`
- `Annotations/annotations.tar`
- `Annotations/BelgiumTSD_annotations.zip`

## 2. Install Requirements
Install dependencies using:

```bash
pip install -r requirements.txt
git submodule update --init --recursive

```

## 3. Preprocessing

Run these scripts in order to prepare your dataset for YOLO training:

1. **`reducedSet.py`**  
   Filters dataset to use only selected traffic sign classes.

2. **`YOLOConversion.py`**  
   Converts annotations to YOLO format and organizes images and labels.

3. **`split.py`**  
   Splits the dataset into 80% training and 20% validation.

4. **`rewriteIds.py`**  
   Remaps class IDs to match your reduced label list.

5. **`convertToJpg.py`**  
   Converts `.jp2` images to `.jpg` for YOLO compatibility.

## 4. Training

Use the `cuda.py` script to see if your gpu is available to speed up the training.

Use the `train.py` script to train your YOLOv8 model:

## Notes

You can edit the `train.py` script and swap for other models like `yolo11n.pt`, `yolo8n.pt`, etc.

Modify hyperparameters in the command or data.yaml to experiment.

Ensure your data.yaml file has correct paths and class names.

To test the model use:
```bash
yolo detect predict model=path/to/model.pt source=path/to/Screenshot.png
```

Or use the `video.py` script

## Dataset and References

This project uses the **BelgiumTS** dataset by Radu Timofte and collaborators.
[https://btsd.ethz.ch/shareddata/](https://btsd.ethz.ch/shareddata/)

## Third-Party Code
This project uses modified versions of:

### [Ultralytics YOLOv8](https://github.com/EwoudVDE/ultralytics)
- **Purpose**:CBAM 
- **Modifications**: CBAM
- **License**: [AGPL-3.0](licenses/ultralytics-LICENSE)  
- **Original Source**: [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)  

### [YOLO-V11-CAM](https://github.com/rigvedrs/YOLO-V11-CAM)
- **Purpose**: Class activation maps  
- **License**: [MIT](licenses/YOLO-V11-CAM-LICENSE)  