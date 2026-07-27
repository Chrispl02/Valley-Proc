import h5py
import numpy as np

filename= "/media/cportilla/HDD/IMAGING_data/pdata/PDATA/d2009308/P2009308301.pdata"

def metadata(hdf, path):
    if path in hdf:
        dne_dataset = hdf[path]
        for attr_name, attr_value in dne_dataset.attrs.items():
            print(f"Metadata - {attr_name}: {attr_value}")

def h5_tree(val, pre=''):
    items = len(val)
    #print("items", items)
    for key, val in val.items():
        #print(key,' VAL ',val, 'ITEMS', items)
        items -= 1
        if items == 0:
            # the last item
            if type(val) == h5py._hl.group.Group:
                print(pre + '└── ' + key)
                h5_tree(val, pre+'    ')
            else:
                try:
                    print(pre + '└── ' + key + ' (%d)' % len(val))
                except TypeError:
                    print(pre + '└── ' + key + ' (scalar)')
        else:
            if type(val) == h5py._hl.group.Group:
                print(pre + '├── ' + key)
                h5_tree(val, pre+'│   ')
            else:
                try:
                    print(pre + '├── ' + key + ' (%d)' % len(val))
                except TypeError:
                    print(pre + '├── ' + key + ' (scalar)')


def load_data(filepath):
    data_vars = {}
    with h5py.File(filepath, 'r') as f:
        # Read datasets in 'Data'
        for key in f['Data']:
            item = f['Data'][key]
            if isinstance(item, h5py.Group):
                # If it's a group with one dataset inside (e.g., channel00)
                ds = list(item.keys())[0]
                try:
                    data_vars[key] = item[ds][:]
                except Exception:
                    data_vars[key] = np.full(item[ds].shape, np.nan)
            else:
                try:
                    data_vars[key] = item[:]
                except Exception:
                    data_vars[key] = np.full(item.shape, np.nan)
        
        # Read Metadata too (optional)
        for key in f['Metadata']:
            item = f['Metadata'][key]
            try:
                data_vars[key] = item[()] if np.isscalar(item[()]) else item[:]
            except Exception:
                data_vars[key] = np.nan if np.isscalar(item.shape) else np.full(item.shape, np.nan)
    
    return data_vars

def load_data_V2(filepath, data_keys):
    data_vars = {}
    with h5py.File(filepath, 'r') as f:
        data_group = f['Data']
        
        for key in data_keys:
            print("data_group", data_group)
            if key in data_group:
                item = data_group[key]
                if isinstance(item, h5py.Group):  # like data_dop/channel00
                    ds = list(item.keys())[0]
                    try:
                        data_vars[key] = item[ds][:]
                    except Exception:
                        data_vars[key] = np.full(item[ds].shape, np.nan)
                else:
                    try:
                        data_vars[key] = item[:]
                    except Exception:
                        data_vars[key] = np.full(item.shape, np.nan)
            else:
                data_vars[key] = np.nan
    
    return data_vars

def load_metadata(filepath, metadata_keys=None):
    data_vars = {}
    with h5py.File(filepath, 'r') as f:
        # Read selected Metadata
        if metadata_keys:
            meta_group = f['Metadata']
            for key in metadata_keys:
                if key not in meta_group:
                    data_vars[key] = np.nan
                    continue
                item = meta_group[key]
                try:
                    val = item[()]
                    data_vars[key] = val if np.isscalar(val) else item[:]
                except Exception:
                    data_vars[key] = np.nan if np.isscalar(item.shape) else np.full(item.shape, np.nan)

    return data_vars


if __name__ == '__main__':
    with h5py.File(filename, 'r') as hdf:
        print(hdf)
        h5_tree(hdf)
        '''dne_data = hdf['Data/Array Layout/2D Parameters/ne'][:]
        gdalt = hdf['Data/Array Layout/gdalt'][:]
        timestamps = hdf['Data/Array Layout/timestamps'][:]
        gdaltr = hdf['Data/Array Layout/1D Parameters/gdlatr'][:]
        print(dne_data)
        print(np.shape(dne_data))
        dne_metadata = hdf['Metadata/_record_layout'][:]
        print(dne_metadata)'''