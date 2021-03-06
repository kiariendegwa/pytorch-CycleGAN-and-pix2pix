import numpy as np
import os
import ntpath
import time
from . import util
from . import html
from pdb import set_trace as st

class Visualizer():
    def __init__(self, opt):
        # self.opt = opt
        self.display_id = opt.display_id
        if self.display_id > 0:
            from . import display
            self.display = display
        else:
            from . import html
            self.web_dir = os.path.join(opt.checkpoints_dir, opt.name, 'web')
            self.img_dir = os.path.join(self.web_dir, 'images')
            self.name = opt.name
            self.win_size = opt.display_winsize
            print('create web directory %s...' % self.web_dir)
            util.mkdirs([self.web_dir, self.img_dir])


    # |visuals|: dictionary of images to display or save
    def display_current_results(self, visuals, epoch):
        if self.display_id > 0: # show images in the browser
            idx = 0
            for label, image_numpy in visuals.items():
                image_numpy = np.flipud(image_numpy)
                self.display.image(image_numpy, title=label,
                                   win=self.display_id + idx)
                idx += 1
        else:  # save images to a web directory
            for label, image_numpy in visuals.items():
                img_path = os.path.join(self.img_dir, 'epoch%.3d_%s.png' % (epoch, label))
                util.save_image(image_numpy, img_path)
            # update website
            webpage = html.HTML(self.web_dir, 'Experiment name = %s' % self.name, reflesh=1)
            for n in range(epoch, 0, -1):
                webpage.add_header('epoch [%d]' % n)
                ims = []
                txts = []
                links = []

                for label, image_numpy in visuals.items():
                    img_path = 'epoch%.3d_%s.png' % (n, label)
                    ims.append(img_path)
                    txts.append(label)
                    links.append(img_path)
                webpage.add_images(ims, txts, links, width=self.win_size)
            webpage.save()
            # st()
    # errors: dictionary of error labels and values
    def plot_current_errors(self, epoch, i, opt, errors):
        pass

    # errors: same format as |errors| of plotCurrentErrors
    def print_current_errors(self, epoch, i, errors, start_time):
        message = '(epoch: %d, iters: %d, time: %.3f) ' % (epoch, i, time.time() - start_time)
        for k, v in errors.items():
            message += '%s: %.3f ' % (k, v)

        print(message)

    # save image to the disk
    def save_images(self, webpage, visuals, image_path):
        image_dir = webpage.get_image_dir()
        short_path = ntpath.basename(image_path[0])
        name = os.path.splitext(short_path)[0]

        webpage.add_header(name)
        ims = []
        txts = []
        links = []

        for label, image_numpy in visuals.items():
            image_name = '%s_%s.png' % (name, label)
            save_path = os.path.join(image_dir, image_name)
            util.save_image(image_numpy, save_path)

            ims.append(image_name)
            txts.append(label)
            links.append(image_name)
        webpage.add_images(ims, txts, links, width=self.win_size)
