#===============================================================================
#=================== PyTHENA: Python class for Athena F95 ======================
#===============================================================================
# Author: Marc B.R. Joos
#
# Created/last modified: jun 26, 2013/jul 10, 2013
#
# This file is distributed under GNU/GPL licence, 
# see <http://www.gnu.org/licenses/>.
#===============================================================================
import glob
import numpy as np

class datAthena:
    """This is Athena data class

    Usage:
        data = datAthena(fname, dtype)
    With:
        - fname: name of the binary file to read
        - dtype: type of the data to read ['f4']"""
    def __init__(self, fname, dtype='f4'):
        f = open(fname)
        ndata = getArray(f, 4, 'i4')
        eos   = getArray(f, 2, dtype)
        nx, ny, nz = ndata[0:3]
        nvar  = ndata[3]
        gamma = eos[0] + 1
        isoc  = eos[1]
        self.nx, self.ny, self.nz, self.nvar = ndata
        self.gamma = gamma; self.isoc = isoc

        x = getArray(f, nx, dtype)
        y = getArray(f, ny, dtype)
        z = getArray(f, nz, dtype)
        self.x, self.y, self.z = x, y, z
        
        u = np.zeros((nx,ny,nz,nvar))
        w = np.zeros((nx,ny,nz,nvar))
        
        var = getArray(f, nx*ny*nz, dtype)
        var = np.reshape(var, (nx,ny,nz))
        u[:,:,:,0] = var
        w[:,:,:,0] = var
        var = getArray(f, nx*ny*nz*3, dtype)
        var = np.reshape(var, (nx,ny,nz,3))
        u[:,:,:,1:4] = var
        if nvar == 4:
            var = getArray(f, nx*ny*nz*3, dtype)
            var = np.reshape(var, (nx,ny,nz,3))
            w[:,:,:,1:nvar] = var
        elif nvar == 5:
            var = getArray(f, nx*ny*nz*5, dtype)
            var = np.reshape(var, (nx,ny,nz,5))
            u[:,:,:,4] = var[:,:,:,0]
            w[:,:,:,1:nvar] = var[:,:,:,1:]
        elif nvar == 7:
            var = getArray(f, nx*ny*nz*3, dtype)
            var = np.reshape(var, (nx,ny,nz,3))
            u[:,:,:,4:nvar] = var
            w[:,:,:,4:nvar] = var
            var = getArray(f, nx*ny*nz*3, dtype)
            var = np.reshape(var, (nx,ny,nz,3))
            w[:,:,:,1:4] = var
        elif nvar == 8:
            var = getArray(f, nx*ny*nz, dtype)
            var = np.reshape(var, (nx,ny,nz))
            u[:,:,:,4] = var
            var = getArray(f, nx*ny*nz*3, dtype)
            var = np.reshape(var, (nx,ny,nz,3))
            u[:,:,:,5:nvar] = var
            w[:,:,:,5:nvar] = var
            var = getArray(f, nx*ny*nz*4, dtype)
            var = np.reshape(var, (nx,ny,nz,4))
            w[:,:,:,1:5] = var
        f.close()
        self.u = u; self.w = w

def getArray(fid, nbCount, dtype):
    bitsType = 'i4'
    pad      = np.fromfile(fid, count=1, dtype=bitsType)
    array    = np.fromfile(fid, count=nbCount, dtype=dtype)
    pad      = np.fromfile(fid, count=1, dtype=bitsType)
    return array

def getFiles(dirpath='./', problemId='KH', ext='bin'):
    lfiles = np.sort(glob.glob(dirpath + problemId + '*' + ext))
    nfiles = lfiles.size
    ff = int(lfiles[0][len(dirpath + problemId + '.'):-len('.' + ext)])
    lf = int(lfiles[-1][len(dirpath + problemId + '.'):-len('.' + ext)])
    ifiles = np.linspace(ff, lf, nfiles)
    ifiles = ifiles.astype('i4')
    return (lfiles, nfiles, ifiles)

def loadFiles(dirpath='./', problemId='KH', ext='bin', fe=None, le=None \
                  , jump=None, dtype='f4'):
    """Load a bunch of Athena data files

    Usage:
        data = loadFiles(dirpath, problemId, ext, fe, le, jump, dtype)
    with: 
        - dirpath:   path of the directory containing the files ['./']
        - problemId: name of the Athena problem ['AW']
        - ext:       extension of the data files ['bin']
        - fe:        index of the first file to read [None]
        - le:        index of the last file to read [None]
        - jump:      stride between the file indices to read [None]
        - dtype:     type of the data ['f4']"""
    lfiles, nfiles, ifiles = getFiles(dirpath, problemId, ext)
    if not(fe):
        fe = ifiles[0]
    if not(le):
        le = ifiles[-1]
    data = []
    lifiles = ifiles.tolist()
    for i in ifiles[lifiles.index(fe):lifiles.index(le)+1:jump]:
        fname = lfiles[i]
        data.append(datAthena(fname, dtype))
    return data
