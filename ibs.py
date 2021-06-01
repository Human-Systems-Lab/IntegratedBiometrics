from threading import Lock

import impl
import config


class API:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def read_frame():
        """
        Retrieves a frame from the webcam; Ensures compatibility with other extensions

        Returns:
            Numpy array with raw frame data: [height, width, 3]; 0 < ret[:,:,:] < 255
        """
        return impl.fmang.read_frame()

    def send_data(self, data: bytes):
        pass


class IbsCmp:
    """
    Abstract component interface
    """
    def startup_ref(self):
        raise NotImplementedError()

    def shutdown_ref(self):
        raise NotImplementedError()

    def get_widget(self):
        raise NotImplementedError()


def reg_ext(ext: IbsCmp):
    config.components.append(ext)
    return API(ext.name if hasattr(ext, "name") else config.current_name)
