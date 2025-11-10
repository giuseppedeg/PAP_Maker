import json
import base64
import os
from PIL import Image
from io import BytesIO

EXT = ".pap"

class Maker:
    def __init__(self):
        self.name = ""
        self.image_base64 = ""
        self.image_format = ""
        self.json_data = {}

    def save_papfile(self, image_path, json_path, output_path):
        """
        Save the file contatining the image and the COCO json annotation
        args:
          - image_path: path of the image to include in the PAP file
          - json_path: path of the COCO json annotation file to include in the PAP file
          - output_path: path where to save the PAP file
        """
        if not os.path.isdir(output_path):
            raise FileNotFoundError(f" {output_path} is not a folder.")

        with open(image_path, "rb") as img_file:
            self.image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        with open(json_path, "rb") as json_file:
            self.json_data =  base64.b64encode(json_file.read()).decode("utf-8")

        # I can load the metadata without b64 encoding. The file is a bit smaller
        # with open(json_path, "r") as json_file:
        #     self.json_data = json.load(json_file)
        
        self.name, self.image_format = os.path.splitext(os.path.basename(image_path))

        data = {"name": self.name,
                "img_format": self.image_format,
                "image": self.image_base64,
                "metadata": self.json_data,
                }

        with open(os.path.join(output_path, self.name+EXT), "w") as json_file:
            json.dump(data, json_file)


    def load_papfile(self, file_path):
        """
        Loads the file and return the image and the json metadata.
        args:
          - file_path: path of the PAP file

        Returns:
          - PIL image and 
          - COCO json annotation
          - image name
          - image format
        """
        
        data = self.load_coded_papfile(file_path)

        image, json_data, name, image_format = self.decode_papfile(data)

        return image, json_data, name, image_format
    
    
    def load_coded_papfile(self, file_path):
        """
        Loads the file and return b64 coded data.
        args:
          - file_path: path of the PAP file

        Returns:
          - PIL image and the COCO json annotation
        """
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        return data
    

    def decode_papfile(self, data):
        """
        Decodes the data and return the image and the COCO json annotation.
        args:
          - data: data of the PAP file

        Returns:
          - PIL image and 
          - COCO json annotation
          - image name
          - image format
        """
        
        self.json_data = data["metadata"]
        self.image_base64 = data["image"]
        self.name = data["name"]
        self.image_format = data["img_format"]

        image_data = base64.b64decode(self.image_base64)
        image = Image.open(BytesIO(image_data))

        json_data = base64.b64decode(self.json_data).decode("utf-8")
        json_data = json.loads(json_data)

        return image, json_data, self.name, self.image_format

    
    def extract_info(self, file_path, out_dir):
        """
        Loads the file and extracts the image and the json metadata in the out_dir folder.
        args:
          - file_path: path of the PAP file
          - out_dir: path where to save the COCO json annotation file

        """

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        image, json_data, _, _ = self.load_papfile(file_path)

        image.save(os.path.join(out_dir, self.name+self.image_format))

        with open(os.path.join(out_dir, self.name+".json"), "w") as json_file:
            json.dump(json_data, json_file, indent=4)


def create_pap(image_path, annotation_path, save_img=False, image_kb_max=1300000):
    """
    Create a PAP annotation file starting froma an image file and a COCO json annotation file
    args:
      - image_path: path of the image to include tin the PAP file
      - annotation_path: path of the COCO json annotation file
      - save_img (bool): if True, the image included in the PAP file is saved 
      - image_kb_max (int): Maximum image size in KB to include in the PAP file. If the image passed is larger, the method automatically reduces the image size to meet this constraint. 
    """
    file_h = Maker()

    out_fld = os.path.dirname(annotation_path)
    img_name = os.path.basename(image_path)

    image = Image.open(image_path)
    image = image.convert("RGB") 

    image_path = os.path.join(out_fld, f"_{img_name}")

    quality = 100
    image.save(image_path,quality=quality,optimize=True)

    file_size = os.path.getsize(image_path)

    while (file_size > image_kb_max and quality > 1):
        quality -= 5
        image.save(image_path, quality=quality, optimize=True)
        file_size = os.path.getsize(image_path)
        #print(name, file_size)
   
    file_h.save_papfile(image_path, annotation_path, out_fld)

    os.rename(os.path.join(out_fld, f"_{os.path.splitext(img_name)[0]}.pap"),
              os.path.join(out_fld, f"{os.path.splitext(img_name)[0]}.pap"), )

    if not save_img:
        os.remove(image_path)


if __name__ == "__main__":
    # This allows the file to be run directly for testing
    img_path = "data/P_Flor_2_109r.jpg"
    annotation_path = "data/annotations.json"
    create_pap(img_path, annotation_path, False)

    print("Done!")

    m = Maker()

    m.extract_info(file_path="data/test/P_Flor_2_109r.pap", 
                   out_dir="data/test/")
    
