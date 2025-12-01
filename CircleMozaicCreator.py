import numpy as np
import cv2

class CircleMozaicCreator():
    """
    Used to transform images into a grid of circles using each regions pixel intensity

    Supplies functions to create, preview and save renders from inputted images.

    Attributes:
        squareSize (int): the width and height of each square in the grid which determine the size of the ROI used to generate circles
        savedImage (np.ndarray or None): the most recently rendered image

    Example usage:
        editor = ImageCirclenator(20)
        editor.render(image)
        editor.preview()
        editor.save("new_image.png")

    """

    def __init__(self, squareSize: int):
        self.squareSize = squareSize
        self.savedImage = None

    def render(self, inputImg: np.ndarray, **kwargs) -> np.ndarray:
        """
        Converts an image into a grid of circles

        Transforms the input image into a grid of squares with size (squareSize, squareSize)
        which is either defined by the constructor or overridden
        Inputs can be colour or grayscale and are always outputted as grayscale

        Args:
            inputImg: an array of size (x,y,3) for RGB inputs or (x,y) for B&W
            **kwargs: expect a squareSize value to temporarily override the object's current value

        Returns:
            The grayscale transformed image with the same size as the input image

        Raises:
            TypeError: inputImage is not a valid array


        Example usage:
            editor = ImageCirclenator(20)
            transformedImage = editor.render(image)
            differentImage = editor.render(image, 50)
        """
        squareSize = kwargs.get("squareSize", self.squareSize)

        self._validateSquareSize(squareSize)

        if not isinstance(inputImg, np.ndarray):
            raise TypeError("inputImg must of type np.ndarray.")

        width, height = inputImg.shape[1], inputImg.shape[0]
        newImg = np.zeros((height, width), dtype=np.uint8)      # this locks the output to grayscale and uses much less memory

        for x in range(0, width, squareSize):
            for y in range(0, height, squareSize):
                # the input isn't sanitised, and inputImg.shape % squareSize might not equal 0, so point to pixels that arnt there
                roi = inputImg[y:min(y + squareSize, height), x:min(x + squareSize, width)]

                avgIntensity = np.mean(roi)

                # the radius of the circle varies from 0-squaresize // 2, so we normalise the intensity to between these values
                maxRadius = squareSize // 2
                radius = int((avgIntensity / 255) * maxRadius)

                if radius > 0:    # a circle with r=0 still leaves a dot in opencv
                    midpointX = x + squareSize // 2
                    midpointY = y + squareSize // 2
                    cv2.circle(newImg, (midpointX, midpointY), radius, (255, 255, 255), -1)


        self.savedImage = newImg       # remember the most recent image
        return newImg

    def preview(self, inputImg: np.ndarray = None, **kwargs):
        """
        Previews the cached image or a render of the input image

        If there is a cached image present and no new image is provided, just displays the
        most recently rendered image. If there is no cached image and a new image is proved,
        render it and preview it but do not cache it.

        Args:
            inputImg (np.ndarry): an array of size (x,y,3) for RGB inputs or (x,y) for B&W
            **kwargs (int): expect a squareSize value to temporarily override the object's current value

        Example usage:
            editor = ImageCirclenator(20)
            editor.render(image)
            editor.preview()

            or

            editor = ImageCirclenator(20)
            editor.preview(image)
            editor.preview(image, 50)

        """

        squareSize = kwargs.get("squareSize", self.squareSize)

        self._validateSquareSize(squareSize)

        windowName = f"Preview, d={squareSize}"

        # if no new image is passed in, get the most recently rendered one
        if inputImg is None:
            if self.savedImage is None:
                print("Warning: No cached image to preview. Make sure to render() before attempting to preview, or pass in an image to render and preview.")
                return None
            img = self.savedImage

        # the user wants to preview a new image
        else:
            # the squareSize might've changed, either way this will pass the correct value in
            img = self.render(inputImg, squareSize=squareSize)

        cv2.imshow(windowName, img)
        cv2.waitKey(0)  # user must click to remove the window
        cv2.destroyAllWindows()

    # uses *args because a string or a string and image can be passed in - this needs to be more flexible than preview
    def save(self, *args, **kwargs):
        """
        Saves the most recetly rendered image or a new render of the input image

        If only a file name is provided, the cached image is saved using said name in the same
        directory as the python file. If a file name and image is provided, a new image is rendered
        using the image and is saved under the file name in the same directory as the python file.
        A squareSize value can be optionally be passed in to override the value used during rendering.

        Args:
            *args[0] (string):       expect name of the saved image file. must be .png, .jpg, .jpeg
            *args[1] (np.ndarry):    expect an array of size (x,y,3) for RGB inputs or (x,y) for B&W
            **kwargs[2] (np.ndarry): expect a squareSize value to temporarily override the object's current value


        Example usage:
            editor = ImageCirclenator(20)
            editor.render(image)
            editor.preview()
            editor.save("new_image.png")
        """

        # if the user just gives a file name to save to
        if len(args) == 1 and isinstance(args[0], str):
            fileName = args[0]

            # warning for superfluous arguments
            if "squareSize" in kwargs:
                print("Warning: squareSize will be ignored when saving the cached image.")

            # validate inputs
            if self.savedImage is None:
                raise ValueError("No cached image to save. Make sure to render() before attempting to save, or pass in an image to render and save.")
            if "." in fileName:
                if not fileName.endswith((".png", ".jpg", ".jpeg")):
                    invalidEnding = fileName.split(".",1)[1]
                    raise ValueError(f"Incorrect image extension (.{invalidEnding}), should be .png, .jpg, .jpeg")
            else:
                raise ValueError(f"File name must contain valid image extension (.png, .jpg, .jpeg)")

            img = self.savedImage

        # image and file name passed in
        elif len(args) >= 2:
            inputImg = args[0]
            fileName = args[1]

            squareSize = kwargs.get("squareSize", self.squareSize)
            # validate squareSize
            self._validateSquareSize(squareSize)

            img = self.render(inputImg, squareSize=squareSize)

        else:
            raise ValueError("Invalid arguments. Pass either a filename or an image and a filename.")

        cv2.imwrite(fileName, img)
        print(f"File {fileName} saved successfully")

    def _validateSquareSize(self, squareSize):
        if not isinstance(squareSize, int) or squareSize <= 0:
            raise ValueError(f"squareSize ({squareSize}) must be of type int and > 0.")

    @property
    def squareSize(self):
        return self._squareSize

    @squareSize.setter
    def squareSize(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"squareSize ({value}) must be of type int and > 0.")

        value = int(value)
        self._squareSize = value

    @property
    def savedImage(self):
        return self._savedImage

    @savedImage.setter
    def savedImage(self, value):
        self._savedImage = value

    def __repr__(self):
        if self.savedImage is not None:
            outputSize = self.savedImage.shape
        else:
            outputSize = None
        return f"{self.__class__.__name__}(squareSize={self.squareSize}, cachedImageSize={outputSize})"