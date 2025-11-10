# PAP file maker

This Python package allows you to create and manage annotation files in PAP format that can be used with the [GlyFix](https://glyfix.scicore.unibas.ch/corrector.html?toml=pyscript.toml&project_file=new)  annotation editing tool specifically designed to annotate images of handwritten text at the character level.



## Installation
```
pip install git+https://github.com/giuseppedeg/PAP_Maker.git
```
__NOTE__: Make sure you have git installed on your machine!

## Usage

This package provides methods and classes to manipulate a PAP file

### Create a PAP file
We can easily create a PAP file having an image and the annotation in COCO json format

```ptython
from pap_maker.pap import create_pap

create_pap(image_path="PATH_TO_IMAGE_FILE",
           annotation_path="PATH_TO_JSON_FILE")
```

### Manipulate a PAP file
The packege contains the class `Maker` that we can use to manipulate a PAP file.

For example, we can extract the image and the COCO json annotation from a PAP file:
 
```ptython
from pap_maker.pap import Maker

m = Maker()

m.extract_info(file_path="PATH_OF_PAP_FILE", 
               out_dir="PATH_WHERE_TO_SAVE_DATA")
```