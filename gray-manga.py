from vstools import vs, core, SPath
from vssource import BestSource as BS
import vsdehalo as vsdh
from vsdenoise import Prefilter
from vodesfunc.scale import mod_padding
from vsmlrt import DPIR, DPIRModel, BackendV2
from lvsfunc import export_frames

#import gray JPEG
path = "H:/Set/Path"
src = BS.source(list(SPath(path).glob("*.jpg"))).std.SetFrameProps(_Matrix=6, _Primaries=1, _Transfer=1, _ColorRange=0) #replace jpg with jpeg if needed

#dehalo
ys = core.resize.Bicubic(src, format=vs.GRAY16)
dh = vsdh.fine_dehalo.mask(clip=ys, rx=0.5, dehaloed=vsdh.dehalo_sigma(ys, pre_ss=2, sigma=3, brightstr=1, blur_func=Prefilter.GAUSSBLUR))

#pad to mod 8
(left, right, top, bottom) = mod_padding(src, mod=8, min=0)
w = src.width + left + right
h = src.height + top + bottom
pad = dh.resize.Point(w, h, format=vs.GRAYS, src_left=-left, src_top=-top, src_width=w, src_height=h)

pad = core.std.Limiter(pad)

#denoise
#Differences between backends: https://github.com/AmusementClub/vs-mlrt/tree/master?tab=readme-ov-file#vs-mlrt 
#Backend list: https://github.com/AmusementClub/vs-mlrt/blob/master/scripts/vsmlrt.py#L218-L225

tiles=1 slower, HQ
dpir = DPIR(
    pad,
    strength=3,
    model=DPIRModel.drunet_gray,
    tiles=1, tilesize=[pad.width, pad.height],
    backend=BackendV2.ORT_CUDA(fp16=True)
)

#tiles=4 faster, LQ
#dpir = DPIR(
#    pad,
#    strength=3,
#    model=DPIRModel.drunet_gray,
#    tiles=4,
#    backend=BackendV2.ORT_CUDA(fp16=True)
#)

#crop to og res
lbd = core.fmtc.bitdepth(dpir, bits=8, fulld=True, dmode=8)
out = lbd.std.Crop(left, right, top, bottom)

frames = list(range(0, out.num_frames))
export_frames(out, frames=frames, filename=SPath("DNR/%03d.png"), compression=0) #Script path + output folder
                                                                  #0 - fast compression
                                                                  #1 - slow compression (smaller output file)
                                                                  #2 - uncompressed
