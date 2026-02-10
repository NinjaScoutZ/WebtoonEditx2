"""
ImageTrans ONNX-based text detector.
Uses ONNX models from ImageTrans/models directory for comic text detection.
Supports multiple models via dropdown selection.
"""
import os
import json
import numpy as np
import cv2
from typing import List, Tuple

from utils.textblock import TextBlock
from utils.registry import Registry

# Import from parent package
from . import TEXTDETECTORS, TextDetectorBase, register_textdetectors
from ..base import DEVICE_SELECTOR

# Default path to ImageTrans models
IMAGETRANS_MODELS_DIR = r"C:\Users\dansa\Desktop\ImageTrans\models"


def scan_available_models(models_dir: str) -> list:
    """Scan the ImageTrans models directory for available ONNX models."""
    available = []
    if not os.path.isdir(models_dir):
        return available
    for name in os.listdir(models_dir):
        model_dir = os.path.join(models_dir, name)
        if os.path.isdir(model_dir):
            json_path = os.path.join(model_dir, "model.json")
            onnx_path = os.path.join(model_dir, "model.onnx")
            if os.path.exists(json_path) and os.path.exists(onnx_path):
                available.append(name)
    return available


# Get available models at import time
_AVAILABLE_MODELS = scan_available_models(IMAGETRANS_MODELS_DIR)
if not _AVAILABLE_MODELS:
    _AVAILABLE_MODELS = ['comic-text-and-bubble-detector']  # fallback


@register_textdetectors('imagetrans_onnx')
class ImageTransOnnxDetector(TextDetectorBase):
    """
    ONNX-based text detector using ImageTrans models.
    Loads model.json for config and model.onnx for inference.
    """

    download_file_list = []  # No downloads needed, models are local

    params = {
        'model_name': {
            'type': 'selector',
            'options': _AVAILABLE_MODELS,
            'select': _AVAILABLE_MODELS[0] if _AVAILABLE_MODELS else 'comic-text-and-bubble-detector'
        },
        'confidence_threshold': {
            'type': 'selector',
            'options': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            'select': 0.3
        },
        'description': 'ImageTrans ONNX Detector (local models)'
    }

    def __init__(self, **params):
        self.session = None
        self.model_config = {}
        self.input_width = 640
        self.input_height = 640
        self._current_model_name = ''
        super().__init__(**params)

    def setup_detector(self):
        """Load the ONNX model specified in params."""
        import onnxruntime as ort

        model_name = self.params['model_name']['select']
        model_dir = os.path.join(IMAGETRANS_MODELS_DIR, model_name)

        # Load config
        json_path = os.path.join(model_dir, "model.json")
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                self.model_config = json.load(f)

        self.input_width = self.model_config.get('width', 640)
        self.input_height = self.model_config.get('height', 640)

        # Load ONNX model
        onnx_path = os.path.join(model_dir, "model.onnx")
        providers = ['CPUExecutionProvider']
        try:
            # Try CUDA first
            if 'CUDAExecutionProvider' in ort.get_available_providers():
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        except Exception:
            pass

        self.session = ort.InferenceSession(onnx_path, providers=providers)
        self._current_model_name = model_name

        # Get input/output info
        self._input_name = self.session.get_inputs()[0].name
        self._output_names = [o.name for o in self.session.get_outputs()]

    def _preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, float, float]:
        """Resize and normalize image for ONNX input."""
        h, w = img.shape[:2]
        scale_x = self.input_width / w
        scale_y = self.input_height / h

        # Resize
        resized = cv2.resize(img, (self.input_width, self.input_height))

        # Normalize to [0, 1] and convert to NCHW format
        blob = resized.astype(np.float32) / 255.0
        blob = blob.transpose(2, 0, 1)  # HWC -> CHW
        blob = np.expand_dims(blob, axis=0)  # Add batch dim

        return blob, scale_x, scale_y

    def _postprocess(self, outputs, orig_h: int, orig_w: int,
                     scale_x: float, scale_y: float) -> Tuple[np.ndarray, List[TextBlock]]:
        """Convert ONNX outputs to mask and TextBlock list."""
        confidence_threshold = float(self.params['confidence_threshold']['select'])
        blk_list = []
        mask = np.zeros((orig_h, orig_w), dtype=np.uint8)

        # Try to parse outputs - ONNX object detection format
        # Common format: [batch, num_detections, 6] where 6 = [x1, y1, x2, y2, confidence, class]
        # or multiple outputs for boxes, scores, classes
        try:
            if len(outputs) == 1:
                # Single output tensor
                detections = outputs[0]
                if detections.ndim == 3:
                    detections = detections[0]  # Remove batch dim

                for det in detections:
                    if len(det) >= 5:
                        # Try format: [x1, y1, x2, y2, conf, ...]
                        conf = float(det[4])
                        if conf < confidence_threshold:
                            continue

                        x1 = int(det[0] / scale_x)
                        y1 = int(det[1] / scale_y)
                        x2 = int(det[2] / scale_x)
                        y2 = int(det[3] / scale_y)

                        # Clamp
                        x1 = max(0, min(x1, orig_w))
                        y1 = max(0, min(y1, orig_h))
                        x2 = max(0, min(x2, orig_w))
                        y2 = max(0, min(y2, orig_h))

                        if x2 <= x1 or y2 <= y1:
                            continue

                        # Create TextBlock
                        xyxy = np.array([x1, y1, x2, y2])
                        blk = TextBlock(xyxy)
                        blk_list.append(blk)

                        # Draw on mask
                        mask[y1:y2, x1:x2] = 255

            elif len(outputs) >= 3:
                # Multi-output format: boxes, scores, classes (or labels)
                boxes = outputs[0]
                scores = outputs[1]

                if boxes.ndim == 3:
                    boxes = boxes[0]
                if scores.ndim == 2:
                    scores = scores[0]
                elif scores.ndim == 1:
                    pass

                for i, score in enumerate(scores):
                    s = float(score)
                    if s < confidence_threshold:
                        continue

                    box = boxes[i]
                    x1 = int(box[0] / scale_x)
                    y1 = int(box[1] / scale_y)
                    x2 = int(box[2] / scale_x)
                    y2 = int(box[3] / scale_y)

                    x1 = max(0, min(x1, orig_w))
                    y1 = max(0, min(y1, orig_h))
                    x2 = max(0, min(x2, orig_w))
                    y2 = max(0, min(y2, orig_h))

                    if x2 <= x1 or y2 <= y1:
                        continue

                    xyxy = np.array([x1, y1, x2, y2])
                    blk = TextBlock(xyxy)
                    blk_list.append(blk)
                    mask[y1:y2, x1:x2] = 255

        except Exception as e:
            from utils.logger import logger as LOGGER
            LOGGER.error(f"ImageTrans ONNX postprocess error: {e}")

        return mask, blk_list

    def detect(self, img: np.ndarray) -> Tuple[np.ndarray, List[TextBlock]]:
        """Run detection on input image."""
        if self.session is None:
            self.setup_detector()

        orig_h, orig_w = img.shape[:2]

        # Preprocess
        blob, scale_x, scale_y = self._preprocess(img)

        # Run inference
        outputs = self.session.run(self._output_names, {self._input_name: blob})

        # Postprocess
        mask, blk_list = self._postprocess(outputs, orig_h, orig_w, scale_x, scale_y)

        return mask, blk_list

    def updateParam(self, param_key: str, param_content):
        super().updateParam(param_key, param_content)
        if param_key == 'model_name':
            new_model = self.params['model_name']['select']
            if new_model != self._current_model_name:
                self.setup_detector()
