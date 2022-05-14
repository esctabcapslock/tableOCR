# tableOCR
- 이미지로 된 표를 csv로 변환

venv\Scripts\activate

## 대부분의 (뭔가 긴) 코드 원본
- https://github.com/eihli/image-table-ocr
- https://github.com/artperrin/image2csv
	- 뭔가 이상하게 작동하지 않음

## 내가 짠거
- [ocr.py](/ocr.py)
	- 그냥 통째로 넣으려 했지만 실패
- [app.py](/app.py)
	- 표 모양대로 자르려 했지만 실패

## 변환
1. 원본 jpg
2. pdf 변환 (웹 등으로. 예를 들면 [이](https://imagetopdf.com/)[런](https://www.adobe.com/in/acrobat/online/jpg-to-pdf.html) 곳들)
3. acrobat으로 OCR
4. pdf.js로 열기
5. 다음 스크립트 실행

```js
k=[...temp0.querySelectorAll('span')]
kk=k.filter(v=>v.innerText.trim())
d = str=>parseInt(str.replace(/px/,'')/10)
kkk = kk.map(v=>{return {l:d(v.style.left),t:d(v.style.top),v:v.innerText.trim()}})
lr = []
tr = []
kkk.forEach(v=>{
	if (!lr.includes(v.l)) lr.push(v.l);
	if (!tr.includes(v.t)) tr.push(v.t);
})
lr.sort((a,b)=>a>b)
tr.sort((a,b)=>a>b)
kkkk = new Array(tr.length).fill(0).map(v=>new Array(lr.length).fill(''))

kkk.forEach(v=>{
	kkkk[tr.indexOf(v.t)][lr.indexOf(v.l)] = v.v
})
copy(JSON.stringify(kkkk))
copy(kkkk.map(vv=>vv.map(v=>`"${v}"`).join(',')).join('\n'))
```