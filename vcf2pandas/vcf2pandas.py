import pysam
import pandas


def vcf2pandas(
    vcf_file,
    info_fields: list[str] | dict[str, str] | None = None,
    sample_list: list[str] | dict[str, str] | None = None,
    format_fields: list[str] | dict[str, str] | None = None,
):
    vcf_reader = pysam.VariantFile(vcf_file)
    data = {
        "CHROM": [],
        "POS": [],
        "ID": [],
        "REF": [],
        "ALT": [],
        "QUAL": [],
        "FILTER": [],
    }

    def format_name(sample_name: str, format_field: str) -> str:
        return f"FORMAT:{sample_name}:{format_field}"
    
    def renamed_format_name(sample_name: str, format_field: str) -> str:
        return f"{sample_name}:{format_field}"

    def info_name(info_field: str) -> str:
        return f"INFO:{info_field}"

    variants_read = 0
    for variant in vcf_reader.fetch():
        data["CHROM"].append(variant.chrom)
        data["POS"].append(variant.pos)
        data["ID"].append(variant.id)
        data["REF"].append(variant.ref)
        data["ALT"].append(variant.alts)
        data["QUAL"].append(variant.qual)
        data["FILTER"].append(", ".join([v.name for v in variant.filter.values()]))

        match info_fields:
            case None:
                for key, value in variant.info.items():
                    if info_name(key) not in data:
                        data[info_name(key)] = ["."] * variants_read
                    data[info_name(key)].append(value)
            case list() as info_fields_list:
                for key in info_fields_list:
                    if info_name(key) not in data:
                        data[info_name(key)] = ["."] * variants_read
                    data[info_name(key)].append(variant.info[key])
            case dict() as info_fields_dict:
                for key, renamed_key in info_fields_dict.items():
                    if renamed_key not in data:
                        data[renamed_key] = ["."] * variants_read
                    data[renamed_key].append(variant.info[key])

        for sample in variant.samples.values():
            if sample_list is not None and sample.name not in sample_list:
                continue
            
            print(format_fields)

            match format_fields:
                case None:
                    for key, value in sample.items():
                        if format_name(sample.name, key) not in data:
                            data[format_name(sample.name, key)] = ["."] * variants_read
                        data[format_name(sample.name, key)].append(value)
                case list() as format_fields_list:
                    for key in format_fields_list:
                        if format_name(sample.name, key) not in data:
                            data[format_name(sample.name, key)] = ["."] * variants_read
                        data[format_name(sample.name, key)].append(sample[key])
                case dict() as format_fields_dict:
                    for key, renamed_key in format_fields_dict.items():
                        renamed_sample = sample_list[sample.name]
                        print(key, renamed_key)
                        print(renamed_sample)
                        print(renamed_format_name(renamed_sample, renamed_key))
                        if renamed_format_name(renamed_sample, renamed_key) not in data:
                            data[renamed_format_name(renamed_sample, renamed_key)] = ["."] * variants_read
                        data[renamed_format_name(renamed_sample, renamed_key)].append(sample[key])

        for value in data.values():
            if len(value) <= variants_read:
                value.append(".")

        variants_read += 1

    df = pandas.DataFrame(data)
    return df
