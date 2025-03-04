# vcf2pandas

![PyPI Downloads](https://static.pepy.tech/badge/vcf2pandas/month)
![PyPI Downloads](https://static.pepy.tech/badge/vcf2pandas)

`vcf2pandas` is a python package to convert vcf files to `pandas` dataframes.

## Install

```bash
pip install vcf2pandas
```

## Dependencies

- pandas (2.1.0)
- pysam (0.22.1)

## Usage

### Selecting all columns (default behaviour)

```python
from vcf2pandas import vcf2pandas
import pandas

df = vcf2pandas("path_to_vcf.vcf")
```

### Remove all empty columns

Sometimes where will be `INFO` or `FORMAT` fields from the header where none of the variants or samples have that field. You can choose to remove all of these from the pandas dataframe.

```python
df = vcf2pandas("path_to_vcf.vcf", remove_empty_columns=True)
```

### Selecting custom columns and samples

```python
info_fields = ["info_field_1", "info_field_2"]
sample_list = ["sample_name_1", "sample_name_2"]
format_fields = ["format_name_1", "format_name_2"]

df_selected = vcf2pandas(
    "path_to_vcf.vcf",
    info_fields=info_fields,
    sample_list=sample_list,
    format_fields=format_fields,
)
```

### Renaming custom columns and samples

From `v0.2.0`, renaming column and sample names is supported. Simply input a dictionary instead of a list with your name mapping. See example below.

```python
info_fields = {
    "info_field_1": "renamed_info_field_1",
    "info_field_2": "renamed_info_field_2"
}
sample_list = {
    "sample_name_1": "renamed_sample_name_1",
    "sample_name_2": "renamed_sample_name_2"
}
format_fields = {
    "format_name_1": "renamed_format_name_1",
    "format_name_2": "renamed_format_name_2"
}

df_renamed = vcf2pandas(
    "path_to_vcf.vcf",
    info_fields=info_fields,
    sample_list=sample_list,
    format_fields=format_fields,
)
```

> [!NOTE]
> You do not need to have everything a list or everything a dictionary, you can mix and match defaults, lists and dictionaries for `info_fields`, `sample_list` and `format_fields`.

## Custom column ordering

`vcf2pandas` can select custom/specific:

- INFO fields
- samples
- FORMAT fields

And order the selected columns based on the input list.

E.g. The following list:

```python
info_fields = ["DP", "MQM", "QA"]
```

Gets the columns (in that order)

```txt
INFO:DP    INFO:MQM    INFO:QA
```

## Output

### INFO and FORMAT headings

```txt
INFO:INFO_FIELD                     e.g. INFO:DP
FORMAT:SAMPLE_NAME:FORMAT_FIELD     e.g. FORMAT:HG002:GT
```

The info field, format field and sample names can also be mapped to custom values by using a dictionary. See [Renaming custom columns and samples](#renaming-custom-columns-and-samples).

### INFO or FORMAT fields not present for some variants

When certain INFO or FORMAT fields are not present for certain variants, `vcf2pandas` inserts a `.` instead in that cell. E.g. for `vcf3_all.txt` you can see `INFO:GENE` column has `.` for the first 7 variants.

## Examples

Example vcf and output files (dataframes as a .txt file) are available in `examples/`

### Example Usage

```python
df1_all = vcf2pandas("examples/vcf1.vcf")
df2_all = vcf2pandas("examples/vcf2.vcf")

df3_all = vcf2pandas("examples/vcf3.vcf")

info_fields = ["DP"]
sample_list = ["HG002"]
format_fields = ["GT", "AO"]

df3_selected = vcf2pandas(
    "examples/vcf3.vcf",
    info_fields=info_fields,
    sample_list=sample_list,
    format_fields=format_fields
)
```

To print to a text file:

```python
with open("path_to_txt_file.txt", "w", encoding='utf-8') as f:
    f.write(df.to_string())
```

For more examples, see `tests/run_examples.py`.

To recreate the examples in the `examples/` folder, run:

```bash
cd vcf2pandas
poetry run python tests/run_examples.py
```

## Changelog

### v0.1.0

- Initial project.

#### v0.1.1

- Fixed converting variant filter into string properly.

#### v0.1.2

- Updated pysam version to `0.22.1`.

### v0.2.0

- Fixed bug where some info/format fields would be overwritten with `.` if not all samples/variants had all the info/format values.
- Changed behaviour of getting info/format fields, it now takes from the vcf headers.
- Added functionality to rename columns using dictionaries. This is a non-breaking change, all existing uses of this package will still work.
- Added functionality to remove columns that are completely empty. Also a non-breaking change.
- Updated README with more examples.
- Added more tests for renaming columns.
- Added unit testing with pytest.

## Issues

Please open an issue if you encounter any problems! Thanks!
