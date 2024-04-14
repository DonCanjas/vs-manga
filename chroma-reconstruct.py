from vstools import vs, core, depth, SPath
from vssource import BestSource as BS
from vsmlrt import Waifu2x, Waifu2xModel, BackendV2
from lvsfunc import export_frames

#Join 2 single pages into a double page
#a = BS.source("left_page.jpg")
#b = BS.source("right_page.jpg")
#src = core.std.StackHorizontal([a, b]).std.SetFrameProps(_Matrix=6, _Primaries=1, _Transfer=1, _ColorRange=0, _ChromaLocation=1) 

#Batch singles
path = "H:/Set/Path"
src = BS.source(list(SPath(path).glob("*.jpg"))).std.SetFrameProps(_Matrix=6, _Primaries=1, _Transfer=1, _ColorRange=0, _ChromaLocation=1) #replace jpg with jpeg if needed
src = depth(src, 32)

#Chroma Resampling
#rgbps = rgbps = core.resize.Bicubic(src, format=vs.RGBS, filter_param_a=0.5, filter_param_b=0, matrix_in=6, transfer_in=1, primaries_in=1, range_in=1, chromaloc_in=1) #Bicubic b=.5 c=0
#rgbps = rgbps = core.resize.Bicubic(src, format=vs.RGBS, filter_param_a=1/3, filter_param_b=1/3, matrix_in=6, transfer_in=1, primaries_in=1, range_in=1, chromaloc_in=1) #Mitchell
rgbps = rgbps = core.resize.Lanczos(src, format=vs.RGBS, filter_param_a=3, matrix_in=6, transfer_in=1, primaries_in=1, range_in=1, chromaloc_in=1) #Lanczos 3

rgbps = core.std.Limiter(rgbps) #limiter

#W2x
#Differences between backends: https://github.com/AmusementClub/vs-mlrt/tree/master?tab=readme-ov-file#vs-mlrt 
#Backend list: https://github.com/AmusementClub/vs-mlrt/blob/master/scripts/vsmlrt.py#L218-L225

#w2x = Waifu2x(rgbps, noise=1, scale=1, tiles=4, overlap=[16,16], model=Waifu2xModel.cunet, backend=BackendV2.ORT_CUDA()) #faster, LQ
w2x = Waifu2x(rgbps, noise=1, scale=1, model=Waifu2xModel.cunet, backend=BackendV2.ORT_CUDA())
w2x444 = core.resize.Bicubic(w2x, format=vs.YUV444PS, matrix=6, transfer=1, primaries=1, range=1)

#Replace with original Luminance
recon = core.std.ShufflePlanes([src, w2x444], [0, 1, 2], vs.YUV)
recon = core.resize.Bicubic(recon, format=vs.RGBS, matrix_in=6, transfer_in=1, primaries_in=1, range_in=1)
out = core.fmtc.bitdepth(recon, bits=8, fulls=True, fulld=True, dmode=8, patsize=256, corplane=True)

frames = list(range(0, out.num_frames))
export_frames(out, frames=frames, filename=SPath("Chroma_Reconstruct/%03d.png"), compression=0) #Script path + output folder
                                                                                 #0 - fast compression
                                                                                 #1 - slow compression (smaller output file)
                                                                                 #2 - uncompressed                                                                         
