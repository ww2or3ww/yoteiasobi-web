const imageResize = {}
imageResize.resizeImage = (imgEL, maxSize, type = 'image/png') =>
  new Promise(resolve => {
    let w = imgEL.naturalWidth
    let h = imgEL.naturalHeight
    const canvas = document.createElement('canvas')
    if (w >= h && w > maxSize) {
      canvas.width = maxSize
      canvas.height = maxSize * h / w
    } else if (w < h && h > maxSize) {
      canvas.width = maxSize * w / h
      canvas.height = maxSize
    } else {
      canvas.width = w
      canvas.height = h
    }
    canvas.getContext('2d').drawImage(imgEL, 0, 0, canvas.width, canvas.height)
    canvas.toBlob(resolve, type)
  })
imageResize.pFileReader = blob =>
  new Promise(resolve => {
    const fr = new FileReader()
    fr.readAsDataURL(blob)
    fr.onload = e => resolve(e.target.result)
  })
imageResize.pImage = src =>
  new Promise(resolve => {
    const img = new Image()
    img.src = src
    img.onload = e => resolve(img)
  })
export default imageResize