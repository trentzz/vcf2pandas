# vcf2pandas

`vcf2pandas` is a python package to convert vcf files to `pandas` dataframes. 

## Install

```bash
pip install vcf2pandas
```

## Dependencies

- pandas (2.1.0)
- pysam (0.21.0)

## Usage

### Selecting all columns

```python
from vcf2pandas import vcf2pandas
import pandas

df_all = vcf2pandas("path_to_vcf.vcf")
```

### Selecting custom custom columns and samples

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
```
INFO:DP    INFO:MQM    INFO:QA
```

Note that this **only applies for INFO and FORMAT columns**. That is, the samples will be ordered based on the VCF and not the input list.


## Output

### INFO and FORMAT headings
```
INFO:INFO_FIELD                     e.g. INFO:DP
FORMAT:SAMPLE_NAME:FORMAT_FIELD     e.g. FORMAT:HG002:GT
```

### INFO fields not present for some variants

When certain INFO fields are not present for certain variants, `vcf2pandas` inserts a `.` instead in that cell. E.g. for `vcf3_all.txt` you can see `INFO:GENE` column has `.` for the first 7 variants.


## Examples

Example vcf and output files (dataframes as a .txt file) are available in `examples/`

### Example Usage
```python
df1 = vcf2pandas("examples/vcf1.vcf")
df2 = vcf2pandas("examples/vcf2.vcf")

df3_all = vcf2pandas("examples/vcf3.vcf")

info = ["DP"]
samples = ["HG002"]
format_fields = ["GT", "AO"]
df3_selected = vcf2pandas("examples/vcf3.vcf")
```

To print to a text file:
```python
with open("path_to_txt_file.txt") as f:
    f.write(df.to_string())
```