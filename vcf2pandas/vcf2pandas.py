import pysam
import pandas


def vcf2pandas(
    vcf_file: str,
    info_fields: list[str] | dict[str, str] | None = None,
    sample_list: list[str] | dict[str, str] | None = None,
    format_fields: list[str] | dict[str, str] | None = None,
    remove_empty_columns: bool = False,
):
    def get_info_name(info_field: str) -> str:
        return f"INFO:{info_field}"

    def get_format_name(sample_name: str, format_field: str) -> str:
        return f"FORMAT:{sample_name}:{format_field}"

    vcf_reader = pysam.VariantFile(vcf_file)
    data: dict[str, list[str]] = {
        "CHROM": [],
        "POS": [],
        "ID": [],
        "REF": [],
        "ALT": [],
        "QUAL": [],
        "FILTER": [],
    }

    # Constructs a map from the vcf info field name to the info column name
    info_map: dict[str, str] = {}
    match info_fields:
        case None:
            # If no info_fields are provided, use the info fields specified
            # in the vcf file header.
            for key in vcf_reader.header.info.keys():
                info_map[key] = get_info_name(key)
        case list():
            info_map = {key: get_info_name(key) for key in info_fields}
        case dict():
            info_map = {key: get_info_name(value) for key, value in info_fields.items()}

    for value in info_map.values():
        data[value] = []

    # Constructs a map from the vcf sample name to the renamed sample name.
    sample_map: dict[str, str] = {}
    match sample_list:
        case None:
            # If no sample_list is provided, use all samples in the vcf file.
            for sample in vcf_reader.header.samples:
                sample_map[sample] = sample
        case list():
            sample_map = {key: key for key in sample_list}
        case dict():
            sample_map = sample_list

    # Constructs a map from the vcf sample name to a map from the vcf format field
    # name to the renamed format field name.
    format_map: dict[str, dict[str, str]] = {}
    match format_fields:
        case None:
            # If no format_fields are provided, use the format fields specified
            # in the vcf file header.
            for key, value in sample_map.items():
                format_map[key] = {
                    format_name: get_format_name(value, format_name)
                    for format_name in vcf_reader.header.formats.keys()
                }
        case list():
            for key, value in sample_map.items():
                format_map[key] = {
                    format_name: get_format_name(value, format_name)
                    for format_name in format_fields
                }
        case dict():
            for key, value in sample_map.items():
                format_map[key] = {
                    format_name: get_format_name(value, renamed_format_name)
                    for format_name, renamed_format_name in format_fields.items()
                }

    for sample_format_values in format_map.values():
        for value in sample_format_values.values():
            data[value] = []

    for variant in vcf_reader.fetch():
        # Manual addition of variant data
        data["CHROM"].append(variant.chrom)
        data["POS"].append(variant.pos)
        data["ID"].append(variant.id)
        data["REF"].append(variant.ref)
        data["ALT"].append(variant.alts)
        data["QUAL"].append(variant.qual)
        data["FILTER"].append(", ".join([v.name for v in variant.filter.values()]))

        # Add info fields
        for key, value in info_map.items():
            if key in variant.info:
                data[value].append(variant.info[key])
            else:
                data[value].append(".")

        # Add format fields
        for sample in variant.samples.values():
            # Skip samples not in sample_list
            if sample_list is not None and sample.name not in sample_list:
                continue

            for key, value in format_map[sample.name].items():
                if key in sample.keys():
                    data[value].append(sample[key])
                else:
                    data[value].append(".")

    df = pandas.DataFrame(data)

    if remove_empty_columns:
        df = df.loc[:, (df != ".").any(axis=0)]

    return df
