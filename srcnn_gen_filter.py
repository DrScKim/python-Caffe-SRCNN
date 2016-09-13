
import sys, os, argparse, time

import numpy as np
import scipy.io

def get_args():
    parser = argparse.ArgumentParser('Extract CNN weights')

    parser.add_argument('-caffemodel', dest='modelFile', type=str, required=True,
                        help='Caffe model weights file to parse')
    parser.add_argument('-mat', dest='matFile', type=str, required=True,
                        help='Network prototxt file associated with model')

    return parser.parse_args()


if __name__ == "__main__":
    import caffe

    args = get_args()
    print args.matFile
    print args.modelFile

    net = caffe.Net(args.matFile, args.modelFile, caffe.TEST)
    d = {}

    for name, blobs in net.params.iteritems():
        print "\nname: ", name

        for ii in range(len(blobs)):
            #
            blob = blobs[ii]
            if ii == 0:
                name2 = "weights_"+name
                channels = blob.channels
                size = blob.height*blob.height
                num = blob.num
                if blob.channels == 1:
                    weights = np.ndarray(shape=(size, num), dtype=np.double)
                else:
                    weights = np.ndarray(shape=(channels, size, num), dtype=np.double)



                for i in range(channels):
                    for j in range(num):
                        print weights.shape
                        print blob.data.shape
                        tmp = blob.data[j,i, :,:]

                        if channels == 1:
                            weights[:,j] = np.ravel(tmp.T)
                        else:
                            weights[i,:,j] = np.ravel(tmp.T)
                        d[name2] = weights
                        # print tmp

            elif ii == 1:
                name2 = "biases_" + name
                d[name2] = np.double(np.reshape(np.ravel(blob.data), (num, 1)))









    # for name, blobs in net.params.iteritems():
    #     for ii in range(len(blobs)):
    #         # Assume here index 0 are the weights and 1 is the bias.
    #         # This seems to be the case in Caffe.
    #         if ii == 0:
    #             name2 = "weight_"+name
    #         elif ii == 1:
    #             name2 = "bias_" + name
    #         else:
    #             pass  # This is not expected
    #
    #         print("%s : %s" % (name2, blobs[ii].data.shape))
    #         d[name2] = blobs[ii].data
    #
    scipy.io.savemat('filter' + ".mat", d)