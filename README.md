# 캡스톤 디자인 프로젝트
본 프로젝트는 ```PX-4```를 이용한 **Line tracer** reository 입니다.

<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/60db52d0-ffe7-474f-a1bb-bc72be51ec0d" />

---

# 라즈베리파이 모듈을 활용한 Line detection
- **원본 영상**
<img width="280" height="397" alt="image" src="https://github.com/user-attachments/assets/6b51e99b-bde4-4880-b195-c1e978223b71" />

- **전처리된 영상**
<img width="286" height="397" alt="image" src="https://github.com/user-attachments/assets/6f6ed46f-57d7-430c-91ab-7b66896bccf8" />

---

```python
def process(img):
    h, w = img.shape[:2]
    roi_vertices = [(0, 650), (2*w//3, 2*h//3), (w, 1000)]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.dilate(gray, kernel=np.ones((3,3), np.uint8))
    edges = cv2.Canny(gray, 130, 220)
    edges_roi = roi(edges, roi_vertices)
    lines = cv2.HoughLinesP(edges_roi, 1, np.pi/180, threshold=10, minLineLength=15, maxLineGap=2)
    out = draw_lines(img.copy(), lines)
    return out
```
- Grayscale function :
**lane dection**에 있어서 일반적으로 색상(RGB)정보보다는 gradient가 중요하므로 color image를 Gray image로 변경

- Dilation :
밝은 부분(차선)을 주변으로 확장시켜서 끊어진 라인과 노이즈를 보완

> Molphology Algorithm

- Canny edge detection :
영상의 경계선을 검출함. Gaussian blur를 내부적으로 적용시키고, Gradient를 계산함. thresholding argument(임계치)는 130에서 220을 유지시킴

- Roi(Resion of interest) :
지금 현재 Capstone design 프로젝트의 목적은 건물을 인식하는 것이 아닌 차선(lane)을 인식하여 tracking 하는 것임. 따라서 불필요한 배경(건물이나 가로등)은 제거하고 도로 영역만 추출함.

- Hough Transform(Probabilistic):
Edge pixel들을 공간으로 변환한 후 직선을 voting 기반으로 추출, 해당 함수에서 argument를 살펴보면 threshold는 투표기준값을 의미하며 **minlinelength**는 직선으로 인식될 최소 기준을 의미한다. 그리고 **maxLineGap**은 연결허용간격과 관련괸 argument이다.

- lineoveray:
위 알고리즘들을 기반으로 검출된 차선을 원본영상위에 올려줌.
