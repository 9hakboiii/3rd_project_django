# Font Detection
Basivally just me stitching 3 projects together:
- [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator) by `Belval`
- [DeepFont](https://github.com/robinreni96/Font_Recognition-DeepFont) by `robinreni96`
- [Text Detection](https://github.com/dodanh041001/text_detection) by `dodanh041001`

## Pre-requisites
# 텍스트 인식 데이터 생성기 설치 (학습 데이터 생성 시 필요)
Install `trdg` to generate data.

```python
pip install trdg
```

# 필수 패키지 설치
Install packages in `requirements.txt` to run font detection

```python
pip install -r requirements.txt
```

## Usage
### Data generator
```
python3 data_generator.py <font_dir> <out_dir> <image_count>
```

- `<fond_dir>`: a directory contains one sub-directory for each font with a `.ttf` file in it.
- `<image_count>`: number of image to generate for each font

### DeepFont training
Run `DeepFont_train.ipynb` in Google Colab (For HCMUT: [link](https://drive.google.com/file/d/1emw1oGeHmYYlVvoHmfBtELTya-6iINT6/view?usp=sharing))

### Font detection
- Put samples in `samples`
- Run `font_detection.py`
- Output will be in `result`
