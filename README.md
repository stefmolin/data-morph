<div align="center">
  <img alt="Data Morph" src="https://github.com/stefmolin/data-morph/raw/main/docs/_static/logo.png">

  <hr>

  <table>
   <tr>
     <td>
      <img alt="Last Release" src="https://img.shields.io/badge/last%20release-inactive?style=for-the-badge">
     </td>
     <td>
      <a href="https://stefaniemolin.com/data-morph" target="_blank" rel="noopener noreferrer">
        <img alt="View docs" src="https://img.shields.io/badge/docs-stable-success">
      </a>
      <a href="https://pypi.org/project/data-morph-ai/" target="_blank" rel="noopener noreferrer">
        <img alt="PyPI release" src="https://img.shields.io/pypi/v/data-morph-ai.svg">
      </a>
      <a href="https://anaconda.org/conda-forge/data-morph-ai" target="_blank" rel="noopener noreferrer">
        <img alt="conda-forge release" src="https://img.shields.io/conda/vn/conda-forge/data-morph-ai.svg">
      </a>
      <a href="https://pypi.org/project/data-morph-ai/" target="_blank" rel="noopener noreferrer">
        <img alt="Supported Python Versions" src="https://img.shields.io/pypi/pyversions/data-morph-ai">
      </a>
      <a href="https://github.com/stefmolin/data-morph/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">
         <img alt="License" src="https://img.shields.io/pypi/l/data-morph-ai.svg?color=blueviolet">
      </a>
     </td>
   </tr>
   <tr>
     <td>
       <img alt="Citation information" src="https://img.shields.io/badge/for%20citation-inactive?style=for-the-badge">
   </td>
     <td>
      <a href="https://doi.org/10.5281/zenodo.8374121"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.8374121.svg" alt="DOI"></a>
     </td>
   </tr>
   <tr>
     <td>
      <img alt="Build status" src="https://img.shields.io/badge/build%20status-inactive?style=for-the-badge">
     </td>
     <td>
      <a href="https://codecov.io/gh/stefmolin/data-morph" target="_blank" rel="noopener noreferrer">
        <img alt="codecov" src="https://codecov.io/gh/stefmolin/data-morph/branch/main/graph/badge.svg?token=3SEEG9SZQO">
      </a>
      <a href="https://github.com/stefmolin/data-morph/actions/workflows/ci.yml" target="_blank" rel="noopener noreferrer">
        <img alt="CI" src="https://github.com/stefmolin/data-morph/actions/workflows/ci.yml/badge.svg">
      </a>
      <a href="https://github.com/stefmolin/data-morph/actions/workflows/docs.yml" target="_blank" rel="noopener noreferrer">
        <img alt="Deploy Docs" src="https://github.com/stefmolin/data-morph/actions/workflows/docs.yml/badge.svg">
      </a>
     </td>
   </tr>
   <tr>
     <td>
      <img alt="Downloads" src="https://img.shields.io/badge/%23%20downloads-inactive?style=for-the-badge">
     </td>
     <td>
      <a href="https://pypi.org/project/data-morph-ai/" target="_blank" rel="noopener noreferrer">
        <img alt="PyPI downloads" src="https://img.shields.io/pepy/dt/data-morph-ai?label=pypi&color=blueviolet">
      </a>
      <a href="https://anaconda.org/conda-forge/data-morph-ai" target="_blank" rel="noopener noreferrer">
        <img alt="conda-forge downloads" src="https://img.shields.io/conda/dn/conda-forge/data-morph-ai.svg?label=conda-forge&color=blueviolet">
      </a>
     </td>
   </tr>
  </table>
  <hr/>
</div>

