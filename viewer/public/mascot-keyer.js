/**
 * Keying the mascot's backdrop out, on the GPU.
 *
 * The renders are on black and near black, and `mix-blend-mode: screen` would
 * drop the character's own dark edges along with the background. This samples
 * the frame's four corners, removes that colour and un-mixes the edge pixels,
 * so the figure keeps its real colours over whatever is behind it.
 *
 * **Lifted out of `mascot.js` so the dock and the page figures share it.**
 * There are now three places drawing the same two clips -- the corner dock, the
 * landing hero and the home page -- and a second copy of a chroma key is how
 * they come to look subtly different from each other on the one machine whose
 * driver rounds differently. Nothing here knows what a mascot is: it takes a
 * canvas, hands back a draw function, and returns null where there is no
 * WebGL, which is the caller's cue to keep showing the still.
 */

const KEY_FS = 'precision mediump float;varying vec2 v;uniform sampler2D t;uniform vec2 c0,c1;'
  + 'void main(){vec2 uv=vec2(mix(c0.x,c1.x,v.x),mix(c0.y,c1.y,v.y));vec3 c=texture2D(t,uv).rgb;'
  + 'vec3 bg=(texture2D(t,vec2(c0.x+.01,.02)).rgb+texture2D(t,vec2(c1.x-.01,.02)).rgb'
  + '+texture2D(t,vec2(c0.x+.01,.98)).rgb+texture2D(t,vec2(c1.x-.01,.98)).rgb)*.25;'
  + 'float a=smoothstep(.035,.12,distance(c,bg));'
  + 'vec3 col=a>.002?clamp(bg+(c-bg)/a,0.,1.):vec3(0.);gl_FragColor=vec4(col*a,a);}';

export function makeKeyer(canvas) {
  const gl = canvas.getContext('webgl', { premultipliedAlpha: true, alpha: true });
  if (!gl) return null;
  const sh = (type, src) => {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    return s;
  };
  const p = gl.createProgram();
  gl.attachShader(p, sh(gl.VERTEX_SHADER,
    'attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0,1);}'));
  gl.attachShader(p, sh(gl.FRAGMENT_SHADER, KEY_FS));
  gl.linkProgram(p);
  gl.useProgram(p);
  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(p, 'p');
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const tex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, tex);
  for (const k of [gl.TEXTURE_WRAP_S, gl.TEXTURE_WRAP_T]) gl.texParameteri(gl.TEXTURE_2D, k, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  const u0 = gl.getUniformLocation(p, 'c0');
  const u1 = gl.getUniformLocation(p, 'c1');

  return (video) => {
    if (video.readyState < 2 || !video.videoWidth) return;
    const dpr = window.devicePixelRatio || 1;
    const pw = Math.round(canvas.clientWidth * dpr);
    const ph = Math.round(canvas.clientHeight * dpr);
    if (canvas.width !== pw || canvas.height !== ph) { canvas.width = pw; canvas.height = ph; }
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, video);
    // Crop rather than stretch, so the character keeps his proportions whatever
    // shape the dock is.
    const ca = (canvas.width || 1) / (canvas.height || 1);
    const va = video.videoWidth / video.videoHeight;
    const fx = ca < va ? ca / va : 1;
    const fy = ca < va ? 1 : va / ca;
    const x0 = (1 - fx) / 2;
    const y0 = (1 - fy) / 2;
    gl.uniform2f(u0, x0, y0);
    gl.uniform2f(u1, 1 - x0, 1 - y0);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  };
}
