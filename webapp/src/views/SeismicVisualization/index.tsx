import { useEffect, useRef } from 'react'
import { Container } from "./styles"

interface SeismicVisualizationProps {
  fileKey: string
}

export default function SeismicVisualization({ fileKey }: SeismicVisualizationProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const SUFileAsBase64String = "thats not a base 64 string but should be"

  // this file will be avaliable globaly inside the iframe 
  const declareSUFileToIframe = (event: any) => {
    const newScriptTag = document.createElement('script');
    const SUFileDeclarationScript = document.createTextNode(`var SUFileAsBase64String = "${SUFileAsBase64String}"`);
    newScriptTag.appendChild(SUFileDeclarationScript)
    event.target.contentWindow.document.querySelector("body").prepend(newScriptTag)
  }

  return (
    <Container>
      <h1>Key: {fileKey}</h1>
      <iframe
        ref={iframeRef}
        name="frame-id"
        src="http://127.0.0.1:5173/src/pyscript/index.html"
        onLoad={declareSUFileToIframe}
      >
      </iframe>
    </Container>
  )
}