Data Morph transforms an input dataset of 2D points into select shapes, while preserving the summary statistics to a given number of decimal points through simulated annealing. It is intended to be used as a teaching tool to illustrate the importance of data visualization (see the [Data Morph in the Classroom](https://stefaniemolin.com/data-morph/stable/index.html#classroom-ideas) section for ideas).

<div align="center">
  <img alt="Morphing the panda dataset into the star shape." src="https://raw.githubusercontent.com/stefmolin/data-morph/main/docs/_static/panda-to-star-eased.gif">
  <br/>
</div>

## Installation

Data Morph can be installed from PyPI using `pip`:

```console
$ python -m pip install data-morph-ai
```

Alternatively, Data Morph can be installed with `conda` by specifying the `conda-forge` channel:

```console
$ conda install -c conda-forge data-morph-ai
```

## Usage

Once installed, Data Morph can be used on the command line or as an importable Python package. Below are some examples; be sure to check out the [documentation](https://stefaniemolin.com/data-morph) for more information.


### Command Line Usage

Run `data-morph` on the command line:

```console
$ data-morph --start-shape panda --target-shape star
```

This produces the animation in the newly-created `morphed_data` directory within your current working directory (shown above). More examples, including how to run multiple transformations in parallel, can be found in the [documentation](https://stefaniemolin.com/data-morph/).

----

See all available CLI options by passing in `--help` or consulting the [CLI reference](https://stefaniemolin.com/data-morph/stable/cli.html) in the documentation:

```console
$ data-morph --help
```

### Python Usage

The `DataMorpher` class performs the morphing from a `Dataset` to a `Shape`. Any `pandas.DataFrame` with numeric columns `x` and `y` can be a `Dataset`. Use the `DataLoader` to create the `Dataset` from a file or use a built-in dataset:

```python
from data_morph.data.loader import DataLoader

dataset = DataLoader.load_dataset('panda')
```

For morphing purposes, all target shapes are placed/sized based on aspects of the `Dataset` class.
All shapes are accessible via the `ShapeFactory` class:

```python
from data_morph.shapes.factory import ShapeFactory

shape_factory = ShapeFactory(dataset)
target_shape = shape_factory.generate_shape('star')
```

With the `Dataset` and `Shape` created, here is a minimal example of morphing:

```python
from data_morph.morpher import DataMorpher

morpher = DataMorpher(
    decimals=2,
    in_notebook=False,  # whether you are running in a Jupyter Notebook
    output_dir='data_morph/output',
)

result = morpher.morph(start_shape=dataset, target_shape=target_shape)
```

Note that the `result` variable in the above code block is a `pandas.DataFrame` of the data after completing the specified iterations of the simulated annealing process. The `DataMorpher.morph()` method is also saving plots to visualize the output periodically and make an animation; these end up in `data_morph/output`, which we set as `DataMorpher.output_dir`.


----

In this example, we morphed the built-in panda `Dataset` into the star `Shape`. Be sure to try out the other built-in options:

* The `DataLoader.AVAILABLE_DATASETS` attribute contains a list of available datasets, which are also visualized in the `DataLoader` documentation [here](https://stefaniemolin.com/data-morph/stable/api/data_morph.data.loader.html#data_morph.data.loader.DataLoader).

* The `ShapeFactory.AVAILABLE_SHAPES` attribute contains a list of available shapes, which are also visualized in the `ShapeFactory` documentation [here](https://stefaniemolin.com/data-morph/stable/api/data_morph.shapes.factory.html#data_morph.shapes.factory.ShapeFactory).

## Data Morph in the Classroom

Data Morph is intended to be used as a teaching tool to illustrate the importance of data visualization. Here are some potential classroom activities for instructors:

- **Statistics Focus**: Have students pick one of the [built-in datasets](https://stefaniemolin.com/data-morph/stable/api/data_morph.data.loader.html#data_morph.data.loader.DataLoader), and morph it into all available [target shapes](https://stefaniemolin.com/data-morph/stable/api/data_morph.shapes.factory.html#data_morph.shapes.factory.ShapeFactory). Ask students to comment on which transformations worked best and why.
- **Creativity Focus**: Have students [create a new dataset](https://stefaniemolin.com/data-morph/stable/tutorials/custom-datasets.html) (*e.g.*, your school logo or something that the student designs), and morph that into multiple [target shapes](https://stefaniemolin.com/data-morph/stable/api/data_morph.shapes.factory.html#data_morph.shapes.factory.ShapeFactory). Ask students to comment on which transformations worked best and why.
- **Math and Coding Focus**: Have students [create a custom shape](https://stefaniemolin.com/data-morph/stable/tutorials/shape-creation.html) by inheriting from `LineCollection` or `PointCollection`, and try morphing a couple of the [built-in datasets](https://stefaniemolin.com/data-morph/stable/api/data_morph.data.loader.html#data_morph.data.loader.DataLoader) into that shape. Ask students to explain how they chose to calculate the shape, and comment on which transformations worked best and why.

If you end up using Data Morph in your classroom, I would love to hear about it. Please [send me a message](https://stefaniemolin.com/contact/) detailing how you used it and how it went.

## Acknowledgements

This code has been altered by Stefanie Molin ([@stefmolin](https://github.com/stefmolin)) to work for other input datasets by parameterizing the target shapes with information from the input shape. The original code works for a specific dataset called the "Datasaurus" and was created for the paper *Same Stats, Different Graphs: Generating Datasets with Varied Appearance and Identical Statistics through Simulated Annealing* by Justin Matejka and George Fitzmaurice (ACM CHI 2017).

The paper and video can be found on the Autodesk Research website [here](https://www.research.autodesk.com/publications/same-stats-different-graphs-generating-datasets-with-varied-appearance-and-identical-statistics-through-simulated-annealing/). The version of the code placed on GitHub at [jmatejka/same-stats-different-graphs](https://github.com/jmatejka/same-stats-different-graphs), served as the starting point for the Data Morph codebase, which is on GitHub at [stefmolin/data-morph](https://github.com/stefmolin/data-morph).

Read more about the creation of Data Morph [here](https://stefaniemolin.com/articles/data-science/introducing-data-morph/) and [here](https://stefaniemolin.com/data-morph-talk/#/).

## Citations

If you use this software, please cite both Data Morph (DOI: [10.5281/zenodo.7834197](https://doi.org/10.5281/zenodo.7834197)) and *[Same Stats, Different Graphs: Generating Datasets with Varied Appearance and Identical Statistics through Simulated Annealing](https://damassets.autodesk.net/content/dam/autodesk/research/publications-assets/pdf/same-stats-different-graphs.pdf)* by Justin Matejka and George Fitzmaurice (ACM CHI 2017).

## Contributing
Please consult the [contributing guidelines](CONTRIBUTING.md).
