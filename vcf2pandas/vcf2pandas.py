import pysam
import pandas


def vcf2pandas(vcf_file, info_fields=None, sample_list=None, format_fields=None):
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

    variants_read = 0
    for variant in vcf_reader.fetch():
        data["CHROM"].append(variant.chrom)
        data["POS"].append(variant.pos)
        data["ID"].append(variant.id)
        data["REF"].append(variant.ref)
        data["ALT"].append(variant.alts)
        data["QUAL"].append(variant.qual)
        data["FILTER"].append(", ".join([v.name for v in variant.filter.values()]))

        if info_fields is None:
            for key, value in variant.info.items():
                if not info_name(key) in data:
                    data[info_name(key)] = ["."] * variants_read
                data[info_name(key)].append(value)
        else:
            for key in info_fields:
                if not info_name(key) in data:
                    data[info_name(key)] = ["."] * variants_read
                data[info_name(key)].append(variant.info[key])

        for sample in variant.samples.values():
            if sample_list is not None and sample.name not in sample_list:
                continue

            if format_fields is None:
                for key, value in sample.items():
                    if not format_name(sample.name, key) in data:
                        data[format_name(sample.name, key)] = ["."] * variants_read
                    data[format_name(sample.name, key)].append(value)
            else:
                for key in format_fields:
                    if not format_name(sample.name, key) in data:
                        data[format_name(sample.name, key)] = ["."] * variants_read
                    data[format_name(sample.name, key)].append(sample[key])

        for value in data.values():
            if len(value) <= variants_read:
                value.append(".")

        variants_read += 1

    df = pandas.DataFrame(data)
    return df


def format_name(sample_name, format_field):
    return f"FORMAT:{sample_name}:{format_field}"


def info_name(info_field):
    return f"INFO:{info_field}"
