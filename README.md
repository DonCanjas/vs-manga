# vs-manga
Scripts to filter (JPEG) manga using VapourSynth. Best use case would be for digital raws.  
[Preview example](https://slow.pics/c/2TDHKCNM)

## Included Scripts:
- ***gray-manga***: remove haloing and deblock/denoise grayscale images
- ***chroma-reconstruct***: reconstruct chroma using W2x
- ***dehalo-deband-recon***: remove haloing, debanding and reconstruct chroma

## Dependencies:
- Python
- [VapourSynth](https://github.com/vapoursynth/vapoursynth) R65+
- [HAvsFunc](https://github.com/HomeOfVapourSynthEvolution/havsfunc) and its dependencies
- [vsjet's git latest](https://github.com/Jaded-Encoding-Thaumaturgy/vs-jet?tab=readme-ov-file#vs-jet): [vs-tools](https://github.com/Jaded-Encoding-Thaumaturgy/vs-tools) [vs-dehalo](), [vssource](), [lvsfunc](https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc) and [vs-denoise](https://github.com/Jaded-Encoding-Thaumaturgy/vs-denoise)
- [vodesfunc](https://github.com/Vodes/vodesfunc/tree/master?tab=readme-ov-file#installation) git latest
- [fpng](https://github.com/Mikewando/vsfpng) (can install with vsrepo)
- [vsmlrt](https://github.com/AmusementClub/vs-mlrt) (can install with vsrepo)
- [BestSource](https://github.com/vapoursynth/bestsource/releases)

## Usage:
Open the script, edit the input and output paths (default output path is `script's path+output folder`) and other settings you might want/need to change.  Run the scipt and hope it works.

## TODO
- CLI front-end
- List all pip dependencies in a requirements.txt file
- Support for more image file formats
