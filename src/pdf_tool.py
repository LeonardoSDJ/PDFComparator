import os
import numpy as np
import cv2
import fitz
import logging
from typing import List, Dict, Any
from difflib import SequenceMatcher
from functools import lru_cache
from PIL import Image

try:
    from pillow_simd import Image as SIMDImage
except ImportError:
    SIMDImage = Image

class PDFComparisonTool:
    def __init__(self):
        self.pdf1_images: List[np.ndarray] = []
        self.pdf2_images: List[np.ndarray] = []
        self.diff_images: List[Dict[str, Any]] = []
        self.threshold: int = 30
        self.color_intensity: float = 0.3
        self.cache: Dict[str, Any] = {}

    @lru_cache(maxsize=32)
    def convert_pdf_to_images(self, pdf_path: str, zoom_x: float = 2.0, zoom_y: float = 2.0) -> List[np.ndarray]:
        images = []
        pdf_document = fitz.open(pdf_path)
        for page in pdf_document:
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom_x, zoom_y))
            img = SIMDImage.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(np.array(img))
        pdf_document.close()
        return images

    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
        return enhanced

    def update_comparison_params(self, threshold: int, color_intensity: float) -> None:
        self.threshold = threshold
        self.color_intensity = color_intensity
        self.recompute_diff_images()

    def recompute_diff_images(self) -> None:
        self.diff_images = [
            {
                'image': self.compare_images(img1, img2),
                'page_number': i + 1,
                'is_extra_page': i >= min(len(self.pdf1_images), len(self.pdf2_images))
            }
            for i, (img1, img2) in enumerate(zip(self.pdf1_images, self.pdf2_images))
        ]

    def compare_images(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        height = max(img1.shape[0], img2.shape[0])
        width = max(img1.shape[1], img2.shape[1])
        
        img1_resized = cv2.resize(img1, (width, height))
        img2_resized = cv2.resize(img2, (width, height))

        gray1 = cv2.cvtColor(img1_resized, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_RGB2GRAY)

        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)

        result = np.zeros_like(img1_resized)
        result[thresh == 0] = [0, 255, 0]
        result[thresh != 0] = [0, 0, 255]

        alpha = 1 - self.color_intensity
        result = cv2.addWeighted(img1_resized, alpha, result, 1 - alpha, 0)

        return result

    def process_pdfs(self, pdf1_path: str, pdf2_path: str, progress_callback: callable = None, mismatch_callback: callable = None) -> None:
        self.pdf1_images = list(map(self.enhance_image, self.convert_pdf_to_images(pdf1_path)))
        self.pdf2_images = list(map(self.enhance_image, self.convert_pdf_to_images(pdf2_path)))

        min_pages = min(len(self.pdf1_images), len(self.pdf2_images))
        total_pages = max(len(self.pdf1_images), len(self.pdf2_images))

        if len(self.pdf1_images) != len(self.pdf2_images):
            logging.warning(f"Os PDFs têm números diferentes de páginas. PDF1: {len(self.pdf1_images)}, PDF2: {len(self.pdf2_images)}")
            if mismatch_callback:
                mismatch_callback(len(self.pdf1_images), len(self.pdf2_images))

        self.recompute_diff_images()

        if progress_callback:
            for i in range(total_pages):
                progress_callback((i + 1) / total_pages * 100)

    def get_diff_image(self, page_num: int) -> Dict[str, Any]:
        if 0 <= page_num < len(self.diff_images):
            return self.diff_images[page_num]
        else:
            return None

    def save_diff_images(self, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        for i, diff_data in enumerate(self.diff_images):
            output_path = os.path.join(output_dir, f"diff_page_{i+1}.png")
            diff_image = diff_data['image']
            diff_image_bgr = cv2.cvtColor(diff_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, diff_image_bgr)

    def extract_text_and_metadata(self, pdf_path: str) -> Dict[str, Any]:
        pdf_document = fitz.open(pdf_path)
        text = ""
        metadata = pdf_document.metadata
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        pdf_document.close()
        return {"text": text, "metadata": metadata}

    def compare_text(self, text1: str, text2: str) -> float:
        return SequenceMatcher(None, text1, text2).ratio()

    def compare_metadata(self, metadata1: Dict[str, Any], metadata2: Dict[str, Any]) -> Dict[str, Any]:
        diff = {}
        all_keys = set(metadata1.keys()) | set(metadata2.keys())
        for key in all_keys:
            if metadata1.get(key) != metadata2.get(key):
                diff[key] = (metadata1.get(key), metadata2.get(key))
        return diff

    def generate_comparison_report(self, pdf1_path: str, pdf2_path: str) -> str:
        pdf1_info = self.extract_text_and_metadata(pdf1_path)
        pdf2_info = self.extract_text_and_metadata(pdf2_path)

        text_similarity = self.compare_text(pdf1_info['text'], pdf2_info['text'])
        metadata_diff = self.compare_metadata(pdf1_info['metadata'], pdf2_info['metadata'])

        total_pages = len(self.diff_images)
        pages_with_differences = sum(1 for img in self.diff_images if np.any(img['image'][:, :, 2] == 255))
        
        report = (
            f"PDF Comparison Report\n"
            f"{'=' * 30}\n\n"
            f"Resumo:\n"
            f"- Similaridade de texto: {text_similarity:.2%}\n"
            f"- Diferenças em metadados: {len(metadata_diff)} campos\n"
            f"- Total de páginas comparadas: {total_pages}\n"
            f"- Páginas com diferenças detectadas: {pages_with_differences}\n\n"
        )

        report += f"Diferenças nos Metadados:\n"
        if metadata_diff:
            for key, (value1, value2) in metadata_diff.items():
                value1 = value1 or "Não disponível"
                value2 = value2 or "Não disponível"
                report += f"  {key}:\n    PDF1: {value1}\n    PDF2: {value2}\n"
        else:
            report += "  Não foram encontradas diferenças significativas nos metadados.\n"

        report += f"\nDiferenças nas Imagens:\n"
        report += f"  Total de páginas comparadas: {total_pages}\n"
        report += f"  Páginas com diferenças: {pages_with_differences}\n"
        if pages_with_differences > 0:
            paginas_com_diferencas = [i+1 for i, img in enumerate(self.diff_images) if np.any(img['image'][:, :, 2] == 255)]
            report += f"  Páginas afetadas: {', '.join(map(str, paginas_com_diferencas))}\n"
            report += f"  Imagens de diferenças salvas em: /caminho/para/imagens\n"
        else:
            report += "  Não foram encontradas diferenças visuais entre as páginas.\n"

        interpretacao = (
            f"\nInterpretação dos Resultados:\n"
            f"A similaridade do texto entre os PDFs é {text_similarity:.2%}, o que sugere que os documentos são "
            f"{'muito semelhantes' if text_similarity > 0.80 else 'bastante diferentes'}.\n"
        )
        if metadata_diff:
            interpretacao += (
                "Diferenças significativas nos metadados foram detectadas. Isso pode indicar que os arquivos foram "
                "gerados por ferramentas ou processos diferentes, ou que eles foram alterados em momentos distintos.\n"
            )
        if pages_with_differences > 0:
            interpretacao += (
                f"As diferenças visuais encontradas em {pages_with_differences} página(s) indicam alterações no layout ou "
                "nos elementos gráficos, o que pode impactar a apresentação visual dos documentos.\n"
            )
        else:
            interpretacao += "Não foram encontradas diferenças visuais, sugerindo que os documentos são visualmente idênticos.\n"

        report += interpretacao
        return report