"""Image preprocessing pipeline for OCR optimization.

Day 22: Prepares rendered PDF page images for Tesseract OCR by applying
conservative, resume-appropriate image transformations.

Pipeline: RGB -> grayscale -> optional upscale -> contrast enhancement -> light threshold
"""

import logging
from PIL import Image, ImageEnhance, ImageFilter

logger = logging.getLogger("talentai.resume_processing.image_preprocessing")

# Minimum dimension (width or height) below which upscaling is applied
MIN_DIMENSION_FOR_UPSCALE = 1000


def preprocess_image_for_ocr(
    image: Image.Image,
    upscale_factor: float = 2.0,
    threshold_value: int = 180,
    apply_threshold: bool = True,
) -> Image.Image:
    """Apply a conservative preprocessing pipeline to optimize OCR accuracy.

    The pipeline is designed for typical resume documents and avoids
    aggressive transformations that could destroy text.

    Args:
        image: Source PIL Image (typically rendered from a PDF page).
        upscale_factor: Multiplier for image dimensions when upscaling small images.
        threshold_value: Pixel intensity cutoff for binarization (0-255).
        apply_threshold: Whether to apply the final binarization step.

    Returns:
        Preprocessed PIL Image ready for OCR. Original image is not modified.

    Raises:
        ValueError: If image is None or has invalid dimensions.
    """
    if image is None:
        raise ValueError("Cannot preprocess a None image.")

    width, height = image.size
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid image dimensions: {width}x{height}")

    logger.debug(
        "Preprocessing image: size=%dx%d, upscale_factor=%.1f, threshold=%d",
        width, height, upscale_factor, threshold_value,
    )

    # Step 1: Ensure RGB mode (strip alpha channel if present)
    if image.mode == "RGBA":
        processed = Image.new("RGB", image.size, (255, 255, 255))
        processed.paste(image, mask=image.split()[3])
    elif image.mode != "RGB":
        processed = image.convert("RGB")
    else:
        processed = image.copy()

    # Step 2: Convert to grayscale
    processed = processed.convert("L")

    # Step 3: Upscale if the image is small (improves OCR on low-res scans)
    if upscale_factor > 1.0 and (width < MIN_DIMENSION_FOR_UPSCALE or height < MIN_DIMENSION_FOR_UPSCALE):
        new_width = int(width * upscale_factor)
        new_height = int(height * upscale_factor)
        processed = processed.resize((new_width, new_height), Image.LANCZOS)
        logger.debug("Upscaled image from %dx%d to %dx%d", width, height, new_width, new_height)

    # Step 4: Enhance contrast (moderate boost)
    enhancer = ImageEnhance.Contrast(processed)
    processed = enhancer.enhance(1.5)

    # Step 5: Light sharpening to improve character edges
    processed = processed.filter(ImageFilter.SHARPEN)

    # Step 6: Apply light threshold / binarization if enabled
    if apply_threshold and 0 < threshold_value < 255:
        processed = processed.point(lambda p: 255 if p > threshold_value else 0)
        logger.debug("Applied binarization threshold at %d", threshold_value)

    logger.debug(
        "Preprocessing complete: final_size=%dx%d, mode=%s",
        processed.size[0], processed.size[1], processed.mode,
    )

    return processed
